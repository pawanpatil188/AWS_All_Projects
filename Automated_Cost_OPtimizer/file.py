import boto3
import json
import time
import zipfile

REGION = "ap-south-1"
ROLE_NAME = "AutoStopLambdaRole"
FUNCTION_NAME = "AutoStopEC2Function"

iam = boto3.client("iam")
lambda_client = boto3.client("lambda", region_name=REGION)
events = boto3.client("events", region_name=REGION)

# -----------------------------
# STEP 1: CREATE IAM ROLE
# -----------------------------
def create_iam_role():
    try:
        role = iam.create_role(
            RoleName=ROLE_NAME,
            AssumeRolePolicyDocument=json.dumps({
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Principal": {"Service": "lambda.amazonaws.com"},
                    "Action": "sts:AssumeRole"
                }]
            })
        )

        # Attach policies
        iam.attach_role_policy(
            RoleName=ROLE_NAME,
            PolicyArn="arn:aws:iam::aws:policy/AmazonEC2FullAccess"
        )
        iam.attach_role_policy(
            RoleName=ROLE_NAME,
            PolicyArn="arn:aws:iam::aws:policy/CloudWatchReadOnlyAccess"
        )
        iam.attach_role_policy(
            RoleName=ROLE_NAME,
            PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
        )

        print("IAM Role created")

        time.sleep(10)  # wait for role to propagate
        return role["Role"]["Arn"]

    except Exception as e:
        print("Role exists or error:", e)
        role = iam.get_role(RoleName=ROLE_NAME)
        return role["Role"]["Arn"]

# -----------------------------
# STEP 2: CREATE LAMBDA CODE ZIP
# -----------------------------
def create_lambda_zip():
    code = '''
import boto3
from datetime import datetime, timedelta

ec2 = boto3.client("ec2")
cloudwatch = boto3.client("cloudwatch")

def lambda_handler(event, context):

    print("Checking idle instances...")

    instances = ec2.describe_instances(
        Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
    )

    to_stop = []

    for r in instances["Reservations"]:
        for i in r["Instances"]:
            instance_id = i["InstanceId"]

            end = datetime.utcnow()
            start = end - timedelta(minutes=30)

            metrics = cloudwatch.get_metric_statistics(
                Namespace="AWS/EC2",
                MetricName="CPUUtilization",
                Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
                StartTime=start,
                EndTime=end,
                Period=300,
                Statistics=["Average"]
            )

            data = metrics["Datapoints"]

            if not data:
                to_stop.append(instance_id)
                continue

            avg = sum(d["Average"] for d in data)/len(data)

            if avg < 5:
                to_stop.append(instance_id)

    if to_stop:
        ec2.stop_instances(InstanceIds=to_stop)
        print("Stopped:", to_stop)
    else:
        print("No idle instances")

    return {"statusCode":200}
'''

    with open("lambda_function.py", "w") as f:
        f.write(code)

    with zipfile.ZipFile("lambda.zip", "w") as z:
        z.write("lambda_function.py")

    print("Lambda ZIP created")

# -----------------------------
# STEP 3: CREATE LAMBDA FUNCTION
# -----------------------------
def create_lambda(role_arn):
    try:
        with open("lambda.zip", "rb") as f:
            response = lambda_client.create_function(
                FunctionName=FUNCTION_NAME,
                Runtime="python3.9",
                Role=role_arn,
                Handler="lambda_function.lambda_handler",
                Code={"ZipFile": f.read()},
                Timeout=60
            )
        print("Lambda created")
        return response["FunctionArn"]

    except Exception as e:
        print("Lambda exists or error:", e)
        response = lambda_client.get_function(FunctionName=FUNCTION_NAME)
        return response["Configuration"]["FunctionArn"]

# -----------------------------
# STEP 4: CREATE SCHEDULE (CLOUDWATCH)
# -----------------------------
def create_schedule(lambda_arn):
    rule_name = "AutoStopSchedule"

    events.put_rule(
        Name=rule_name,
        ScheduleExpression="rate(1 hour)",
        State="ENABLED"
    )

    events.put_targets(
        Rule=rule_name,
        Targets=[{
            "Id": "1",
            "Arn": lambda_arn
        }]
    )

    lambda_client.add_permission(
        FunctionName=FUNCTION_NAME,
        StatementId="AllowEventBridge",
        Action="lambda:InvokeFunction",
        Principal="events.amazonaws.com",
        SourceArn=f"arn:aws:events:{REGION}:{boto3.client('sts').get_caller_identity()['Account']}:rule/{rule_name}"
    )

    print("Schedule created (runs every hour)")

# -----------------------------
# MAIN EXECUTION
# -----------------------------
if __name__ == "__main__":
    print("🚀 Setting up Automated Cost Optimizer...\n")

    role_arn = create_iam_role()
    create_lambda_zip()
    lambda_arn = create_lambda(role_arn)
    create_schedule(lambda_arn)

    print("\n✅ FULLY AUTOMATED SETUP COMPLETE!")