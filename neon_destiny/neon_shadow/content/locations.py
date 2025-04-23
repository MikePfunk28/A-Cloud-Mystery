"""
Definition of all locations available in the game.
Each location is stored as a dictionary with the required attributes.
"""

LOCATIONS = {
    # Cloud City Region - Main Hub
    "Cloud_City": {
        "name": "Cloud City",
        "description": "The central hub for cloud engineers and digital nomads. Towering server racks form the cityscape.",
        "region": "us-east-1",
        "connections": ["Serverless Valley", "Database District", "Security Perimeter"],
        "difficulty": 1,
        "events": ["welcome_to_cloud_city", "artifact_discovery"]
    },

    "Serverless_Valley": {
        "name": "Serverless Valley",
        "description": "A vast landscape where computation resources materialize on demand. Lambda functions flow like rivers.",
        "region": "us-east-1",
        "connections": ["Cloud City", "Edge Outpost", "Function Junction"],
        "difficulty": 2,
        "events": ["serverless_challenge"]
    },

    "Database_District": {
        "name": "Database District",
        "description": "Rows of data warehouses and database servers line the streets. Queries flow through the air.",
        "region": "us-east-1",
        "connections": ["Cloud City", "Analytics Archipelago", "Cache Cove"],
        "difficulty": 2,
        "events": ["database_breach"]
    },

    "Security_Perimeter": {
        "name": "Security Perimeter",
        "description": "The defensive wall surrounding Cloud City. Firewalls and security groups monitor all traffic.",
        "region": "us-east-1",
        "connections": ["Cloud City", "Identity Federation", "Network Nexus"],
        "difficulty": 3,
        "events": []
    },

    # US-WEST Region
    "Edge_Outpost": {
        "name": "Edge Outpost",
        "description": "A frontier outpost at the edge of the network. CDN caches and edge computing nodes operate here.",
        "region": "us-west-2",
        "connections": ["Serverless Valley", "Container Canyon"],
        "difficulty": 3,
        "events": []
    },

    "Container_Canyon": {
        "name": "Container Canyon",
        "description": "Deep ravines filled with container orchestration systems. Docker images flow down the canyon walls.",
        "region": "us-west-2",
        "connections": ["Edge Outpost", "Kubernetes Plateau"],
        "difficulty": 4,
        "events": []
    },

    "Kubernetes_Plateau": {
        "name": "Kubernetes Plateau",
        "description": "A vast elevated plain where container pods roam freely. Control planes monitor the horizon.",
        "region": "us-west-2",
        "connections": ["Container Canyon", "DevOps Desert"],
        "difficulty": 5,
        "events": []
    },

    # EU Region
    "Function_Junction": {
        "name": "Function Junction",
        "description": "A bustling crossroads where serverless functions are exchanged. Code snippets float through the air.",
        "region": "eu-west-1",
        "connections": ["Serverless Valley", "Event Bridge"],
        "difficulty": 3,
        "events": []
    },

    "Event_Bridge": {
        "name": "Event Bridge",
        "description": "A massive bridge spanning a digital chasm. Events flow across it, triggering reactions.",
        "region": "eu-west-1",
        "connections": ["Function Junction", "State Machine Forest"],
        "difficulty": 4,
        "events": []
    },

    "State_Machine_Forest": {
        "name": "State Machine Forest",
        "description": "A dense forest of workflow trees. Step Functions guide you along predefined paths.",
        "region": "eu-west-1",
        "connections": ["Event Bridge", "Microservice Meadows"],
        "difficulty": 5,
        "events": []
    },

    # ASIA Region
    "Cache_Cove": {
        "name": "Cache Cove",
        "description": "A hidden bay where cached data washes ashore. ElastiCache instances bob in the water.",
        "region": "ap-southeast-1",
        "connections": ["Database District", "Query Quicksand"],
        "difficulty": 3,
        "events": []
    },

    "Query_Quicksand": {
        "name": "Query Quicksand",
        "description": "Treacherous grounds where poorly optimized queries sink without a trace. Indexes provide safe paths.",
        "region": "ap-southeast-1",
        "connections": ["Cache Cove", "NoSQL Nullspace"],
        "difficulty": 4,
        "events": [],
        "hazards": [
            {
                "name": "Query Collapse",
                "description": "Unstable data structures may collapse, causing damage.",
                "chance": 20,
                "damage": "random.randint(5, 15)",
                "avoidable_with_skill": "database"
            }
        ]
    },

    "NoSQL_Nullspace": {
        "name": "NoSQL Nullspace",
        "description": "A strange dimensionless void where traditional database rules don't apply. Document models float freely.",
        "region": "ap-southeast-1",
        "connections": ["Query Quicksand", "Blockchain Bazaar"],
        "difficulty": 5,
        "events": []
    },

    # Additional Locations for Advanced Players
    "Network_Nexus": {
        "name": "Network Nexus",
        "description": "The central routing facility for all cloud traffic. VPCs intersect and packets zoom through routers.",
        "region": "global",
        "connections": ["Security Perimeter", "Hybrid Harbor"],
        "difficulty": 6,
        "events": ["network_storm"]
    },

    "Hybrid_Harbor": {
        "name": "Hybrid Harbor",
        "description": "Where on-premises connections dock with cloud services. Direct Connect cables stretch into the distance.",
        "region": "global",
        "connections": ["Network Nexus", "Multi-Cloud Maelstrom"],
        "difficulty": 7,
        "events": []
    },

    "Analytics_Archipelago": {
        "name": "Analytics Archipelago",
        "description": "A collection of islands each dedicated to a different data analytics service.",
        "region": "us-east-2",
        "connections": ["Database District", "Machine Learning Marsh"],
        "difficulty": 6,
        "events": []
    },

    "Machine_Learning_Marsh": {
        "name": "Machine Learning Marsh",
        "description": "A mysterious wetland where models train and infer. Neural networks form like lily pads.",
        "region": "us-east-2",
        "connections": ["Analytics Archipelago", "AI Abyss"],
        "difficulty": 8,
        "events": []
    },

    "DevOps_Desert": {
        "name": "DevOps Desert",
        "description": "A harsh landscape where CI/CD pipelines form oases. CodeBuild and CodeDeploy caravans cross the dunes.",
        "region": "us-west-1",
        "connections": ["Kubernetes Plateau", "Infrastructure Wastes"],
        "difficulty": 7,
        "events": [],
        "hazards": [
            {
                "name": "Broken Pipeline",
                "description": "Damaged CI/CD pipelines can cause deployment failures.",
                "chance": 30,
                "damage": "random.randint(8, 20)",
                "avoidable_with_skill": "cloud"
            }
        ]
    },

    "Infrastructure_Wastes": {
        "name": "Infrastructure Wastes",
        "description": "The ancient ruins of manual infrastructure. CloudFormation templates help rebuild civilization.",
        "region": "us-west-1",
        "connections": ["DevOps Desert"],
        "difficulty": 8,
        "events": []
    },

    "Microservice_Meadows": {
        "name": "Microservice Meadows",
        "description": "Rolling fields filled with small, specialized service flowers. API Gateways stand like fences.",
        "region": "eu-central-1",
        "connections": ["State Machine Forest", "Service Mesh Mountain"],
        "difficulty": 6,
        "events": []
    },

    "Service_Mesh_Mountain": {
        "name": "Service Mesh Mountain",
        "description": "A towering peak where services are interconnected in complex meshes. Traffic flows along monitored paths.",
        "region": "eu-central-1",
        "connections": ["Microservice Meadows"],
        "difficulty": 8,
        "events": []
    },

    "Blockchain_Bazaar": {
        "name": "Blockchain Bazaar",
        "description": "A bustling marketplace built on distributed ledger technology. Smart contracts seal every deal.",
        "region": "ap-northeast-1",
        "connections": ["NoSQL Nullspace", "Quantum Quarry"],
        "difficulty": 9,
        "events": []
    },

    "Quantum_Quarry": {
        "name": "Quantum Quarry",
        "description": "The deepest, most mysterious location. Quantum computing experiments create reality-bending effects.",
        "region": "ap-northeast-1",
        "connections": ["Blockchain Bazaar"],
        "difficulty": 10,
        "events": ["quantum_fluctuation"]
    },

    "Multi-Cloud_Maelstrom": {
        "name": "Multi-Cloud Maelstrom",
        "description": "A churning storm where multiple cloud providers' services mix together. Only the most skilled can navigate it.",
        "region": "global",
        "connections": ["Hybrid Harbor", "Shadow Admin's Lair"],
        "difficulty": 9,
        "events": []
    },

    "AI_Abyss": {
        "name": "AI Abyss",
        "description": "An unfathomable depth where sentient AI systems evolve. Complex algorithms create emergent behaviors.",
        "region": "us-east-2",
        "connections": ["Machine Learning Marsh", "Shadow Admin's Lair"],
        "difficulty": 9,
        "events": []
    },

    "Shadow_Admins_Lair": {
        "name": "Shadow Admin's Lair",
        "description": "The hidden headquarters of the mysterious Shadow Admin who controls the cloud from behind the scenes.",
        "region": "unknown",
        "connections": ["Multi-Cloud Maelstrom", "AI Abyss"],
        "difficulty": 10,
        "events": ["admin_sighting", "shadow_admin_message"],
        "hazards": [
            {
                "name": "Security Countermeasures",
                "description": "Powerful defense systems that target intruders.",
                "chance": 50,
                "damage": "random.randint(15, 30)",
                "avoidable_with_skill": "security"
            }
        ]
    }
}
