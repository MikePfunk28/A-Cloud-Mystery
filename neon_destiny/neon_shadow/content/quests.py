"""
Definition of all quests available in the game.
Each quest is stored as a dictionary with the required attributes.
"""

QUESTS = {
    # Tutorial Quest
    "tutorial": {
        "id": "tutorial",
        "title": "Cloud Ranger Training",
        "description": "Complete basic training to become a certified Cloud Ranger.",
        "objectives": [
            {"id": "tutorial_1", "description": "Visit Cloud City", "completed": False},
            {"id": "tutorial_2", "description": "Acquire your first artifact",
                "completed": False},
            {"id": "tutorial_3", "description": "Deploy your first service",
                "completed": False}
        ],
        "reward": {
            "credits": 50,
            "faction_rep": {"CorpSec": 5}
        },
        "prereq_quests": [],
        "min_skill_level": {},
        "min_faction_rep": {},
        "location": "Cloud City",
        "difficulty": 1
    },

    # Main Story Quests
    "mysterious_outage": {
        "id": "mysterious_outage",
        "title": "The Mysterious Outage",
        "description": "Investigate a service outage reported in the Database District.",
        "objectives": [
            {"id": "outage_1", "description": "Visit Database District",
                "completed": False},
            {"id": "outage_2", "description": "Scan the affected RDS instance",
                "completed": False},
            {"id": "outage_3", "description": "Find evidence of the attack",
                "completed": False},
            {"id": "outage_4", "description": "Report your findings to Security Perimeter",
                "completed": False}
        ],
        "reward": {
            "credits": 100,
            "skill": {"investigation": 1, "security": 1},
            "faction_rep": {"CorpSec": 10}
        },
        "prereq_quests": ["tutorial"],
        "min_skill_level": {},
        "min_faction_rep": {},
        "location": "Database District",
        "difficulty": 2
    },
    "shadow_admin": {
        "id": "shadow_admin",
        "title": "Trail of the Shadow Admin",
        "description": "Follow the clues left by the mysterious Shadow Admin who seems to be behind recent incidents.",
        "objectives": [
            {"id": "shadow_1", "description": "Collect all Shadow Admin clues",
                "completed": False},
            {"id": "shadow_2", "description": "Decrypt the secret message",
                "completed": False},
            {"id": "shadow_3", "description": "Find the Shadow Admin's hidden access point",
                "completed": False},
            {"id": "shadow_4", "description": "Confront the Shadow Admin",
                "completed": False}
        ],
        "reward": {
            "credits": 500,
            "artifacts": ["Console Master Key"],
            "skill": {"security": 3, "cloud": 3},
            "faction_rep": {"CorpSec": 15, "ShadowNetwork": -10}
        },
        "prereq_quests": ["mysterious_outage"],
        "min_skill_level": {"security": 3, "investigation": 3},
        "min_faction_rep": {},
        "location": "Security Perimeter",
        "difficulty": 9
    },

    # Side Quests
    "data_recovery": {
        "id": "data_recovery",
        "title": "Critical Data Recovery",
        "description": "Help recover crucial data from a failed database cluster in Cache Cove.",
        "objectives": [
            {"id": "recovery_1", "description": "Travel to Cache Cove",
                "completed": False},
            {"id": "recovery_2", "description": "Assess database damage",
                "completed": False},
            {"id": "recovery_3", "description": "Deploy RDS with recovery mode",
                "completed": False},
            {"id": "recovery_4", "description": "Restore data from backup",
                "completed": False}
        ],
        "reward": {
            "credits": 150,
            "artifacts": ["Aurora Analyzer"],
            "skill": {"database": 2},
            "faction_rep": {"DataBrokers": 10}
        },
        "prereq_quests": [],
        "min_skill_level": {"database": 2},
        "min_faction_rep": {},
        "location": "Cache Cove",
        "difficulty": 3
    },
    "serverless_pioneer": {
        "id": "serverless_pioneer",
        "title": "Serverless Pioneer",
        "description": "Master serverless technologies by completing a series of challenges in Serverless Valley.",
        "objectives": [
            {"id": "serverless_1", "description": "Deploy 3 Lambda functions",
                "completed": False},
            {"id": "serverless_2",
                "description": "Create API Gateway endpoints", "completed": False},
            {"id": "serverless_3",
                "description": "Set up event-driven architecture", "completed": False},
            {"id": "serverless_4",
                "description": "Complete the Serverless Challenge", "completed": False}
        ],
        "reward": {
            "credits": 200,
            "artifacts": ["Lambda Invoker"],
            "skill": {"serverless": 3, "cloud": 1},
            "faction_rep": {"ServerlessCollective": 15}
        },
        "prereq_quests": [],
        "min_skill_level": {"serverless": 1},
        "min_faction_rep": {"ServerlessCollective": 10},
        "location": "Serverless Valley",
        "difficulty": 4
    },
    "secure_the_perimeter": {
        "id": "secure_the_perimeter",
        "title": "Secure the Perimeter",
        "description": "Help strengthen Cloud City's security by addressing vulnerabilities in Security Perimeter.",
        "objectives": [
            {"id": "secure_1", "description": "Audit IAM policies", "completed": False},
            {"id": "secure_2", "description": "Configure Security Groups",
                "completed": False},
            {"id": "secure_3", "description": "Deploy WAF rules", "completed": False},
            {"id": "secure_4", "description": "Test security with penetration test",
                "completed": False}
        ],
        "reward": {
            "credits": 175,
            "artifacts": ["IAM Auditor"],
            "skill": {"security": 2, "network": 1},
            "faction_rep": {"CorpSec": 12}
        },
        "prereq_quests": [],
        "min_skill_level": {"security": 2},
        "min_faction_rep": {"CorpSec": 20},
        "location": "Security Perimeter",
        "difficulty": 5
    },

    # Advanced Quests
    "shadow_network_infiltration": {
        "id": "shadow_network_infiltration",
        "title": "Shadow Network Infiltration",
        "description": "Gain the trust of the Shadow Network by completing a series of covert operations.",
        "objectives": [
            {"id": "infiltrate_1", "description": "Meet the Shadow Network contact in Blockchain Bazaar", "completed": False},
            {"id": "infiltrate_2",
                "description": "Complete a test mission to prove your skills", "completed": False},
            {"id": "infiltrate_3",
                "description": "Extract data from a secure facility", "completed": False},
            {"id": "infiltrate_4",
                "description": "Deliver the data to gain Shadow Network trust", "completed": False}
        ],
        "reward": {
            "credits": 300,
            "artifacts": ["Vulnerability Scanner Pro"],
            "skill": {"security": 2, "investigation": 2},
            "faction_rep": {"ShadowNetwork": 20, "CorpSec": -10}
        },
        "prereq_quests": [],
        "min_skill_level": {"security": 5, "investigation": 4},
        "min_faction_rep": {"ShadowNetwork": 20},
        "location": "Blockchain Bazaar",
        "difficulty": 7
    },
    "quantum_algorithm": {
        "id": "quantum_algorithm",
        "title": "The Quantum Algorithm",
        "description": "Develop a quantum computing algorithm in the Quantum Quarry to break an unbreakable cipher.",
        "objectives": [
            {"id": "quantum_1", "description": "Study quantum computing principles",
                "completed": False},
            {"id": "quantum_2", "description": "Gather quantum computing resources",
                "completed": False},
            {"id": "quantum_3", "description": "Develop the algorithm prototype",
                "completed": False},
            {"id": "quantum_4", "description": "Test the algorithm against the cipher",
                "completed": False}
        ],
        "reward": {
            "credits": 400,
            "artifacts": ["Quantum Decryptor"],
            "skill": {"cloud": 3, "security": 2},
            "faction_rep": {"DataBrokers": 15, "ServerlessCollective": 10}
        },
        "prereq_quests": [],
        "min_skill_level": {"cloud": 6},
        "min_faction_rep": {},
        "location": "Quantum Quarry",
        "difficulty": 9
    }
}
