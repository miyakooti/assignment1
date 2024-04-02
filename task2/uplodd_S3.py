import boto3

def get_img_urls_from_dynamodb(table_name):
    
    # DynamoDBクライアントの作成
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(table_name)

    # テーブルから全てのアイテムを取得
    response = table.scan()

    # アイテムから"img_url"属性の値を取り出す
    img_urls = [item['img_url'] for item in response['Items']]

    return img_urls


if __name__ == "__main__":
    
    # テーブル名を指定して"img_url"属性の値を取得
    img_urls = get_img_urls_from_dynamodb('music')

    # 結果を出力
    print(img_urls)

