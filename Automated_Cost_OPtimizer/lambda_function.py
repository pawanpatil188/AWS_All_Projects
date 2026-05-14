
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
