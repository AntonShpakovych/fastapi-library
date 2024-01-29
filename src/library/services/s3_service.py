import os

from dotenv import load_dotenv
import boto3


load_dotenv()


class S3Service:
    def __init__(
            self,
            aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY"),
            bucket_name: str = os.getenv("AWS_S3_BUCKET_NAME")
    ):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        self.bucket_name = bucket_name

    def upload_file(self, file: bytes, filename: str) -> None:
        self.s3_client.put_object(
            Body=file,
            Bucket=self.bucket_name,
            Key=filename
        )

    def download_file(self, filename):
        return self.s3_client.get_object(Bucket=self.bucket_name, Key=filename)
