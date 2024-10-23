from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
    aws_s3_notifications,
    Duration,
    aws_iam as iam
)

from constructs import Construct

class TumbnailGeneratorStack(Stack):
    """
    Stack responsible for setting up AWS resources required for the Thumbnail Generator service, 
    including an AWS Lambda function, S3 buckets for source and target images, 
    and a DynamoDB table for storing image metadata.
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        """
        Initializes the Thumbnail Generator stack with the necessary AWS resources.

        Args:
            scope (Construct): Scope in which this stack is defined.
            construct_id (str): Identifier for this construct.
            kwargs (dict): Additional keyword arguments.

        Returns:
            None
        """
        super().__init__(scope, construct_id, **kwargs)
        self.construct_id = construct_id

        # Main methods
        self.create_source_s3_bucket()
        self.create_destination_s3_bucket()
        self.create_s3_event()
        self.create_dynamo_db_table()
        self.create_lambda_function()

    def create_lambda_function(self):
        """
        Creates an AWS Lambda function that will generate thumbnails from source images.
        A role to access to the different resources required for this project is created too.

        The Lambda function uses Python 3.8 runtime and has a 15-second timeout with 128 MB memory.

        Returns:
            None
        """
        # Create IAM Role
        self.lambda_role = iam.Role(
            self, "LambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"), 
            description="Role that allows Lambda to access S3, DynamoDB and Lambda services",
        )

        # Add S3 permissions
        self.lambda_role.add_to_policy(iam.PolicyStatement(
            actions=["s3:GetObject", "s3:ListBucket"],
            resources=[self.source_bucket.bucket_arn, f"{self.source_bucket.bucket_arn}/*"]
        ))

        self.lambda_role.add_to_policy(iam.PolicyStatement(
            actions=["s3:GetObject", "s3:ListBucket", "s3:PutObject"],
            resources=[self.destination_bucket.bucket_arn, f"{self.source_bucket.bucket_arn}/*"]
        ))
        # Add DynamoDB permissions
        self.lambda_role.add_to_policy(iam.PolicyStatement(
            actions=["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:Scan", "dynamodb:Query"],
            resources=[self.metadata_table.table_arn]
        ))

        # Add Lambda permissions
        self.lambda_role.add_to_policy(iam.PolicyStatement(
            actions=["lambda:InvokeFunction"],
            resources=["*"] 
        ))
        self.fn = _lambda.Function(
                            self,
                            function_name="thumbnails-generator",
                            description="This Lambda function is a Thumbnail generator",
                            runtime=_lambda.Runtime.PYTHON_3_8,
                            handler="lambda_function.lambda_handler",
                            code=_lambda.Code.from_asset("./lambda"),
                            timeout=Duration.seconds(15),
                            memory_size=128,
                            role = self.lambda_role)

    def create_source_s3_bucket(self):
        """
        Creates an S3 bucket to store the source images.

        The bucket is versioned, has public access blocked, uses S3 managed encryption,
        and requires SSL for communication.

        Returns:
            None
        """
        self.source_bucket = s3.Bucket(
                                    self,
                                    bucket_name="thumbnails-generator-source-images-bucket",
                                    block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                                    encryption=s3.BucketEncryption.S3_MANAGED,
                                    enforce_sSL=True,
                                    versioned=True)

    def create_destination_s3_bucket(self):
        """
        Creates an S3 bucket to store the generated thumbnail images.

        Like the source bucket, this bucket is versioned, has public access blocked,
        and uses S3 managed encryption with SSL enforcement.

        Returns:
            None
        """
        self.destination_bucket = s3.Bucket(
                                    self, 
                                    bucket_name="thumbnails-generator-destination-images-bucket",
                                    block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                                    encryption=s3.BucketEncryption.S3_MANAGED,
                                    enforce_sSL=True,
                                    versioned=True)

    def create_s3_event(self):
        """
        Configures an S3 event to trigger the Lambda function whenever a new object 
        (image) is uploaded to the source S3 bucket.

        Returns:
            None
        """
        self.notification = aws_s3_notifications.LambdaDestination(self.fn)
        self.source_bucket.add_event_notification(s3.EventType.OBJECT_CREATED, self.notification)

    def create_dynamo_db_table(self):
        """
        Creates a DynamoDB table to store metadata about the images processed by the Lambda function.

        The table uses a string partition key named 'id'.

        Returns:
            None
        """
        self.metadata_table = dynamodb.Table(self, "thumbails-generator-metadata",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING))