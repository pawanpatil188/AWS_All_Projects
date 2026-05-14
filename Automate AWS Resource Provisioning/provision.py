import boto3
import time

# -----------------------------
# CONFIG (EDIT THESE)
# -----------------------------
REGION = "ap-south-1"
BUCKET_NAME = "my-unique-bucket-12345-demo123"   # must be globally unique
IAM_USER_NAME = "demo-user-boto325"
INSTANCE_TYPE = "t3.micro"   # Free Tier safe
AMI_ID = "ami-0f58b397bc5c1f2e86"  # Amazon Linux (update if needed)
KEY_NAME = "privisoning"    # WITHOUT .pem

# -----------------------------
# CLIENTS
# -----------------------------
s3 = boto3.client("s3", region_name=REGION)
ec2 = boto3.client("ec2", region_name=REGION)
iam = boto3.client("iam")

# -----------------------------
# 1️⃣ CREATE S3 BUCKET
# -----------------------------
def create_s3_bucket():
    try:
        if REGION == "us-east-1":
            s3.create_bucket(Bucket=BUCKET_NAME)
        else:
            s3.create_bucket(
                Bucket=BUCKET_NAME,
                CreateBucketConfiguration={"LocationConstraint": REGION}
            )
        print(f"S3 Bucket created: {BUCKET_NAME}")
    except Exception as e:
        print("S3 (may already exist):", e)

# -----------------------------
# 2️⃣ CREATE IAM USER
# -----------------------------
def create_iam_user():
    try:
        iam.create_user(UserName=IAM_USER_NAME)

        iam.attach_user_policy(
            UserName=IAM_USER_NAME,
            PolicyArn="arn:aws:iam::aws:policy/AmazonS3FullAccess"
        )

        print(f"IAM User created: {IAM_USER_NAME}")
    except Exception as e:
        print("IAM (may already exist):", e)

# -----------------------------
# 3️⃣ CREATE OR GET SECURITY GROUP
# -----------------------------
def create_or_get_security_group():
    try:
        response = ec2.describe_security_groups(
            Filters=[{"Name": "group-name", "Values": ["boto3-sg"]}]
        )

        if response["SecurityGroups"]:
            sg_id = response["SecurityGroups"][0]["GroupId"]
            print(f"Using existing Security Group: {sg_id}")
            return sg_id

        response = ec2.create_security_group(
            GroupName="boto3-sg",
            Description="Security group for boto3 EC2"
        )

        sg_id = response["GroupId"]

        ec2.authorize_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": 22,
                    "ToPort": 22,
                    "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
                }
            ]
        )

        print(f"Created new Security Group: {sg_id}")
        return sg_id

    except Exception as e:
        print("SG Error:", e)
        return None

# -----------------------------
# 4️⃣ LAUNCH EC2 INSTANCE
# -----------------------------
def launch_ec2_instance(sg_id):
    try:
        response = ec2.run_instances(
            ImageId=AMI_ID,
            InstanceType=INSTANCE_TYPE,
            KeyName=KEY_NAME,
            MaxCount=1,
            MinCount=1,
            SecurityGroupIds=[sg_id]
        )

        instance_id = response["Instances"][0]["InstanceId"]

        print(f"EC2 Instance launched: {instance_id}")
        return instance_id

    except Exception as e:
        print("EC2 Error:", e)

# -----------------------------
# MAIN EXECUTION
# -----------------------------
if __name__ == "__main__":
    print("🚀 Starting AWS Resource Provisioning...\n")

    create_s3_bucket()
    create_iam_user()

    sg_id = create_or_get_security_group()

    if sg_id:
        launch_ec2_instance(sg_id)

    print("\n✅ Script execution completed!")