# 🚀 Scalable Web Application using NLB & Auto Scaling on AWS

## 📌 Project Overview

This project demonstrates how to build a **highly scalable and highly available web application** using **Auto Scaling** and a **Network Load Balancer (NLB)** on Amazon Web Services.

The architecture ensures that the application can handle varying traffic loads efficiently while maintaining low latency and high performance.

---

## 🎯 Objectives

* Design a **fault-tolerant architecture**
* Implement **automatic scaling** based on load
* Distribute traffic using a **high-performance load balancer**
* Achieve **high availability across multiple Availability Zones**

---

## 🧰 Services Used

* Amazon EC2 – Virtual servers to host the web application
* Amazon EC2 Auto Scaling – Automatically adjusts the number of instances
* Elastic Load Balancing (Network Load Balancer) – Distributes traffic
* Amazon VPC – Networking environment
* Amazon CloudWatch – Monitoring and scaling triggers

---

## 🏗️ Architecture Diagram

```
User
  ↓
Network Load Balancer (TCP Layer 4)
  ↓
Target Group
  ↓
Auto Scaling Group
  ↓
EC2 Instances (Apache Web Server)
```

---

## ⚙️ Key Features

* ⚡ **Low latency** using NLB (Layer 4 load balancing)
* 🔁 **Auto Scaling** based on CPU utilization
* 🌍 **Multi-AZ deployment** for high availability
* 💰 **Cost optimization** with dynamic scaling
* 🔄 **Fault tolerance** with automatic instance replacement

---

## 🧱 Step-by-Step Implementation

### 1️⃣ Create Launch Template

* Selected AMI: Amazon Linux 2023
* Instance Type: `t2.micro`
* Configured Security Group:

  * SSH (22) → My IP
  * HTTP (80) → Anywhere

### User Data Script:

```bash
#!/bin/bash
dnf update -y
dnf install -y httpd
systemctl start httpd
systemctl enable httpd

echo "<h1>Scalable App via NLB</h1>" > /var/www/html/index.html
echo "<h2>Instance: $(hostname)</h2>" >> /var/www/html/index.html
```

---

### 2️⃣ Create Target Group

* Target Type: Instances
* Protocol: TCP
* Port: 80
* Health Check: TCP

---

### 3️⃣ Create Network Load Balancer

* Type: Internet-facing
* Listener: TCP on port 80
* Attached Target Group
* Enabled Multi-AZ

---

### 4️⃣ Create Auto Scaling Group

* Linked with Launch Template
* Attached Target Group
* Configured subnets across multiple AZs

#### Scaling Configuration:

* Desired Capacity: 2
* Minimum: 1
* Maximum: 4

#### Scaling Policy:

* Target Tracking based on CPU utilization (60%)

---

## 🧪 Testing the Application

1. Access the application using NLB DNS
2. Refresh the page multiple times

   * Observe changing instance IDs → Load balancing works
3. Generate load using stress tool

   * Verify new instances are launched automatically

---

## 📊 Monitoring

* Used Amazon CloudWatch to:

  * Track CPU utilization
  * Trigger Auto Scaling events

---

## 🧠 Key Concepts Explained

### 🔹 Network Load Balancer (NLB)

* Operates at **Layer 4 (TCP/UDP)**
* Provides **ultra-low latency**
* Suitable for **high-performance applications**

### 🔹 Auto Scaling

* Dynamically adjusts EC2 instances
* Ensures:

  * High availability
  * Cost efficiency

### 🔹 Multi-AZ Deployment

* Distributes instances across zones
* Prevents single point of failure

---

## ⚠️ Challenges Faced

* Misconfiguration of instance type in launch template
* Incorrect security group rules (port issues)
* Instance requirement mismatch in Auto Scaling

---

## ✅ Solutions

* Defined instance type (`t2.micro`) explicitly
* Configured correct inbound rules (HTTP + SSH)
* Used launch template instead of manual overrides

---

## 🚀 Future Enhancements

* Add HTTPS using TLS listener
* Integrate CI/CD pipeline (CodePipeline)
* Deploy a dynamic app (Flask / Node.js)
* Use Application Load Balancer for HTTP routing

---

## 🎤 Interview Explanation (Short)

> “This project demonstrates a scalable architecture where a Network Load Balancer distributes incoming traffic across EC2 instances managed by an Auto Scaling Group. The system automatically scales based on CPU utilization and ensures high availability using multi-AZ deployment.”

---

## 📌 Conclusion

This project showcases the implementation of a **high-performance, scalable, and fault-tolerant web application architecture** using core AWS services, making it highly relevant for real-world cloud deployments and interviews.

---
