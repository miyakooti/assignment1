import boto3
import requests
from io import BytesIO
# from PIL import Image

def get_img_urls_from_dynamodb(table_name):
    
    # DynamoDBクライアントの作成
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(table_name)

    # テーブルから全てのアイテムを取得
    response = table.scan()

    print(response['Items'][0]['image_url'])

    # アイテムから"img_url"属性の値を取り出す
    image_urls = [item['image_url'] for item in response['Items']]



    # S3クライアントの作成
    s3 = boto3.client('s3', region_name='us-east-1')
    bucket_name = "artist-images-s4075688"

    for image_url in image_urls:
        try:
            # 画像をダウンロード
            response = requests.get(image_url)
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                
                # 画像をS3にアップロード
                image_key = image_url.split('/')[-1]  # URLからファイル名を取得してキーとして使用
                s3.put_object(Body=image_data.getvalue(), Bucket=bucket_name, Key=image_key)
                print(f"Uploaded image {image_key} to S3 bucket {bucket_name}")
            else:
                print(f"Failed to download image from {image_url}")
        except Exception as e:
            print(f"Error occurred: {e}")



if __name__ == "__main__":

    # テーブル名を指定して"img_url"属性の値を取得
    img_urls = get_img_urls_from_dynamodb('music')

    # 結果を出力
    print(img_urls)

