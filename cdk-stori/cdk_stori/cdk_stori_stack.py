from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
    aws_s3_notifications,
    Duration
)

from constructs import Construct
from pathlib import Path

class TumbnailGeneratorStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.construct_id = construct_id

        #Main methods
        self.create_lambda_function()
        self.create_source_s3_bucket()
        self.create_target_s3_bucket()
        self.create_s3_event()
        self.create_dynamo_db_table()

    def create_lambda_function(self):
        self.fn = _lambda.Function(
                            self,
                            function_name = "thumbnails-generator",
                            description = "This Lambda function is a Thumbnail generator",
                            runtime = _lambda.Runtime.PYTHON_3_8,
                            handler = "lambda_function.lambda_handler",
                            code = _lambda.Code.from_asset("./lambda"),
                            timeout = Duration.seconds(15),
                            memory_size=128)
    
    def create_source_s3_bucket(self):
        self.source_bucket = s3.Bucket(
                                    self,
                                    bucket_name = "thumbnails-generator-source-images-bucket",
                                    block_public_access = s3.BlockPublicAccess.BLOCK_ALL,
                                    encryption=s3.BucketEncryption.S3_MANAGED,
                                    enforce_sSL=True,
                                    versioned=True)

    
    def create_target_s3_bucket(self):
        self.target_bucket = s3.Bucket(
                                    self, 
                                    bucket_name = "thumbnails-generator-target-images-bucket",
                                    block_public_access = s3.BlockPublicAccess.BLOCK_ALL,
                                    encryption=s3.BucketEncryption.S3_MANAGED,
                                    enforce_sSL=True,
                                    versioned=True)

    def create_s3_event(self):
        # create s3 notification for lambda function
        self.notification = aws_s3_notifications.LambdaDestination(self.fn)
        # assign notification for the s3 event type
        self.source_bucket.add_event_notification(s3.EventType.OBJECT_CREATED, self.notification)
    
    def create_dynamo_db_table(self):
        # Create Dynamodb table to store image's metadata
        self.metadata_table = dynamodb.Table(self, "thumbails-generator-metadata",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING)
        )