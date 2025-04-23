"""
Definition of all cloud services available in the game.
Each service is stored as a dictionary with the required attributes.
"""

SERVICES = {
    # Compute Services
    "EC2_Instance": {
        "name": "EC2 Instance",
        "description": "Virtual server in the cloud.",
        "service_type": "Compute",
        "cost_per_hour": 0.10,
        "deploy_cost": 5,
        "region_availability": ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"],
        "dependencies": []
    },
    "Lambda_Function": {
        "name": "Lambda Function",
        "description": "Serverless compute service.",
        "service_type": "Compute",
        "cost_per_hour": 0.01,
        "deploy_cost": 2,
        "region_availability": ["us-east-1", "us-west-1", "us-west-2", "eu-west-1", "ap-southeast-1"],
        "dependencies": []
    },

    # Storage Services
    "S3_Bucket": {
        "name": "S3 Bucket",
        "description": "Object storage service.",
        "service_type": "Storage",
        "cost_per_hour": 0.02,
        "deploy_cost": 1,
        "region_availability": ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "eu-west-1", "eu-central-1", "ap-southeast-1", "ap-northeast-1"],
        "dependencies": []
    },
    "EBS_Volume": {
        "name": "EBS Volume",
        "description": "Block storage for EC2 instances.",
        "service_type": "Storage",
        "cost_per_hour": 0.08,
        "deploy_cost": 3,
        "region_availability": ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"],
        "dependencies": ["EC2 Instance"]
    },

    # Database Services
    "RDS_Database": {
        "name": "RDS Database",
        "description": "Relational database service.",
        "service_type": "Database",
        "cost_per_hour": 0.20,
        "deploy_cost": 15,
        "region_availability": ["us-east-1", "us-west-2", "eu-west-1", "eu-central-1", "ap-southeast-1"],
        "dependencies": ["VPC"]
    },
    "DynamoDB_Table": {
        "name": "DynamoDB Table",
        "description": "NoSQL database service.",
        "service_type": "Database",
        "cost_per_hour": 0.15,
        "deploy_cost": 8,
        "region_availability": ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "eu-west-1", "eu-central-1", "ap-southeast-1", "ap-northeast-1"],
        "dependencies": []
    },

    # Network Services
    "VPC": {
        "name": "VPC",
        "description": "Virtual private cloud network.",
        "service_type": "Network",
        "cost_per_hour": 0.01,
        "deploy_cost": 5,
        "region_availability": ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "eu-west-1", "eu-central-1", "ap-southeast-1", "ap-northeast-1"],
        "dependencies": []
    },
    "API_Gateway": {
        "name": "API Gateway",
        "description": "API creation and management service.",
        "service_type": "Network",
        "cost_per_hour": 0.12,
        "deploy_cost": 7,
        "region_availability": ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"],
        "dependencies": []
    },

    # Security Services
    "IAM_Policy": {
        "name": "IAM Policy",
        "description": "Identity and access management.",
        "service_type": "Security",
        "cost_per_hour": 0.00,
        "deploy_cost": 0,
        "region_availability": ["global"],
        "dependencies": []
    },
    "Security_Group": {
        "name": "Security Group",
        "description": "Virtual firewall for services.",
        "service_type": "Security",
        "cost_per_hour": 0.00,
        "deploy_cost": 0,
        "region_availability": ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "eu-west-1", "eu-central-1", "ap-southeast-1", "ap-northeast-1"],
        "dependencies": ["VPC"]
    },

    # Advanced Services
    "Elastic_Kubernetes_Service": {
        "name": "Elastic Kubernetes Service",
        "description": "Managed Kubernetes service for container orchestration.",
        "service_type": "Compute",
        "cost_per_hour": 0.30,
        "deploy_cost": 25,
        "region_availability": ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"],
        "dependencies": ["VPC"]
    },
    "SageMaker_Instance": {
        "name": "SageMaker Instance",
        "description": "Managed machine learning service.",
        "service_type": "AI/ML",
        "cost_per_hour": 0.50,
        "deploy_cost": 35,
        "region_availability": ["us-east-1", "us-west-2", "eu-west-1"],
        "dependencies": ["S3 Bucket"]
    },
    "CloudFront_Distribution": {
        "name": "CloudFront Distribution",
        "description": "Content delivery network service.",
        "service_type": "Network",
        "cost_per_hour": 0.10,
        "deploy_cost": 12,
        "region_availability": ["global"],
        "dependencies": ["S3 Bucket"]
    },
    "Elastic_Load_Balancer": {
        "name": "Elastic Load Balancer",
        "description": "Automatically distributes traffic across multiple targets.",
        "service_type": "Network",
        "cost_per_hour": 0.08,
        "deploy_cost": 10,
        "region_availability": ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"],
        "dependencies": ["VPC", "EC2 Instance"]
    }
}
