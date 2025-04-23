"""
Definitions of all vendors available at various locations.
Each vendor has an inventory of items and requirements to access them.
"""

VENDORS = {
    "CloudTech_Supplies": {
        "name": "CloudTech Supplies",
        "description": "General store selling basic artifacts and consumables",
        "location": "Cloud_City",
        "inventory": {
            "artifacts": ["S3_Scanner", "EC2_Inspector"],
            "consumables": {
                "Emergency_Patch": {
                    "description": "Restores 30 health",
                    "price": 25,
                    "effect": "player.heal(30)"
                },
                "Energy_Cell": {
                    "description": "Restores 50 energy",
                    "price": 20,
                    "effect": "player.restore_energy(50)"
                }
            }
        }
    },

    "CorpSec_Defense_Systems": {
        "name": "CorpSec Defense Systems",
        "description": "High-quality security artifacts",
        "location": "Security_Perimeter",
        "reputation_required": {"CorpSec": 20},
        "inventory": {
            "artifacts": ["IAM_Auditor", "GuardDuty_Lens", "WAF_Shield"],
            "consumables": {
                "Firewall_Patch": {
                    "description": "Increases service security by 2",
                    "price": 40,
                    "effect": "service.enhance_security(2)"
                }
            }
        }
    },

    "DataStore_Solutions": {
        "name": "DataStore Solutions",
        "description": "Database services and optimization tools",
        "location": "Database_District",
        "inventory": {
            "artifacts": ["RDS_Analyzer", "Aurora_Analyzer", "DynamoDB_Query_Engine"],
            "services": ["RDS_Database", "DynamoDB_Table"]
        }
    },

    "FunctionForge": {
        "name": "FunctionForge",
        "description": "Serverless computing specialists",
        "location": "Serverless_Valley",
        "reputation_required": {"ServerlessCollective": 10},
        "inventory": {
            "artifacts": ["Lambda_Invoker"],
            "services": ["Lambda_Function", "API_Gateway"]
        }
    },

    "Network_Nexus_Exchange": {
        "name": "Network Nexus Exchange",
        "description": "Advanced networking tools and services",
        "location": "Network_Nexus",
        "inventory": {
            "artifacts": ["VPC_Tracer", "Route53_Resolver"],
            "services": ["VPC", "Elastic_Load_Balancer"]
        }
    },

    "Container_Outfitters": {
        "name": "Container Outfitters",
        "description": "Container and orchestration specialists",
        "location": "Container_Canyon",
        "inventory": {
            "artifacts": ["ECS_Orchestrator"],
            "services": ["Elastic_Kubernetes_Service"]
        }
    },

    "Edge_Technologies": {
        "name": "Edge Technologies",
        "description": "CDN and edge computing solutions",
        "location": "Edge_Outpost",
        "inventory": {
            "services": ["CloudFront_Distribution"],
            "consumables": {
                "Performance_Booster": {
                    "description": "Increases service performance by 2",
                    "price": 35,
                    "effect": "service.optimize_performance(2)"
                }
            }
        }
    },

    "Shadow_Market": {
        "name": "Shadow Market",
        "description": "Black market dealer with rare items",
        "location": "Blockchain_Bazaar",
        "reputation_required": {"ShadowNetwork": 30},
        "inventory": {
            "artifacts": ["Network_Pulse_Emitter", "Vulnerability_Scanner_Pro", "Digital_Shield_Generator"],
            "consumables": {
                "Zero_Day_Exploit": {
                    "description": "Powerful attack tool that bypasses security",
                    "price": 100,
                    "effect": "special.attack_bonus(15)"
                },
                "Stealth_Module": {
                    "description": "Temporarily makes you undetectable to security systems",
                    "price": 75,
                    "effect": "player.add_status_effect('stealth', 3)"
                }
            }
        }
    },

    "Quantum_Components": {
        "name": "Quantum Components",
        "description": "Experimental quantum computing artifacts",
        "location": "Quantum_Quarry",
        "reputation_required": {"DataBrokers": 40},
        "inventory": {
            "artifacts": ["Quantum_Decryptor"],
            "consumables": {
                "Quantum_Shard": {
                    "description": "Temporarily boosts all skills by 1",
                    "price": 150,
                    # +1 to all skills for 3 turns
                    "effect": "player.boost_all_skills(1, 3)"
                }
            }
        }
    }
}
