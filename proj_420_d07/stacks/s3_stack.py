import os
import aws_cdk as cdk
from aws_cdk import aws_s3 as s3


class S3Stack(cdk.Stack):
    def __init__(self, scope: cdk.App, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Bucket S3 pour nos données
        self.bucket = s3.Bucket(
            scope=self,
            id="SourceBucket",
            versioned=True,
            bucket_name="source-bucket-420d07",  # os.getenv("SOURCE_S3_BUCKET"),
        )
