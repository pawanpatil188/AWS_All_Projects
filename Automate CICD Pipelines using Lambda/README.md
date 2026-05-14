# 🚀 Automate CI/CD Pipelines using AWS Lambda

## 📌 Project Title
**Automate CI/CD Pipelines using Lambda**

---

## 🎯 Purpose

The purpose of this project is to automate software deployment workflows by integrating **AWS Lambda** with **AWS CodePipeline**.  

Whenever a trigger event occurs (such as code commit, file upload, or scheduled event), AWS Lambda automatically starts or manages the CI/CD pipeline, reducing manual effort and enabling faster deployments.

This project demonstrates how serverless automation can improve DevOps efficiency.

---

## 🧰 AWS Services Used

- **AWS Lambda** – Executes serverless automation logic
- **AWS CodePipeline** – Manages CI/CD workflow
- **IAM** – Provides secure access permissions
- **CloudWatch Logs** – Monitors Lambda execution
- **Amazon S3 / CodeCommit / GitHub** *(optional source)* – Source code repository

---

## 🏗️ Architecture

```text
Developer Pushes Code
        ↓
Source Repository (GitHub / CodeCommit / S3)
        ↓
AWS Lambda Triggered
        ↓
Lambda Starts CodePipeline
        ↓
Build Stage (CodeBuild)
        ↓
Deploy Stage (EC2 / S3 / Elastic Beanstalk)


📂 Project Workflow
Step 1️⃣ Create AWS CodePipeline


Step 2️⃣ Create IAM Role for Lambda
Go to IAM → Roles → Create Role

Step 3️⃣ Create Lambda Function

Step 4️⃣ Add Lambda Code

Step 5️⃣ Deploy Lambda

Step 6️⃣ Test Lambda Function

✅ Expected Output

Pipeline Triggered Successfully
And in AWS CodePipeline:


🔐 Security Best Practices
Use least privilege IAM roles

Restrict Lambda permissions

Enable CloudTrail logging

Encrypt pipeline artifacts in S3


🚀 Advantages
Fully automated deployments

No server management

Faster release cycle

Reduced manual intervention

Scalable and cost-effective


👩‍💻 Author
Manasi Patil
AWS DevOps / Cloud Project

