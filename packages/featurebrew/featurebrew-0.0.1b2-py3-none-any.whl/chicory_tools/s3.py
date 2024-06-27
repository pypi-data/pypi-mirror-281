import os
import tempfile

import boto3
from langchain_core.tools import tool

from utils.helper import doc_loader


class AmazonS3:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name='us-west-1'):
        self.s3 = boto3.client('s3', region_name=region_name,
                               aws_access_key_id=aws_access_key_id,
                               aws_secret_access_key=aws_secret_access_key)

    def list_buckets(self):
        """
        List all S3 buckets

        :return: list of bucket names in json format
        """
        return self.s3.list_buckets()


    def list_buckets_in_region(self, region):
        # List all buckets
        all_buckets = self.s3.list_buckets()

        # Create a list to hold buckets in the specified region
        regional_buckets = []

        # Iterate through all buckets and check their location
        for bucket in all_buckets['Buckets']:
            # Get the bucket location
            bucket_location = self.s3.get_bucket_location(Bucket=bucket['Name'])

            # Check if the bucket's region matches the specified region
            bucket_region = bucket_location['LocationConstraint']
            if bucket_region == region:
                regional_buckets.append(bucket['Name'])
            # Handle the case for the 'us-east-1' region (known as 'None' in the LocationConstraint)
            elif bucket_region is None and region == 'us-east-1':
                regional_buckets.append(bucket['Name'])

        return regional_buckets


    def describe_bucket(self, bucket_name):
        """
        Get the bucket policy or an error if no policy is set

        :param bucket_name:
        :return: bucket description in json format
        """
        try:
            return self.s3.get_bucket_policy(Bucket=bucket_name)
        except Exception as e:
            return str(e)

    def list_files(self, bucket_name):
        """
        List files in a specific S3 bucket

        :param bucket_name:
        :return: list of file names in json format
        """
        return self.s3.list_objects(Bucket=bucket_name)


class S3Downloader:
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, region_name='us-west-1'):
        if not aws_access_key_id or not aws_secret_access_key:
            self.s3 = boto3.client('s3', region_name=region_name)
        else:
            self.s3 = boto3.client('s3', region_name=region_name,
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key
                                 )

    def download_file(self, bucket_name, s3_object_key, local_file_path):
        """
        Download a file from an S3 bucket.

        :param bucket_name: Name of the S3 bucket.
        :param s3_object_key: Key of the object in the S3 bucket (essentially the file path in S3).
        :param local_file_path: Path to which the file will be downloaded locally.
        """
        try:
            if s3_object_key.endswith("_SUCCESS"):
                return
            self.s3.download_file(bucket_name, s3_object_key, local_file_path)
            print(f"File downloaded successfully from S3: {s3_object_key} to {local_file_path}")
        except Exception as e:
            print(f"Error downloading file from S3: {e}")

    def download_dir(self, bucket_name, s3_prefix, local_dir, mock_download_dir=False, check_path=None):
        """
        Recursively download files from a given S3 bucket and prefix to a local directory.
        """
        object_list = {}
        try:
            paginator = self.s3.get_paginator('list_objects_v2')
            for page in paginator.paginate(Bucket=bucket_name, Prefix=s3_prefix):
                for obj in page.get('Contents', []):
                    s3_object_key = obj['Key']
                    if not s3_object_key.endswith('/'):  # Skip directories
                        local_file_path = os.path.join(local_dir, s3_object_key)
                        local_file_dir = os.path.dirname(local_file_path)

                        if not check_path or check_path in s3_object_key:
                            object_list[bucket_name + "/" + s3_object_key] = ""

                        # Create local directory structure if it doesn't exist
                        if not os.path.exists(local_file_dir):
                            os.makedirs(local_file_dir)
                        if not mock_download_dir and bucket_name + "/" + s3_object_key in object_list:
                            self.download_file(bucket_name, s3_object_key, local_file_path)
                            object_list[bucket_name + "/" + s3_object_key] = local_file_path

        except Exception as e:
            print(f"Error downloading file from S3: {e}")
        finally:
            return object_list

@tool
def s3_loader(s3_uri, region=None):
    """Get a document loader for passed s3 path formatted as a string parameters.
    It needs aws region to be passed as an argument along with the s3 uri.
    It needs cluster-id to be passed as an argument along with the s3 uri.
    It downloads the document from s3 and returns a doc loader as per the doc type.
    """
    if region is not None:
        return s3_downloader(s3_uri, region)
    else:
        regions = ['us-west-1', 'us-west-2', 'us-east-1', 'us-east-2']
        for region in regions:
            doc = s3_downloader(s3_uri, region)
            if len(doc) > 0:
                return doc
        return []

def s3_downloader(s3_uri, region):
    docs = []
    s3_downloader = S3Downloader(region_name=region)
    uri_without_scheme = s3_uri.split("://", 1)[1] if "://" in s3_uri else s3_uri
    # Split the remaining string into bucket and path
    bucket_name, path = uri_without_scheme.split("/", 1)

    file_extension = os.path.splitext(path)[1]
    # Create a temporary directory
    tmp_dir = tempfile.mkdtemp()

    import uuid
    local_file_path = os.path.join(tmp_dir, "s3_file" + str(uuid.uuid4().hex))

    try:
        object_dict = s3_downloader.download_dir(bucket_name, path,
                                                 local_file_path,
                                                 mock_download_dir=False)
    except Exception as e:
        print(e)
        return docs
    for obj_key, obj_val in object_dict.items():
        if obj_val != "":
            meta = {
                "location_type": "s3",
                "bucket_name": bucket_name if bucket_name else  "",
                "identifier": path if path else  "",
                "source_location": obj_key if obj_key else  "",
                "emr_cluster": cluster_id if cluster_id else  "",
                "region": region if region else  "",
                "provider": "aws",
            }
            # i = 1
            # for key in obj_key.split("/"):
            #     meta[f"tag{i}"] = key
            #     i += 1
            if os.path.exists(obj_val):
                doc = doc_loader(obj_val, file_extension)
                docs.append(doc)
    return docs
