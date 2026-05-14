# 🚀 Containerized Flask Application on AWS ECS (Fargate)

## 📌 Project Overview
This project demonstrates how to containerize a Flask web application using Docker and deploy it on AWS ECS using Amazon ECR and Fargate.

The entire deployment was done using a combination of AWS Console + boto3 automation scripts for learning cloud infrastructure.

---

## 🎯 Objective
- Build Flask web application
- Containerize using Docker
- Push image to Amazon ECR
- Deploy on AWS ECS (Fargate)

---

## 🧰 AWS Services Used
- Amazon ECS (Elastic Container Service)
- Amazon ECR (Elastic Container Registry)
- AWS IAM (Execution Role)
- AWS CloudWatch (logs - optional)
- AWS CLI

---

## 🏗️ Architecture
Local Machine → Docker Image → ECR → ECS Fargate → Running Flask Container

---
## 🚀 Deployment Steps (Manual + Automation)

### 1. Build Docker Image

docker build -t flask-app .


### 2. Create ECR Repository
- Created in AWS ECR

### 3. Authenticate Docker

aws ecr get-login-password | docker login


### 4. Push Image

docker tag flask-app:latest <ECR_URI>
docker push <ECR_URI>


### 5. ECS Deployment
- Create ECS Cluster
- Register Task Definition (port 5000)
- Create ECS Service (Fargate)

---
