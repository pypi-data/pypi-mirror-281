import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Hardcoded AWS credentials
AWS_ACCESS_KEY_ID = 'AKIA6ODU5DHTXUGV4HME'
AWS_SECRET_ACCESS_KEY = 'tnbu500PnZhIQvPMDrv51rGjozGJ+GLCH3ua2MQ7'
AWS_REGION = 'us-east-2'

# The name of the S3 bucket to list objects from
BUCKET_NAME = 'your_bucket_name'

def list_s3_objects(access_key, secret_key, region, bucket_name):
    try:
        # Create a session using the hardcoded credentials
        session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

        # Create an S3 client
        s3_client = session.client('s3')

        # List objects in the specified bucket
        response = s3_client.list_objects_v2(Bucket=bucket_name)

        # Check if the bucket contains objects
        if 'Contents' in response:
            print(f"Objects in bucket '{bucket_name}':")
            for obj in response['Contents']:
                print(f" - {obj['Key']}")
        else:
            print(f"The bucket '{bucket_name}' is empty or does not exist.")

    except NoCredentialsError:
        print("Credentials not available.")
    except PartialCredentialsError:
        print("Incomplete credentials provided.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    list_s3_objects(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, BUCKET_NAME)
