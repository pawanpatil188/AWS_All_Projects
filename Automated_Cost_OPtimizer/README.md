# 💰🚀 Automated Cost Optimizer (Manual Setup using AWS Console)

## 📌 Project Overview

This project demonstrates how to build a **cost optimization system** on Amazon Web Services that automatically stops idle EC2 instances using **AWS Lambda** and **CloudWatch (EventBridge)**.

👉 Unlike fully automated provisioning, this version is **configured manually using the AWS Console**, which helps in understanding each component clearly.

---

## 🎯 Objective

* Reduce AWS costs by stopping unused EC2 instances
* Learn **manual AWS setup process**
* Understand **event-driven automation**
* Gain hands-on experience with Lambda and CloudWatch

---

## 🏗️ Architecture

```text id="q6v8kq"
CloudWatch (Scheduled Rule)
            ↓
        AWS Lambda
            ↓
     Check EC2 Instances
            ↓
 Stop Idle Instances Automatically
```

---

## 🧰 AWS Services Used

* **AWS Lambda** → Executes cost optimization logic
* **Amazon CloudWatch / EventBridge** → Triggers Lambda on schedule
* **Amazon EC2** → Instances to monitor and stop
* **AWS IAM** → Provides permissions to Lambda

---

# ⚙️ Step-by-Step Manual Implementation

---

## 🧱 Step 1: Create IAM Role

1. Go to IAM → Roles → Create Role
2. Select **AWS Service → Lambda**
3. Attach policies:

   * `AmazonEC2FullAccess` *(for demo)*
   * `CloudWatchReadOnlyAccess`
   * `AWSLambdaBasicExecutionRole`
4. Give role name (e.g., `LambdaEC2CostOptimizerRole`)
5. Create role

👉 This allows Lambda to:

* Read EC2 details
* Access CloudWatch metrics
* Stop instances

---

## 🧱 Step 2: Create Lambda Function

1. Go to Lambda → Create Function
2. Choose **Author from scratch**
3. Runtime: Python 3.x
4. Attach the IAM role created earlier
5. Create function

---

## 🧱 Step 3: Add Cost Optimization Logic

* In Lambda code section, add logic to:

  * Fetch running EC2 instances
  * Check CPU utilization using CloudWatch
  * Identify idle instances
  * Stop those instances

👉 Deploy the function after adding code

---

## 🧱 Step 4: Create CloudWatch (EventBridge) Rule

1. Go to EventBridge → Create Rule
2. Choose **Schedule-based rule**
3. Set schedule expression:

   ```
   rate(1 hour)
   ```
4. Select target → Lambda function
5. Create rule

👉 This will trigger Lambda automatically every hour

---

## 🧱 Step 5: Tag EC2 Instances (Recommended)

To avoid stopping critical instances:

1. Go to EC2 → Select instance
2. Add tag:

   ```
   Key: AutoStop
   Value: True
   ```

👉 Configure Lambda logic to stop only tagged instances

---

## 🧪 Step 6: Testing

### Manual Test:

* Go to Lambda → Click **Test**

### Automatic Test:

* Wait for scheduled execution
* Observe EC2 instances

---

## 📊 Expected Output

| Instance Condition | Action  |
| ------------------ | ------- |
| Idle (low CPU)     | Stopped |
| Active usage       | Running |
| Not tagged         | Ignored |

---

## ⚠️ Common Issues & Fixes

| Issue                         | Cause                   | Solution                |
| ----------------------------- | ----------------------- | ----------------------- |
| Lambda not stopping instances | Missing IAM permissions | Update role policies    |
| No instances affected         | No tag applied          | Add AutoStop tag        |
| Rule not triggering           | Schedule misconfigured  | Verify EventBridge rule |
| Access denied errors          | IAM issue               | Attach correct policies |

---

## 🧠 Key Concepts Learned

* Manual AWS resource configuration
* Event-driven architecture
* Serverless computing
* Cost optimization techniques
* EC2 lifecycle management

---

## 📌 Conclusion

This project shows how to:

* Build a **cost-saving automation system manually**
* Understand each AWS component in detail
* Implement real-world cloud optimization strategies

---
