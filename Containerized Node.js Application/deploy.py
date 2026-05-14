import boto3
import subprocess

region = "ap-south-1"
repo_name = "node-app-repo"
cluster_name = "node-cluster"
service_name = "node-service"
task_family = "node-task"

account_id = boto3.client("sts").get_caller_identity()["Account"]

ecr = boto3.client("ecr", region_name=region)
ecs = boto3.client("ecs", region_name=region)

# ==============================
# 1. CREATE ECR REPO
# ==============================
try:
    repo = ecr.create_repository(repositoryName=repo_name)
    repo_uri = repo['repository']['repositoryUri']
except:
    repo = ecr.describe_repositories(repositoryNames=[repo_name])
    repo_uri = repo['repositories'][0]['repositoryUri']

print("ECR:", repo_uri)

# ==============================
# 2. LOGIN TO ECR
# ==============================
subprocess.run(
    f"aws ecr get-login-password --region {region} | docker login --username AWS --password-stdin {account_id}.dkr.ecr.{region}.amazonaws.com",
    shell=True
)

# ==============================
# 3. BUILD & PUSH IMAGE
# ==============================
subprocess.run(f"docker build -t {repo_name} .", shell=True)
subprocess.run(f"docker tag {repo_name}:latest {repo_uri}:latest", shell=True)
subprocess.run(f"docker push {repo_uri}:latest", shell=True)

# ==============================
# 4. CREATE ECS CLUSTER
# ==============================
try:
    ecs.create_cluster(clusterName=cluster_name)
except:
    pass

# ==============================
# 5. REGISTER TASK DEF
# ==============================
task_def = ecs.register_task_definition(
    family=task_family,
    networkMode="awsvpc",
    requiresCompatibilities=["FARGATE"],
    cpu="256",
    memory="512",
    executionRoleArn="arn:aws:iam::794248399953:role/ecsTaskExecutionRole",
    containerDefinitions=[
        {
            "name": "node-container",
            "image": f"{repo_uri}:latest",
            "portMappings": [
                {
                    "containerPort": 3000,
                    "protocol": "tcp"
                }
            ],
            "essential": True
        }
    ]
)

task_def_arn = task_def['taskDefinition']['taskDefinitionArn']

# ==============================
# 6. CREATE SERVICE
# ==============================
ecs.create_service(
    cluster=cluster_name,
    serviceName=service_name,
    taskDefinition=task_def_arn,
    desiredCount=1,
    launchType="FARGATE",
    networkConfiguration={
        "awsvpcConfiguration": {
            "subnets": ["subnet-0caa43be2ceec266b"],  # Replace
            "assignPublicIp": "ENABLED"
        }
    }
)

print("✅ Node.js ECS App Deployed!")