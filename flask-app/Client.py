import os
from boto3 import Session


class Client:
    def __init__(self):
        ses = Session(aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                      aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
                      region_name=os.environ.get('REGION_NAME'))
        self.bucket_name = os.environ.get('BUCKET_NAME')
        self.s3 = ses.resource('s3')
        self.session_client = ses.client('s3')

    def put_to_bucket(self, input_file, write_file_name):
        data = open(input_file, 'rb')
        self.s3.Bucket(self.bucket_name).put_object(Key=write_file_name, Body=data)

    def get_presigned_url(self, file_key):
        url = self.session_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': self.bucket_name,
                'Key': file_key,
                'ResponseContentDisposition': 'attachment'
            },
            ExpiresIn=600
        )
        return url
