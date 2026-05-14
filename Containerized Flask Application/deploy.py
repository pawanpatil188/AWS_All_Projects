import boto3
import subprocess
import sys

# ==============================
# CONFIG
# ==============================
region = "ap-south-1"
repo_name = "flask-app-repo"
cluster_name = "flask-cluster"
service_name = "flask-service"   # keep same name now
task_family = "flask-task"

account_id = boto3.client("sts").get_caller_identity()["Account"]

# ✅ FIXED (no comma)
execution_role = f"arn:aws:iam::{account_id}:role/ecsTaskExecutionRole"

# ✅ Your subnet
subnets = ["subnet-0caa43be2ceec266b"]

# ==============================
# CLIENTS
# ==============================
ecr = boto3.client("ecr", region_name=region)
ecs = boto3.client("ecs", region_name=region)

# ==============================
# HELPER FUNCTION
# ==============================
def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ Command failed: {cmd}")
        sys.exit(1)

# ==============================
# 1. CREATE ECR REPO
# ==============================
print("🔹 Creating ECR repository...")
try:
    repo = ecr.create_repository(repositoryName=repo_name)
    repo_uri = repo['repository']['repositoryUri']
except:
    repo = ecr.describe_repositories(repositoryNames=[repo_name])
    repo_uri = repo['repositories'][0]['repositoryUri']

print("✅ ECR:", repo_uri)

# ==============================
# 2. LOGIN TO ECR
# ==============================
print("🔹 Logging into ECR...")
run_cmd(
    f"aws ecr get-login-password --region {region} | docker login --username AWS --password-stdin {account_id}.dkr.ecr.{region}.amazonaws.com"
)

# ==============================
# 3. BUILD & PUSH IMAGE
# ==============================
print("🔹 Building Docker image...")
run_cmd(f"docker build -t {repo_name} .")

print("🔹 Tagging image...")
run_cmd(f"docker tag {repo_name}:latest {repo_uri}:latest")

print("🔹 Pushing image...")
run_cmd(f"docker push {repo_uri}:latest")

# ==============================
# 4. CREATE ECS CLUSTER
# ==============================
print("🔹 Creating ECS cluster...")
try:
    ecs.create_cluster(clusterName=cluster_name)
except:
    print("Cluster already exists")

# ==============================
# 5. REGISTER TASK DEF
# ==============================
print("🔹 Registering task definition...")

task_def = ecs.register_task_definition(
    family=task_family,
    networkMode="awsvpc",
    requiresCompatibilities=["FARGATE"],
    cpu="256",
    memory="512",
    executionRoleArn=execution_role,
    containerDefinitions=[
        {
            "name": "flask-container",
            "image": f"{repo_uri}:latest",
            "portMappings": [
                {
                    "containerPort": 5000,
                    "protocol": "tcp"
                }
            ],
            "essential": True
        }
    ]
)

task_def_arn = task_def['taskDefinition']['taskDefinitionArn']

# ==============================
# 6. CREATE OR UPDATE SERVICE
# ==============================
print("🔹 Creating/Updating ECS service...")

services = ecs.list_services(cluster=cluster_name)

service_exists = any(service_name in s for s in services['serviceArns'])

if service_exists:
    print("🔁 Service exists → updating...")

    ecs.update_service(
        cluster=cluster_name,
        service=service_name,
        taskDefinition=task_def_arn,
        desiredCount=1
    )

else:
    print("🆕 Creating new service...")

    ecs.create_service(
        cluster=cluster_name,
        serviceName=service_name,
        taskDefinition=task_def_arn,
        desiredCount=1,
        launchType="FARGATE",
        networkConfiguration={
            "awsvpcConfiguration": {
                "subnets": subnets,
                "assignPublicIp": "ENABLED"
            }
        }
    )

print("\n🎉 DEPLOYMENT SUCCESSFUL!")