# 🚀 Containerized Node.js Application on AWS ECS (Fargate)

## 📌 Project Overview
This project demonstrates how to containerize a Node.js Express application using Docker and deploy it on AWS ECS using Amazon ECR and Fargate.

Deployment was performed using AWS services and boto3 automation scripts for hands-on cloud learning.

---

## 🎯 Objective
- Build Node.js Express application
- Containerize using Docker
- Push image to Amazon ECR
- Deploy on AWS ECS (Fargate)

---

## 🧰 AWS Services Used
- Amazon ECS (Elastic Container Service)
- Amazon ECR (Elastic Container Registry)
- AWS IAM (Execution Role)
- AWS CLI
- CloudWatch Logs (optional)

---

## 🏗️ Architecture
Node.js App → Docker Image → ECR → ECS Fargate → Running Container

---

## 🚀 Deployment Steps

### 1. Build Docker Image

docker build -t node-app .


### 2. Create ECR Repository
- Created repository in AWS ECR

### 3. Login to ECR

aws ecr get-login-password | docker login


### 4. Push Image

docker tag node-app:latest <ECR_URI>
docker push <ECR_URI>


### 5. ECS Deployment
- Create ECS Cluster
- Register Task Definition (port 3000)
- Create ECS Service (Fargate)

---

