import boto3
import json
import time

region = "ap-south-1"

s3 = boto3.client('s3', region_name=region)
iam = boto3.client('iam')
codebuild = boto3.client('codebuild', region_name=region)
codepipeline = boto3.client('codepipeline', region_name=region)
ec2 = boto3.resource('ec2', region_name=region)

bucket_name = "attendance-cicd-bucket-123456789"

# -----------------------------
# 1. CREATE S3 BUCKET
# -----------------------------
def create_bucket():
    try:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )
        print("S3 bucket created")
    except Exception as e:
        print("Bucket exists:", e)

# -----------------------------
# 2. CREATE IAM ROLE
# -----------------------------
def create_role():
    role_name = "CodePipelineServiceRole"

    assume_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "codepipeline.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }

    try:
        role = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(assume_policy)
        )

        iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn="arn:aws:iam::aws:policy/AdministratorAccess"
        )

        print("IAM Role created")
        return role['Role']['Arn']

    except Exception as e:
        print("Role exists:", e)
        return iam.get_role(RoleName=role_name)['Role']['Arn']

# -----------------------------
# 3. CREATE EC2 INSTANCE
# -----------------------------
def create_ec2():
    instances = ec2.create_instances(
        ImageId="ami-0f5ee92e2d63afc18",  # Amazon Linux
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName="your-key",  # change this
        SecurityGroupIds=["your-sg"],  # change this
        UserData="""#!/bin/bash
        yum update -y
        yum install python3 git -y
        pip3 install flask
        """
    )

    instance = instances[0]
    instance.wait_until_running()
    print("EC2 created:", instance.id)
    return instance.id

# -----------------------------
# 4. CREATE CODEBUILD
# -----------------------------
def create_codebuild(role_arn):
    project_name = "AttendanceBuild"

    codebuild.create_project(
        name=project_name,
        source={
            'type': 'S3',
            'location': f"{bucket_name}/source.zip"
        },
        artifacts={'type': 'NO_ARTIFACTS'},
        environment={
            'type': 'LINUX_CONTAINER',
            'image': 'aws/codebuild/standard:5.0',
            'computeType': 'BUILD_GENERAL1_SMALL'
        },
        serviceRole=role_arn
    )

    print("CodeBuild created")

# -----------------------------
# 5. CREATE CODEPIPELINE
# -----------------------------
def create_pipeline(role_arn):
    pipeline = {
        "pipeline": {
            "name": "AttendancePipeline",
            "roleArn": role_arn,
            "artifactStore": {
                "type": "S3",
                "location": bucket_name
            },
            "stages": [
                {
                    "name": "Source",
                    "actions": [{
                        "name": "Source",
                        "actionTypeId": {
                            "category": "Source",
                            "owner": "AWS",
                            "provider": "S3",
                            "version": "1"
                        },
                        "outputArtifacts": [{"name": "source_output"}],
                        "configuration": {
                            "S3Bucket": bucket_name,
                            "S3ObjectKey": "source.zip"
                        }
                    }]
                },
                {
                    "name": "Build",
                    "actions": [{
                        "name": "Build",
                        "actionTypeId": {
                            "category": "Build",
                            "owner": "AWS",
                            "provider": "CodeBuild",
                            "version": "1"
                        },
                        "inputArtifacts": [{"name": "source_output"}],
                        "outputArtifacts": [{"name": "build_output"}],
                        "configuration": {
                            "ProjectName": "AttendanceBuild"
                        }
                    }]
                }
            ],
            "version": 1
        }
    }

    codepipeline.create_pipeline(**pipeline)
    print("Pipeline created")

# -----------------------------
# MAIN EXECUTION
# -----------------------------
if __name__ == "__main__":
    create_bucket()
    role_arn = create_role()
    instance_id = create_ec2()
    time.sleep(10)
    create_codebuild(role_arn)
    create_pipeline(role_arn)

    print("CI/CD setup complete")