from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_lambda_event_sources as lambda_events,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
    aws_s3_notifications
)

from constructs import Construct
from pathlib import Path

class TumbnailGeneratorStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.create_lambda_function()
        self.create_s3_bucket("thumbnails-generator-source-images-bucket")
        self.create_s3_bucket("thumbnails-generator-target-images-bucket")
        self.create_s3_event()

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
        
        def create_s3_bucket(self, bucket_name):
            # Create soruce S3 bucket (original images)
            self.source_bucket = s3.Bucket(self, bucket_name)
        
        def create_s3_event(self):
            # create s3 notification for lambda function
            notification = aws_s3_notifications.LambdaDestination(function)
            # assign notification for the s3 event type
            s3.add_event_notification(s3.EventType.OBJECT_CREATED, notification)