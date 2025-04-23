"""
Definition of all artifacts available in the game.
Each artifact is stored as a dictionary with the required attributes.
"""

ARTIFACTS = {
    # Basic Scanner Artifacts
    "S3_Scanner": {
        "name": "S3 Scanner",
        "description": "Scans and analyzes S3 buckets for vulnerabilities.",
        "artifact_type": "Scanner",
        "aws_service": "Amazon S3",
        "cost": 10,
        "power": 1
    },
    "EC2_Inspector": {
        "name": "EC2 Inspector",
        "description": "Checks EC2 instances for security issues.",
        "artifact_type": "Scanner",
        "aws_service": "Amazon EC2",
        "cost": 15,
        "power": 2
    },
    "RDS_Analyzer": {
        "name": "RDS Analyzer",
        "description": "Analyzes database configurations for vulnerabilities.",
        "artifact_type": "Scanner",
        "aws_service": "Amazon RDS",
        "cost": 20,
        "power": 2
    },

    # Network Artifacts
    "VPC_Tracer": {
        "name": "VPC Tracer",
        "description": "Traces network traffic through Virtual Private Clouds.",
        "artifact_type": "Network",
        "aws_service": "Amazon VPC",
        "cost": 25,
        "power": 3
    },
    "Route53_Resolver": {
        "name": "Route53 Resolver",
        "description": "Resolves domain names and finds hidden endpoints.",
        "artifact_type": "Network",
        "aws_service": "Amazon Route 53",
        "cost": 30,
        "power": 3
    },

    # Security Artifacts
    "IAM_Auditor": {
        "name": "IAM Auditor",
        "description": "Audits IAM permissions and finds policy flaws.",
        "artifact_type": "Security",
        "aws_service": "AWS IAM",
        "cost": 35,
        "power": 4
    },
    "GuardDuty_Lens": {
        "name": "GuardDuty Lens",
        "description": "Detects threats and suspicious activities.",
        "artifact_type": "Security",
        "aws_service": "Amazon GuardDuty",
        "cost": 40,
        "power": 4
    },
    "WAF_Shield": {
        "name": "WAF Shield",
        "description": "Protects against web attacks and intrusions.",
        "artifact_type": "Security",
        "aws_service": "AWS WAF",
        "cost": 50,
        "power": 5
    },

    # Compute Artifacts
    "Lambda_Invoker": {
        "name": "Lambda Invoker",
        "description": "Invokes Lambda functions safely for testing.",
        "artifact_type": "Compute",
        "aws_service": "AWS Lambda",
        "cost": 20,
        "power": 2
    },
    "ECS_Orchestrator": {
        "name": "ECS Orchestrator",
        "description": "Controls container deployments and scaling.",
        "artifact_type": "Compute",
        "aws_service": "Amazon ECS",
        "cost": 35,
        "power": 3
    },

    # Storage Artifacts
    "Glacier_Drill": {
        "name": "Glacier Drill",
        "description": "Retrieves archived data from Glacier storage.",
        "artifact_type": "Storage",
        "aws_service": "Amazon S3 Glacier",
        "cost": 30,
        "power": 3
    },
    "EFS_Mount": {
        "name": "EFS Mount",
        "description": "Mounts shared file systems for data analysis.",
        "artifact_type": "Storage",
        "aws_service": "Amazon EFS",
        "cost": 25,
        "power": 2
    },

    # Database Artifacts
    "DynamoDB_Query_Engine": {
        "name": "DynamoDB Query Engine",
        "description": "Performs complex queries on NoSQL data.",
        "artifact_type": "Database",
        "aws_service": "Amazon DynamoDB",
        "cost": 35,
        "power": 3
    },
    "Aurora_Analyzer": {
        "name": "Aurora Analyzer",
        "description": "Analyzes and optimizes Aurora databases.",
        "artifact_type": "Database",
        "aws_service": "Amazon Aurora",
        "cost": 45,
        "power": 4
    },

    # Legendary Artifacts
    "CloudFormation_Architect": {
        "name": "CloudFormation Architect",
        "description": "Reverse engineers cloud infrastructure and creates templates.",
        "artifact_type": "IaC",
        "aws_service": "AWS CloudFormation",
        "cost": 100,
        "power": 8
    },
    "Console_Master_Key": {
        "name": "Console Master Key",
        "description": "Grants elevated access to AWS console functions.",
        "artifact_type": "Security",
        "aws_service": "AWS Management Console",
        "cost": 150,
        "power": 9
    },
    "Quantum_Decryptor": {
        "name": "Quantum Decryptor",
        "description": "Uses quantum computing to break encryption.",
        "artifact_type": "Security",
        "aws_service": "AWS Key Management Service",
        "cost": 200,
        "power": 10
    },

    # Additional Artifacts
    "VPC_Flow_Log_Analyzer": {
        "name": "VPC Flow Log Analyzer",
        "description": "Analyzes VPC flow logs to trace network connections and detect anomalies.",
        "artifact_type": "Network",
        "aws_service": "Amazon VPC",
        "cost": 45,
        "power": 5
    },
    "CloudWatch_Metrics_Dashboard": {
        "name": "CloudWatch Metrics Dashboard",
        "description": "Visualizes CloudWatch metrics to diagnose performance issues and resource utilization.",
        "artifact_type": "Monitoring",
        "aws_service": "Amazon CloudWatch",
        "cost": 40,
        "power": 4
    },
    "IAM_Access_Analyzer": {
        "name": "IAM Access Analyzer",
        "description": "Identifies unintended resource access and validates security policies.",
        "artifact_type": "Security",
        "aws_service": "AWS IAM Access Analyzer",
        "cost": 55,
        "power": 6
    },
    "Log_Analyzer_Toolkit": {
        "name": "Log Analyzer Toolkit",
        "description": "A suite of tools for parsing and analyzing various system and application logs.",
        "artifact_type": "Investigation",
        "aws_service": None,
        "cost": 30,
        "power": 3
    },
    "Digital_Shield_Generator": {
        "name": "Digital Shield Generator",
        "description": "Creates a protective barrier against digital attacks.",
        "artifact_type": "Defense",
        "aws_service": "AWS Shield Advanced",
        "cost": 75,
        "power": 7
    },
    "Network_Pulse_Emitter": {
        "name": "Network Pulse Emitter",
        "description": "Disrupts hostile connections and network intrusions.",
        "artifact_type": "Offense",
        "aws_service": "AWS Network Firewall",
        "cost": 80,
        "power": 7
    },
    "Vulnerability_Scanner_Pro": {
        "name": "Vulnerability Scanner Pro",
        "description": "Advanced scanning tool that identifies system weaknesses.",
        "artifact_type": "Scanner",
        "aws_service": "Amazon Inspector",
        "cost": 65,
        "power": 6
    },
    "Backup_Restore_Module": {
        "name": "Backup & Restore Module",
        "description": "Quickly restores service health from backup snapshots.",
        "artifact_type": "Recovery",
        "aws_service": "AWS Backup",
        "cost": 50,
        "power": 5
    }
}
