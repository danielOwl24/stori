import json
import boto3
from PIL import Image
from io import BytesIO
import os
from PIL.ExifTags import TAGS
import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
THUMBNAIL_SIZE = (64, 64)
def generate_thumbnail(s3_object_content, thumbnail_key):
    """
    Generates a thumbnail from an image using the Pillow library.

    Args:
        s3_object_content (bytes): The content of the S3 object (image file) in bytes.
        thumbnail_key (str): The key (filename) for the thumbnail in S3 storage.

    Returns:
        Image object: A resized image object in thumbnail format.
        
    Raises:
        OSError: If the image file cannot be opened or processed.
    """
    """Genera una miniatura a partir de una imagen utilizando Pillow."""
    try:
        with Image.open(BytesIO(s3_object_content)) as image:
            image.thumbnail(THUMBNAIL_SIZE)
            exif_data = image._getexif()
            metadata = {}
            metadata['Id'] = thumbnail_key
            metadata['Size'] = image.size
            metadata['CreatedAt'] = datetime.utcnow().isoformat()
            metadata['Format'] = image.format
            metadata['Mode'] = image.mode
            if exif_data is not None:
                for tag_id, value in exif_data.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    metadata['Exif'][tag_name] = value
            return image, metadata
    except OSError:
        print(f"It was not possible to create thumbnail for {thumbnail_key}.")

def save_thumbnail_metadata(metadata, thumbnail_key):
    """
    Saves the metadata of a thumbnail in a DynamoDB table.

    Args:
        metadata (dict): A dictionary containing the metadata associated with the thumbnail. It must include the necessary attributes for the DynamoDB table.
        thumbnail_key (str): The identifier or name of the thumbnail, used to log which thumbnail is being processed.
    """
    try:
        table = dynamodb.Table('thumbails-generator-metadata')
        table.put_item(Item=metadata)
        print(f"Metadata of the thumbnail {thumbnail_key} was stored in DynamoDB.")
    except Exception as e:
        print(f"An unexpected error occurred while saving metadata for thumbnail {thumbnail_key}: {str(e)}")
        raise
def lambda_handler(event, context):
    """
    Main AWS Lambda function that processes S3 events to generate thumbnails.

    This function is triggered by an S3 event when an image is uploaded. It retrieves the image,
    generates a thumbnail, and saves the thumbnail to a specified destination bucket.

    Args:
        event (dict): The event payload that includes information about the S3 event (bucket name, object key).
        context (object): Provides runtime information to the Lambda function.

    Returns:
        dict: Response containing the HTTP status code and a success or error message.

    Raises:
        Exception: If there is an issue with retrieving or processing the S3 object, 
        the exception is caught and logged, and a 500 status code is returned."""
    
    # Get the S3 event information
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    destination_bucket = "thumbnails-generator-destination-images-bucket"
    
    try:
        # Get the S3 original image
        s3_object = s3.get_object(Bucket=source_bucket, Key=key)
        s3_object_content = s3_object.get("Body").read()
        
        # Generate the thumbnail
        thumbnail, metadata_dict= generate_thumbnail(s3_object_content, thumbnail_key)
        
        # Create the filename to store the thumbnail, it will have the same key of the original image
        thumbnail_key = f"thumbnails/{key.split('/')[-1]}"
        
        # Save metadata thumbnail within a DynamoDB table
        save_thumbnail_metadata(metadata_dict, thumbnail_key)

        # Save the thumbnail into the destination bucket
        s3.put_object(
            Bucket=destination_bucket,
            Key=thumbnail_key,
            Body=thumbnail,
            ContentType='image/jpeg'
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(f'Thumbnail created successfully: {thumbnail_key}')
        }
        
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error generating thumbnail {thumbnail_key}')
        }