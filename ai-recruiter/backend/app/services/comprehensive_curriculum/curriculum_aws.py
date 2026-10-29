"""
curriculum_aws.py - Complete 8 Chapters Comprehensive Curriculum for AWS (Amazon Web Services).
Every chapter contains:
1. Detailed Concepts & In-Depth Explanation
2. Key Formulas, Rules & Architecture
3. Step-by-Step Solved Examples with working code and breakdown
4. Practice Questions with Answers & Explanations
5. Company Placement Technical Interview Questions & Answers
"""
from typing import List, Dict, Any

AWS_CHAPTERS: List[Dict[str, Any]] = [
    {
        "chapter_num": 1,
        "title": "AWS Global Infrastructure, Regions, Availability Zones & Core Compute (EC2)",
        "key_takeaways": "Understand Regions, AZs, Edge Locations, EC2 instance families (General, Compute, Memory, Storage), AMIs, and billing models.",
        "topics": [
            "AWS Global Footprint: Regions, Availability Zones, Local Zones & Points of Presence (Edge Locations)",
            "Amazon EC2 Instance Types: General Purpose (t3, m6), Compute (c6), Memory (r6), Storage (i3)",
            "Amazon Machine Images (AMI), User Data shell bootstrapping & EC2 lifecycle states",
            "EC2 Pricing Models: On-Demand, Savings Plans, Reserved Instances, Spot Instances & Dedicated Hosts",
            "AWS Instance Metadata Service (IMDSv2) security and temporary session credentials"
        ],
        "sections": {
            "concept": "AWS infrastructure is organized into geographic Regions containing isolated Availability Zones (AZs) connected via private ultra-low-latency fiber. Edge Locations power CloudFront CDN and Route 53. Amazon Elastic Compute Cloud (EC2) delivers resizable virtual machines. Compute instances are categorized by hardware architecture: 'c' for compute-heavy, 'r' for high-RAM databases, 'm' for general-purpose workloads, and 't' for burstable CPU with credit accumulation. Bootstrapping occurs via User Data scripts executed during first instance initialization.",
            "formulas": "1. EC2 Pricing: Total_Cost = Unit_Rate * Hours_Run + EBS_GB_Cost\n2. Burstable CPU Credits: Earn_Rate = Base_vCPU * 6 credits/hr (t3)\n3. Multi-AZ Inter-AZ Latency: Typical round-trip time <= 1.0 millisecond",
            "solved_examples": [
                {
                    "title": "Configuring Automated EC2 Web Server Bootstrapping with IMDSv2",
                    "difficulty": "Easy | AWS, Infosys, Wipro",
                    "problem": "Write an EC2 User Data bootstrap script that installs Nginx, enables systemd, and outputs instance metadata securely using IMDSv2.",
                    "step_by_step": [
                        "Step 1: Obtain an IMDSv2 session token using a PUT request with 6-hour TTL.",
                        "Step 2: Query the instance-id using the retrieved session token.",
                        "Step 3: Install and start Nginx web server.",
                        "Step 4: Generate an index.html displaying the dynamic instance ID for load balancer testing."
                    ],
                    "code_or_math": "#!/bin/bash\nyum update -y\nyum install -y nginx\nsystemctl start nginx\nsystemctl enable nginx\n# Fetch IMDSv2 Token\nTOKEN=$(curl -s -X PUT 'http://169.254.169.254/latest/api/token' -H 'X-aws-ec2-metadata-token-ttl-seconds: 21600')\nINSTANCE_ID=$(curl -s -H \"X-aws-ec2-metadata-token: $TOKEN\" http://169.254.169.254/latest/meta-data/instance-id)\necho \"<h1>Served from AWS EC2 Instance: $INSTANCE_ID</h1>\" > /usr/share/nginx/html/index.html"
                }
            ],
            "practice_questions": [
                {
                    "question": "Which EC2 pricing option offers the deepest discount (up to 90%) for fault-tolerant batch workloads that can withstand unexpected termination?",
                    "options": [
                        "On-Demand Instances",
                        "Spot Instances",
                        "Convertible Reserved Instances",
                        "Dedicated Hosts"
                    ],
                    "answer": "Spot Instances",
                    "explanation": "Spot Instances allow bidding on unused EC2 capacity at steep discounts (up to 90%), but AWS can reclaim the instance with a 2-minute interruption notice when demand surges."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon Web Services (AWS)",
                    "question": "Why is IMDSv2 significantly more secure than legacy IMDSv1 on EC2?",
                    "model_answer": "IMDSv1 used simple HTTP GET requests, making it highly vulnerable to Server-Side Request Forgery (SSRF) attacks where attackers trick web servers into fetching AWS credentials. IMDSv2 mandates a session-oriented flow using a PUT request with custom headers to acquire a secret token before querying metadata, completely neutralizing simple SSRF and open reverse proxy exploits.",
                    "interviewer_tip": "Cite protection against SSRF vulnerabilities directly."
                }
            ]
        }
    },
    {
        "chapter_num": 2,
        "title": "AWS S3 Storage Architecture, Lifecycle Policies & Data Lake Foundations",
        "key_takeaways": "Master S3 storage tiers (Standard, Infrequent Access, Glacier, Deep Archive), bucket versioning, replication, and S3 Select.",
        "topics": [
            "Amazon S3 Architecture: Buckets, Keys, Metadata, Prefixes & S3 Partitions",
            "Storage Classes: Standard, Intelligent-Tiering, Standard-IA, OneZone-IA, Glacier Flexible & Deep Archive",
            "Automated Lifecycle Management: Expiration rules, transition rules & noncurrent version expiration",
            "S3 Bucket Policies, Access Points, Cross-Region Replication (CRR) & Same-Region Replication (SRR)",
            "S3 Security: Block Public Access, SSE-S3 vs SSE-KMS vs SSE-C encryption, and Object Lock (WORM)"
        ],
        "sections": {
            "concept": "Amazon Simple Storage Service (S3) provides highly durable object storage. Data is partitioned across physical disks based on object key prefixes. S3 offers automated lifecycle transitions: moving objects from S3 Standard to Standard-IA after 30 days of inactivity, and to Glacier Deep Archive after 90 days for 80%+ cost reduction. S3 Object Lock enforces Write Once, Read Many (WORM) compliance. Encryption at rest is enforced by default using 256-bit Advanced Encryption Standard (AES-256).",
            "formulas": "1. Storage Tier Cost Comparison: Deep Archive ($0.00099/GB) is ~95% cheaper than S3 Standard ($0.023/GB)\n2. S3 Partition Performance: 3,500 PUT/POST/DELETE and 5,500 GET requests per second per prefix\n3. Lifecycle Savings: Savings = (Standard_Rate - Glacier_Rate) * GB * Months",
            "solved_examples": [
                {
                    "title": "Designing Cost-Optimized S3 Lifecycle Configuration for Media Archives",
                    "difficulty": "Medium | Amazon, Netflix, Hotstar",
                    "problem": "Write an S3 Lifecycle JSON policy that moves user uploads to Standard-IA after 30 days, Glacier after 90 days, and permanently deletes them after 365 days.",
                    "step_by_step": [
                        "Step 1: Define Rule with Filter prefix (or empty filter for entire bucket).",
                        "Step 2: Add Transition 1: Days=30, StorageClass=STANDARD_IA.",
                        "Step 3: Add Transition 2: Days=90, StorageClass=GLACIER.",
                        "Step 4: Add Expiration: Days=365 to clean up old objects automatically."
                    ],
                    "code_or_math": "{\n  'Rules': [\n    {\n      'ID': 'CostOptimizationArchive',\n      'Status': 'Enabled',\n      'Filter': {'Prefix': 'archives/'},\n      'Transitions': [\n        {'Days': 30, 'StorageClass': 'STANDARD_IA'},\n        {'Days': 90, 'StorageClass': 'GLACIER'}\n      ],\n      'Expiration': {'Days': 365}\n    }\n  ]\n}"
                }
            ],
            "practice_questions": [
                {
                    "question": "Which Amazon S3 storage class automatically optimizes storage costs by moving data between frequent and infrequent access tiers without performance impact or retrieval fees?",
                    "options": [
                        "S3 One Zone-IA",
                        "S3 Intelligent-Tiering",
                        "S3 Glacier Deep Archive",
                        "S3 Standard"
                    ],
                    "answer": "S3 Intelligent-Tiering",
                    "explanation": "S3 Intelligent-Tiering monitors access patterns and automatically moves objects between frequent, infrequent, and archive access tiers without operational overhead, retrieval fees, or performance loss."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon & Adobe",
                    "question": "How do you scale Amazon S3 performance to achieve 50,000+ GET requests per second for a high-traffic application?",
                    "model_answer": "S3 scales automatically to handle 5,500 GET requests per second per prefix. To achieve 55,000 GET requests per second, distribute object keys across at least 10 distinct prefixes (e.g. `bucket/folderA/`, `bucket/folderB/`, or using deterministic hashes). Additionally, integrate Amazon CloudFront in front of S3 to cache static content at edge locations, offloading up to 95% of S3 requests entirely.",
                    "interviewer_tip": "Mention CloudFront CDN caching as the primary real-world scaling mechanism."
                }
            ]
        }
    },
    {
        "chapter_num": 3,
        "title": "AWS VPC Deep Dive: Subnetting, Transit Gateway & Route 53 DNS",
        "key_takeaways": "Master public/private VPC design, Transit Gateways, VPC peering limits, Route 53 routing policies, and PrivateLink endpoints.",
        "topics": [
            "VPC core components: Internet Gateways (IGW), Egress-Only Internet Gateways, and NAT Gateways",
            "Multi-VPC Architecture: Hub-and-Spoke Transit Gateway vs VPC Peering mesh",
            "AWS PrivateLink (Interface VPC Endpoints) vs Gateway VPC Endpoints (S3 and DynamoDB)",
            "Amazon Route 53: Public vs Private Hosted Zones, DNS records (A, AAAA, CNAME, Alias)",
            "Route 53 Routing Policies: Latency-based, Geolocation, Geoproximity, Failover & Weighted"
        ],
        "sections": {
            "concept": "Amazon VPC allows configuring private software-defined networking. For multi-account and multi-VPC enterprise topologies, AWS Transit Gateway acts as a central cloud router connecting thousands of VPCs and on-premises networks in a scalable hub-and-spoke topology, replacing complex N*(N-1)/2 VPC peering meshes. Gateway VPC Endpoints provide free, high-throughput private connectivity to S3 and DynamoDB without routing over the public internet. Amazon Route 53 delivers global, resilient DNS resolution with integrated health checks and failover routing.",
            "formulas": "1. VPC Peering Complexity: Connections = N * (N - 1) / 2 (Transit Gateway reduces this to N attachments)\n2. Route 53 Health Check Interval: Standard = 30 seconds; Fast = 10 seconds\n3. Alias Records: Resolve directly to AWS resources (ALB, S3, CloudFront) with zero DNS lookup query fee",
            "solved_examples": [
                {
                    "title": "Configuring Route 53 Active-Passive Multi-Region DNS Failover",
                    "difficulty": "Medium | AWS, Cisco, Bloomberg",
                    "problem": "Configure automated DNS failover between primary region us-east-1 and secondary disaster recovery region us-west-2.",
                    "step_by_step": [
                        "Step 1: Create Route 53 Health Check monitoring the Primary ALB `/health` endpoint.",
                        "Step 2: Create Primary Record: Routing Policy = Failover, Failover Record Type = Primary, Associate Health Check.",
                        "Step 3: Create Secondary Record: Routing Policy = Failover, Failover Record Type = Secondary (points to DR ALB).",
                        "Step 4: When 3 consecutive health checks fail (30 seconds), Route 53 automatically withdraws the primary record and directs 100% of global DNS traffic to the secondary region."
                    ],
                    "code_or_math": "# Route 53 Failover Record Concept\nPrimary = {'record': 'api.company.com', 'target': 'alb-useast1.aws.com', 'type': 'PRIMARY', 'health_check': True}\nSecondary = {'record': 'api.company.com', 'target': 'alb-uswest2.aws.com', 'type': 'SECONDARY'}"
                }
            ],
            "practice_questions": [
                {
                    "question": "Which Route 53 record type allows mapping a root zone apex domain (e.g. `example.com`) directly to an AWS Application Load Balancer without performance penalty or CNAME restrictions?",
                    "options": [
                        "CNAME Record",
                        "Alias Record",
                        "TXT Record",
                        "PTR Record"
                    ],
                    "answer": "Alias Record",
                    "explanation": "Route 53 Alias records are an AWS-specific extension to DNS that allow mapping the root zone apex domain directly to AWS resources like ALBs, CloudFront distributions, and S3 website endpoints, which standard DNS CNAME records prohibit."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon & Cisco",
                    "question": "What is the difference between a VPC Gateway Endpoint and an Interface Endpoint (PrivateLink)?",
                    "model_answer": "Gateway Endpoints are route table entries used exclusively for Amazon S3 and DynamoDB at zero cost. Interface Endpoints (AWS PrivateLink) deploy an Elastic Network Interface (ENI) with a private IP address into your subnet, powered by AWS Hyperplane, supporting almost all AWS services and private third-party SaaS applications.",
                    "interviewer_tip": "Highlight that Gateway Endpoints are free, whereas Interface Endpoints incur hourly and GB-processed charges."
                }
            ]
        }
    },
    {
        "chapter_num": 4,
        "title": "AWS Managed Relational & NoSQL Databases: RDS, Aurora, DynamoDB & ElastiCache",
        "key_takeaways": "Master Amazon RDS Multi-AZ vs Read Replicas, Aurora cloud-native storage engine, DynamoDB single-digit millisecond NoSQL, and Redis caching.",
        "topics": [
            "Amazon RDS: Multi-AZ Synchronous Replication (High Availability) vs Read Replicas (Read Scaling)",
            "Amazon Aurora: Log-structured distributed storage across 3 AZs (6 copies) and global databases",
            "Amazon DynamoDB: Partition keys, Sort keys, Global Secondary Indexes (GSI) & Local Secondary Indexes (LSI)",
            "DynamoDB Capacity Modes: Provisioned (with Auto-Scaling) vs On-Demand (Pay-per-request)",
            "Amazon ElastiCache (Redis / Memcached): Cache-Aside vs Write-Through caching patterns"
        ],
        "sections": {
            "concept": "AWS provides specialized database engines. Amazon RDS automates provisioning, patching, and backups. RDS Multi-AZ synchronously replicates commits to a standby instance in another AZ for automatic disaster failover. Read Replicas use asynchronous replication for scaling read-heavy queries. Amazon Aurora decouples compute from storage, replicating 6 copies of data across 3 AZs at the disk block level, delivering 5x MySQL throughput. Amazon DynamoDB is a fully managed NoSQL key-value database guaranteeing single-digit millisecond latency at any scale. ElastiCache Redis provides sub-millisecond in-memory caching.",
            "formulas": "1. DynamoDB Read Capacity Units (RCU): 1 RCU = 1 Strongly Consistent read (up to 4 KB) or 2 Eventually Consistent reads\n2. DynamoDB Write Capacity Units (WCU): 1 WCU = 1 write (up to 1 KB)\n3. Aurora Quorum Model: 4/6 write quorum, 3/6 read quorum across 3 AZs",
            "solved_examples": [
                {
                    "title": "Calculating DynamoDB RCU and WCU Provisioning for High-Throughput API",
                    "difficulty": "Medium | Amazon, Swiggy, Uber",
                    "problem": "Calculate required RCUs and WCUs for an app performing 500 writes/sec (item size 2.5 KB) and 2,000 eventually consistent reads/sec (item size 3.5 KB).",
                    "step_by_step": [
                        "Step 1: Write calculation: Item size 2.5 KB rounds up to 3 KB. 1 WCU = 1 KB write/sec. Required WCU = 500 * 3 = 1,500 WCUs.",
                        "Step 2: Read calculation: Item size 3.5 KB rounds up to 4 KB. 1 RCU = 4 KB strongly consistent read/sec. Eventually consistent uses 0.5 RCU per 4 KB.",
                        "Step 3: Required RCU = 2,000 * 0.5 = 1,000 RCUs.",
                        "Step 4: Total provisioned throughput: 1,500 WCU and 1,000 RCU."
                    ],
                    "code_or_math": "import math\ndef calc_dynamodb(writes, write_kb, reads, read_kb):\n    wcus = writes * math.ceil(write_kb)\n    rcus = reads * (math.ceil(read_kb / 4.0) * 0.5) # Eventually consistent\n    return wcus, rcus\nprint('DynamoDB Capacity:', calc_dynamodb(500, 2.5, 2000, 3.5))"
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the primary architectural purpose of deploying an Amazon RDS database in a Multi-AZ configuration?",
                    "options": [
                        "To scale out read query throughput across multiple regions",
                        "To provide synchronous high-availability failover in the event of an availability zone outage",
                        "To reduce database monthly hosting costs by 50%",
                        "To convert SQL queries into NoSQL JSON documents"
                    ],
                    "answer": "To provide synchronous high-availability failover in the event of an availability zone outage",
                    "explanation": "RDS Multi-AZ synchronously replicates all database writes to a standby replica in a different physical Availability Zone. If the primary crashes or the AZ experiences an outage, RDS triggers an automated DNS failover to the standby in under 60 seconds."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon & Microsoft",
                    "question": "What is the Cache-Aside (Lazy Loading) pattern in Amazon ElastiCache, and how does it handle cache misses?",
                    "model_answer": "In Cache-Aside, the application first queries the Redis cache. On a Cache Hit, it returns the cached data immediately. On a Cache Miss, the application queries the underlying database (e.g. RDS Aurora), writes the fetched record into Redis with an appropriate Time-To-Live (TTL), and returns the response. This ensures only frequently requested data consumes memory.",
                    "interviewer_tip": "Always mention setting a TTL to avoid stale data accumulating indefinitely."
                }
            ]
        }
    },
    {
        "chapter_num": 5,
        "title": "AWS Serverless Ecosystem: Lambda, API Gateway, SQS, SNS & EventBridge",
        "key_takeaways": "Master building decoupled, event-driven serverless architectures with Lambda, REST/HTTP APIs, SQS queues, SNS topics, and EventBridge buses.",
        "topics": [
            "AWS Lambda internals: Memory sizing, ephemeral storage (/tmp), timeout limits & VPC ENI cold starts",
            "Amazon API Gateway: REST APIs vs HTTP APIs vs WebSockets with Cognito JWT authorizers",
            "Amazon SQS (Simple Queue Service): Standard vs FIFO queues, visibility timeout & dead-letter queues",
            "Amazon SNS (Simple Notification Service): Pub/Sub fanout architecture and message filtering",
            "Amazon EventBridge: Serverless event bus, schema registry & SaaS third-party event routing"
        ],
        "sections": {
            "concept": "The AWS Serverless ecosystem enables fully managed, pay-per-use architectures. Amazon API Gateway acts as the secure entry door, routing client traffic to backend Lambda functions. Amazon SQS provides pull-based asynchronous queuing for decoupling workloads. Standard SQS offers nearly unlimited throughput with at-least-once delivery; FIFO queues guarantee exact first-in-first-out order with deduplication. Amazon SNS provides push-based Pub/Sub broadcasting. Amazon EventBridge routes events from AWS services and external SaaS systems (Datadog, Zendesk) based on JSON pattern rules.",
            "formulas": "1. Lambda CPU Allocation: CPU scales linearly with RAM (1,769 MB RAM = exactly 1 full vCPU)\n2. SQS Visibility Timeout Rule: VisibilityTimeout >= 6 * Lambda_Function_Timeout\n3. SQS FIFO Throughput: Up to 3,000 msgs/sec with batching (300 msgs/sec standard without batching)",
            "solved_examples": [
                {
                    "title": "Architecting an Asynchronous Order Processing System with Fanout",
                    "difficulty": "Medium | Amazon, Uber, Walmart",
                    "problem": "When a customer places an order, three downstream microservices must process the event simultaneously: Payment, Inventory, and Notification.",
                    "step_by_step": [
                        "Step 1: Order API writes event to a central Amazon SNS Topic: `order-placed-topic`.",
                        "Step 2: Create three distinct SQS Queues: `payment-queue`, `inventory-queue`, and `notification-queue`.",
                        "Step 3: Subscribe all three SQS queues to the SNS Topic (Pub/Sub Fanout pattern).",
                        "Step 4: Each microservice's Lambda function polls its dedicated SQS queue independently. If payment processing fails, inventory and notification remain unaffected.",
                        "Step 5: Attach Dead Letter Queues (DLQs) to capture malformed orders after 3 failed retries."
                    ],
                    "code_or_math": "# SNS Fanout Architectural Mapping\nsns_topic = 'order-created'\nsubscribers = ['sqs-payment-service', 'sqs-inventory-service', 'sqs-email-notifier']\nprint(f'Publishing to {sns_topic} automatically delivers message to all {len(subscribers)} independent queues.')"
                }
            ],
            "practice_questions": [
                {
                    "question": "What happens when an Amazon SQS consumer receives a message and begins processing it?",
                    "options": [
                        "The message is permanently deleted from the queue immediately",
                        "The message remains in the queue but becomes invisible to other consumers for the duration of the Visibility Timeout",
                        "The queue pauses all other incoming messages",
                        "The message is forwarded to all AWS users"
                    ],
                    "answer": "The message remains in the queue but becomes invisible to other consumers for the duration of the Visibility Timeout",
                    "explanation": "During the Visibility Timeout, SQS hides the message from other polling consumers. If the worker successfully processes it, it calls `DeleteMessage`. If the worker crashes or times out, the message becomes visible again for another worker to retry."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon & Salesforce",
                    "question": "Why should you always configure a Dead Letter Queue (DLQ) for asynchronous Lambda invocations and SQS queues?",
                    "model_answer": "In distributed event systems, a malformed message ('poison pill') can cause worker functions to crash repeatedly. Without a DLQ, the message triggers endless retries, wasting compute budget and potentially blocking FIFO queues. A DLQ catches messages after a designated maximum receive count (e.g. 3 attempts), allowing engineers to alert on DLQ metrics, inspect payloads, fix bugs, and redrive messages safely.",
                    "interviewer_tip": "Mention the term 'Poison Pill'\u2014interviewers recognize it as practical operational experience."
                }
            ]
        }
    },
    {
        "chapter_num": 6,
        "title": "AWS Security, Governance, Compliance & Key Management (KMS)",
        "key_takeaways": "Master AWS IAM, Organization Service Control Policies (SCPs), AWS KMS, AWS WAF, and automated compliance auditing.",
        "topics": [
            "AWS IAM Policies: Identity-based vs Resource-based policies (S3 Bucket Policies, KMS Key Policies)",
            "AWS Organizations & Service Control Policies (SCPs) for enterprise governance guardrails",
            "AWS KMS: Customer Managed Keys (CMK), AWS Managed Keys & KMS Key Policies",
            "AWS WAF (Web Application Firewall): SQL injection, XSS protection & rate-limiting rules",
            "Security monitoring: AWS CloudTrail, Amazon GuardDuty (AI threat detection) & AWS Security Hub"
        ],
        "sections": {
            "concept": "AWS enforces security through layered defense-in-depth. AWS Organizations groups accounts into Organizational Units (OUs) governed by Service Control Policies (SCPs) that set maximum permission guardrails. AWS Key Management Service (KMS) uses FIPS 140-2 validated hardware security modules (HSMs) to manage cryptographic keys. AWS WAF inspects HTTP traffic at CloudFront, ALB, or API Gateway, blocking malicious bots, SQL injection, and DDoS attempts. Amazon GuardDuty uses machine learning to monitor VPC flow logs and CloudTrail events for compromised credentials or crypto-mining malware.",
            "formulas": "1. KMS Request Rate Limits: 10,000 requests/sec per region with automatic burst scaling\n2. AWS WAF Rate Limiting: Evaluates requests over 5-minute rolling window (e.g. max 1,000 req/IP)\n3. CloudTrail Delivery Latency: Logs delivered to S3 typically within 15 minutes",
            "solved_examples": [
                {
                    "title": "Writing an AWS WAF Rate-Limiting Rule to Defend Against Login Brute-Force",
                    "difficulty": "Medium | AWS, Cloudflare, Akamai",
                    "problem": "Create an AWS WAF rule that blocks any client IP making more than 100 requests to `/api/v1/auth/login` within a 5-minute window.",
                    "step_by_step": [
                        "Step 1: Define WAF Rule of type Rate-based Rule.",
                        "Step 2: Set Rate limit = 100 requests per 5 minutes.",
                        "Step 3: Add scope-down statement: URI Path starts with `/api/v1/auth/login`.",
                        "Step 4: Set Action = Block with custom HTTP 429 Too Many Requests response.",
                        "Step 5: Attach WebACL to the Application Load Balancer."
                    ],
                    "code_or_math": "# WAF JSON Rule Definition Concept\nwaf_rule = {\n  'Name': 'BlockBruteForceLogin',\n  'Priority': 1,\n  'Action': {'Block': {}},\n  'Statement': {\n    'RateBasedStatement': {\n      'Limit': 100,\n      'AggregateKeyType': 'IP',\n      'ScopeDownStatement': {'ByteMatchStatement': {'SearchString': '/api/v1/auth/login'}}\n    }\n  }\n}"
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the primary function of an AWS Organizations Service Control Policy (SCP)?",
                    "options": [
                        "To assign IAM user passwords and manage SSH key pairs",
                        "To set fine-grained maximum permission boundaries and guardrails for accounts in an organization",
                        "To inspect inbound database SQL queries for syntax errors",
                        "To bill individual credit cards per virtual machine"
                    ],
                    "answer": "To set fine-grained maximum permission boundaries and guardrails for accounts in an organization",
                    "explanation": "Service Control Policies (SCPs) define the maximum available permissions for member accounts in an AWS Organization. Even the root user of a member account cannot perform an action denied by an SCP."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon & Goldman Sachs",
                    "question": "What is the difference between AWS CloudTrail and Amazon CloudWatch?",
                    "model_answer": "AWS CloudTrail audits API calls and management actions across your AWS account (answering 'Who made what API call, from what IP, at what time?'). Amazon CloudWatch monitors performance metrics and operational logs (answering 'What is the CPU utilization, memory pressure, and HTTP 5xx error rate of my application?').",
                    "interviewer_tip": "Remember: CloudTrail is for API governance and security auditing; CloudWatch is for performance metrics and operational observability."
                }
            ]
        }
    },
    {
        "chapter_num": 7,
        "title": "AWS Infrastructure as Code (IaC) & Automated DevOps with CloudFormation & CDK",
        "key_takeaways": "Master declarative infrastructure with AWS CloudFormation templates, drift detection, and programmatic infrastructure with AWS CDK.",
        "topics": [
            "Infrastructure as Code (IaC) principles: Version control, repeatability, drift detection & immutability",
            "AWS CloudFormation: Stacks, Resources, Parameters, Outputs, Intrinsic Functions (!Ref, !Sub, !GetAtt)",
            "CloudFormation Change Sets, Rollbacks, and Deletion Policies (Retain vs Delete)",
            "AWS Cloud Development Kit (CDK): Defining cloud resources programmatically in TypeScript and Python",
            "AWS CodePipeline, CodeBuild & CodeDeploy for automated cloud CI/CD release engineering"
        ],
        "sections": {
            "concept": "Infrastructure as Code (IaC) treats infrastructure provisioning with the same engineering rigor as application software. AWS CloudFormation provisions stacks of AWS resources declaratively from YAML/JSON templates. If any resource fails during creation, CloudFormation executes an automatic rollback, leaving the environment in a clean state. Change Sets allow previewing the exact proposed modifications before applying changes to production. The AWS Cloud Development Kit (CDK) elevates IaC by allowing developers to define cloud architectures using modern object-oriented programming languages like TypeScript and Python.",
            "formulas": "1. CloudFormation Stack Limits: Up to 500 resources per template (use Nested Stacks to scale)\n2. Drift Detection: Identifies differences between deployed AWS resources and template definitions\n3. CDK Synthesis: CDK Code -> CloudFormation Template -> CloudFormation Engine -> Live AWS Resources",
            "solved_examples": [
                {
                    "title": "Writing a Production CloudFormation Template with Dynamic S3 and KMS Resources",
                    "difficulty": "Medium | AWS, Cognizant, Infosys",
                    "problem": "Write a clean YAML CloudFormation template that provisions an encrypted S3 bucket with versioning and deletion protection.",
                    "step_by_step": [
                        "Step 1: Declare AWSTemplateFormatVersion: '2010-09-09'.",
                        "Step 2: Add Parameters for EnvironmentName (dev, staging, prod).",
                        "Step 3: Define AWS::S3::Bucket with BucketEncryption set to AES256.",
                        "Step 4: Set DeletionPolicy: Retain to prevent accidental bucket deletion during stack removal.",
                        "Step 5: Output the Bucket ARN using !GetAtt."
                    ],
                    "code_or_math": "AWSTemplateFormatVersion: '2010-09-09'\nDescription: Secure Enterprise S3 Bucket\nParameters:\n  Env:\n    Type: String\n    Default: prod\nResources:\n  SecureDataBucket:\n    Type: AWS::S3::Bucket\n    DeletionPolicy: Retain\n    Properties:\n      BucketName: !Sub 'company-data-${Env}-${AWS::AccountId}'\n      VersioningConfiguration:\n        Status: Enabled\n      BucketEncryption:\n        ServerSideEncryptionConfiguration:\n          - ServerSideEncryptionByDefault:\n              SSEAlgorithm: AES256\nOutputs:\n  BucketArn:\n    Value: !GetAtt SecureDataBucket.Arn"
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the purpose of a CloudFormation Change Set?",
                    "options": [
                        "To change the AWS account owner password",
                        "To preview how proposed template changes will impact running resources before executing the update",
                        "To permanently erase previous stack backups",
                        "To convert Python CDK code into Java"
                    ],
                    "answer": "To preview how proposed template changes will impact running resources before executing the update",
                    "explanation": "A Change Set allows you to preview the additions, modifications, or deletions of resources that will occur before applying an update to an existing CloudFormation production stack, preventing unexpected service interruptions."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon & Atlassian",
                    "question": "Why is AWS CDK often preferred over raw CloudFormation YAML/JSON for complex architectures?",
                    "model_answer": "AWS CDK allows using real programming languages (TypeScript, Python) with full IDE code completion, compile-time type checking, unit testing frameworks (Jest/pytest), and high-level Constructs. A single line of CDK code can provision a production-ready VPC or ECS cluster with dozens of automatically configured subnets, route tables, and security groups that would require 500+ lines of raw CloudFormation YAML.",
                    "interviewer_tip": "Mention CDK Constructs (L1, L2, L3) to demonstrate deep hands-on expertise."
                }
            ]
        }
    },
    {
        "chapter_num": 8,
        "title": "AWS Solutions Architect Placement Case Studies & System Design Interviews",
        "key_takeaways": "Master real-world AWS system design interview problems: resilient e-commerce, global multi-region architectures, and media pipelines.",
        "topics": [
            "Architecture Design 1: Highly scalable global SaaS platform with multi-tenant data isolation",
            "Architecture Design 2: Financial payment gateway handling ACID transactions with sub-second latency",
            "Cost Optimization Case Study: Rightsizing compute, storage tiering, and saving $500,000/year",
            "Troubleshooting Production Outages: Diagnosing ALB 502/504 errors, database lock contention & throttling",
            "FAANG AWS Solutions Architect placement questions, scoring criteria, and trade-off matrices"
        ],
        "sections": {
            "concept": "In campus placement interviews for AWS Cloud Solutions Architect and Cloud DevOps Engineer roles, candidates are evaluated on end-to-end system design following the AWS Well-Architected Framework. You must explain trade-offs between latency, consistency, availability, and cost. When diagnosing production outages, systematically trace traffic: DNS (Route 53) -> CDN (CloudFront) -> Load Balancer (ALB) -> Compute (EC2/ECS/Lambda) -> Database (Aurora/DynamoDB). HTTP 502 Bad Gateway indicates the backend app crashed or dropped connections; HTTP 504 Gateway Timeout indicates backend query latency exceeded the ALB idle timeout.",
            "formulas": "1. Database Connection Pool Formula: Connections = ((vCPU * 2) + Effective_Spindle_Count)\n2. ALB Target Response Time Metric: TargetResponseTime <= 0.200 seconds\n3. CloudFront Edge Cache Optimization: Target Cache Hit Ratio >= 90%",
            "solved_examples": [
                {
                    "title": "Designing a Global Resilient Banking Payment Gateway on AWS",
                    "difficulty": "Hard | Amazon, JPMorgan Chase, PayPal",
                    "problem": "Design a PCI-DSS compliant banking payment platform with 99.999% availability, zero transaction loss, and sub-second response times.",
                    "step_by_step": [
                        "Step 1: Network: Multi-AZ VPC across 3 AZs with public ALBs, private containerized ECS Fargate app tier, and isolated database subnets.",
                        "Step 2: Database: Amazon Aurora PostgreSQL Global Database with Multi-Master or rapid automated cross-region storage replication.",
                        "Step 3: Security: AWS WAF inspecting all inbound HTTP traffic, AWS KMS Customer Managed Keys for column-level envelope encryption, and Secrets Manager for automated database credential rotation.",
                        "Step 4: Caching & Resilience: Redis ElastiCache cluster with Multi-AZ failover for idempotent transaction token verification.",
                        "Step 5: Observability: CloudWatch Container Insights and AWS X-Ray distributed tracing across all microservice API calls."
                    ],
                    "code_or_math": "# Architectural Blueprint Check\npayment_arch = {\n    'VPC': '3 AZ Public/Private/DB',\n    'Compute': 'ECS Fargate Containers',\n    'DB': 'Amazon Aurora Multi-AZ',\n    'Cache': 'ElastiCache Redis Cluster',\n    'Security': 'WAF + KMS CMK + Secrets Manager'\n}\nprint('Architecture Compliant with AWS Well-Architected Pillars:', len(payment_arch) == 5)"
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the most likely cause of an HTTP 504 Gateway Timeout error returned by an AWS Application Load Balancer?",
                    "options": [
                        "The client entered the wrong website password",
                        "The target backend instance failed to respond to the load balancer within the configured idle timeout period",
                        "The Amazon S3 bucket has versioning disabled",
                        "The domain name registration has expired"
                    ],
                    "answer": "The target backend instance failed to respond to the load balancer within the configured idle timeout period",
                    "explanation": "An HTTP 504 Gateway Timeout error indicates that the Application Load Balancer successfully forwarded the request to the backend target (EC2, ECS, or Lambda), but the backend failed to return a response before the ALB idle timeout (default 60 seconds) elapsed."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon & Google",
                    "question": "How do you systematically debug an Application Load Balancer returning HTTP 502 Bad Gateway errors?",
                    "model_answer": "HTTP 502 indicates the ALB connected to the target, but received an unexpected or malformed response. Systematic debugging steps: 1) Check ALB Target Group health checks to verify if instances are healthy; 2) Review web server error logs (Nginx/Node.js/Tomcat) to check for application crashes or unhandled exceptions; 3) Verify the backend's keep-alive timeout is configured higher than the ALB's idle timeout (otherwise the target may close the connection prematurely); 4) Confirm backend security groups permit inbound traffic from the ALB's security group on the application port.",
                    "interviewer_tip": "Highlight the keep-alive timeout mismatch\u2014it is one of the most common real-world causes of intermittent 502 errors."
                }
            ]
        }
    }
]
