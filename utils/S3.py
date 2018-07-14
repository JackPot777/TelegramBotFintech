import boto3
import configuration.private as priv
import configuration.public as publ

class S3Instance:

    def __init__(self,
                 key_id=priv.AWS_ACCESS_KEY_ID,
                 access_key=priv.AWS_SECRET_ACCESS_KEY):
        self.__key_id = key_id
        self.__access_key = access_key
        self.s3client = boto3.client('s3',
                               aws_access_key_id=self.__key_id,
                               aws_secret_access_key=self.__access_key
                               )
        self.s3res = boto3.resource('s3')

    def deleteFilesInS3Bucket(self, BucketName: str = publ.s3_picturesbucket):
        """Deletes all files in bucket"""
        bucket = self.s3res.Bucket(BucketName)
        bucket.objects.all().delete()