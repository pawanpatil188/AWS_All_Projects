# 🚀 Scalable Web Application using ALB & Auto Scaling on AWS

## 📌 Project Overview

This project demonstrates how to build a **highly available and scalable web application** using cloud infrastructure on AWS. The system automatically distributes incoming traffic across multiple servers and scales dynamically based on demand.

---

## 🎯 Objective

* Handle high user traffic without downtime
* Ensure high availability across multiple Availability Zones
* Automatically scale infrastructure based on load
* Implement secure and efficient traffic routing

---

## 🏗️ Architecture

User → Application Load Balancer → Target Group → EC2 Instances (Auto Scaling Group)

* The Load Balancer distributes incoming requests
* Auto Scaling Group dynamically adjusts the number of EC2 instances
* Each EC2 instance runs a web server (Apache)

---

## 🧰 Technologies & Services Used

* **AWS EC2** – Virtual servers hosting the application
* **Application Load Balancer (ALB)** – Distributes HTTP traffic
* **Auto Scaling Group (ASG)** – Automatically scales instances
* **Target Group** – Manages registered EC2 instances
* **Security Groups** – Controls inbound/outbound traffic
* **Amazon Linux 2023** – Operating system

---

## ⚙️ Implementation Steps

### 1️⃣ Launch EC2 Instance

* Created an EC2 instance using Amazon Linux
* Installed Apache web server
* Hosted a simple webpage displaying instance hostname

```bash
sudo yum update -y
sudo yum install httpd -y
sudo systemctl start httpd
sudo systemctl enable httpd
echo "Hello from $(hostname)" > /var/www/html/index.html
```

---

### 2️⃣ Create AMI (Machine Image)

* Created a reusable image of configured EC2
* Used for launching identical instances in Auto Scaling

---

### 3️⃣ Create Launch Template

* Defined instance configuration:

  * AMI
  * Instance type
  * Security group

---

### 4️⃣ Create Target Group

* Protocol: HTTP
* Port: 80
* Health check path: `/`

---

### 5️⃣ Create Application Load Balancer

* Internet-facing ALB
* Listener: HTTP (port 80)
* Forward traffic to target group

---

### 6️⃣ Create Auto Scaling Group

* Minimum instances: 2
* Maximum instances: 4
* Attached to ALB target group
* Distributed across multiple Availability Zones

---

### 7️⃣ Configure Scaling Policy

* Scale out when CPU > 70%
* Scale in when CPU < 30%

---

## 🔍 Testing & Validation

* Accessed ALB DNS in browser
* Observed responses from different EC2 instances
* Verified load balancing by refreshing page
* Monitored health checks in target group
* Ensured all instances became **Healthy**

---

## 🚨 Issues Faced & Solutions

### ❌ Issue: ALB Timeout

* Cause: Target group not attached / no registered instances
* Fix: Attached target group and registered EC2 instances

### ❌ Issue: Unhealthy Instances

* Cause: Apache not running or port blocked
* Fix:

  * Started HTTP service
  * Opened port 80 in security group

### ❌ Issue: Access Issue Detected

* Cause: Incorrect configuration in new instance
* Fix: Installed and configured Apache properly

---

## 📈 Results

* Successfully distributed traffic across multiple instances
* Achieved high availability and fault tolerance
* Implemented automatic scaling based on demand

---

## 🔐 Security Considerations

* Used SSH key-based authentication
* Restricted access using Security Groups
* Opened only required ports (22, 80)

---

## 🚀 Future Enhancements

* Add HTTPS using AWS Certificate Manager
* Integrate CI/CD pipeline (GitHub Actions)
* Containerize application using Docker
* Add monitoring with CloudWatch

---

## 🎯 Key Learnings

* Working of Layer 7 load balancing (ALB)
* Importance of health checks
* Auto Scaling concepts and policies
* Debugging real-world cloud deployment issues

---

## 🧠 Interview Explanation (Short)

> “I built a scalable web application using AWS ALB and Auto Scaling. The load balancer distributes incoming traffic across multiple EC2 instances, and the Auto Scaling Group dynamically adjusts capacity based on CPU utilization. I also debugged issues related to target group health checks and security configurations.”

---

## 📌 Conclusion

This project demonstrates how cloud infrastructure can be designed to handle scalability, reliability, and performance efficiently using AWS services.

---
