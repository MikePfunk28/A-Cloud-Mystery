"""
Definition of all events available in the game.
Each event is stored as a dictionary with the required attributes.
These data definitions will be used to instantiate CloudEvent objects.
"""

EVENTS = {
    # Tutorial Events
    "welcome_to_cloud_city": {
        "id": "welcome_to_cloud_city",
        "name": "Welcome to Cloud City",
        "description": "As you arrive in Cloud City, a veteran Cloud Ranger greets you and offers guidance.",
        "event_type": "tutorial",
        "effects": {
            "credits": 25,
            "clue": "The Cloud Rangers protect the digital infrastructure from threats.",
            "faction_rep": {"CorpSec": 2}
        },
        "requirements": {},
        "chance": 100,
        "repeatable": False
    },
    "artifact_discovery": {
        "id": "artifact_discovery",
        "name": "First Artifact Discovery",
        "description": "You stumble upon a discarded S3 Scanner. It seems functional after some minor repairs.",
        "event_type": "discovery",
        "effects": {
            "artifact": {
                "name": "S3 Scanner",
                "description": "Scans and analyzes S3 buckets for vulnerabilities.",
                "artifact_type": "Scanner",
                "aws_service": "Amazon S3",
                "cost": 10,
                "power": 1
            }
        },
        "requirements": {},
        "chance": 100,
        "repeatable": False
    },

    # Location-specific Events
    "database_breach": {
        "id": "database_breach",
        "name": "Database Breach",
        "description": "You discover signs of unauthorized access to a critical database cluster.",
        "event_type": "encounter",
        "effects": {
            "skill": {"security": 1, "investigation": 1},
            "clue": "The intruder used a sophisticated SQL injection technique.",
            "faction_rep": {"CorpSec": -3, "ShadowNetwork": 2}
        },
        "requirements": {
            "min_skill": {"investigation": 1}
        },
        "chance": 75,
        "repeatable": True
    },
    "serverless_challenge": {
        "id": "serverless_challenge",
        "name": "Serverless Challenge",
        "description": "A group of developers invites you to participate in their serverless architecture contest.",
        "event_type": "challenge",
        "effects": {
            "credits": 50,
            "skill": {"serverless": 1, "cloud": 1},
            "faction_rep": {"ServerlessCollective": 5}
        },
        "requirements": {},
        "chance": 60,
        "repeatable": True
    },
    "network_storm": {
        "id": "network_storm",
        "name": "Network Storm",
        "description": "A sudden surge in network traffic creates chaos. Your quick response helps maintain stability.",
        "event_type": "disaster",
        "effects": {
            "skill": {"network": 1},
            "faction_rep": {"CorpSec": 3}
        },
        "requirements": {},
        "chance": 40,
        "repeatable": True
    },

    # Shadow Admin Events
    "shadow_admin_message": {
        "id": "shadow_admin_message",
        "name": "Message from the Shadow",
        "description": "You find a cryptic message on a terminal: 'Not all services are what they seem. Look deeper.'",
        "event_type": "discovery",
        "effects": {
            "clue": "The Shadow Admin leaves cryptic messages on compromised systems.",
            "faction_rep": {"ShadowNetwork": 1}
        },
        "requirements": {},
        "chance": 30,
        "repeatable": True
    },
    "admin_sighting": {
        "id": "admin_sighting",
        "name": "Shadow Admin Sighting",
        "description": "You catch a glimpse of a hooded figure disappearing into the digital void, leaving traces of advanced code.",
        "event_type": "encounter",
        "effects": {
            "skill": {"investigation": 1},
            "clue": "The Shadow Admin uses custom tools to move through the cloud undetected.",
            "faction_rep": {"ShadowNetwork": 2, "CorpSec": -1}
        },
        "requirements": {
            "min_skill": {"investigation": 2}
        },
        "chance": 20,
        "repeatable": True
    },

    # Rare Events
    "quantum_fluctuation": {
        "id": "quantum_fluctuation",
        "name": "Quantum Fluctuation",
        "description": "A strange quantum fluctuation occurs, temporarily enhancing your abilities.",
        "event_type": "phenomenon",
        "effects": {
            "skill": {"cloud": 1, "security": 1, "networking": 1},
            "time": 1,
            "faction_rep": {"DataBrokers": 1}  # Simplified from random choice
        },
        "requirements": {},
        "chance": 10,
        "repeatable": True
    },
    "legendary_artifact": {
        "id": "legendary_artifact",
        "name": "Legendary Artifact Discovery",
        "description": "Hidden in an encrypted data vault, you discover plans for a legendary CloudFormation Architect.",
        "event_type": "discovery",
        "effects": {
            "artifact": {
                "name": "CloudFormation Architect",
                "description": "Reverse engineers cloud infrastructure and creates templates.",
                "artifact_type": "IaC",
                "aws_service": "AWS CloudFormation",
                "cost": 100,
                "power": 8
            }
        },
        "requirements": {
            "min_skill": {"investigation": 5}
        },
        "chance": 5,
        "repeatable": False
    },

    # Health/Energy Events
    "digital_virus": {
        "id": "digital_virus",
        "name": "Digital Virus Exposure",
        "description": "You encounter a malicious piece of code that attempts to infect your systems.",
        "event_type": "hazard",
        "effects": {
            "health": -15,
            "status_effect": {
                "name": "Digital Infection",
                "duration": 3,
                "per_turn_effect": lambda player: player.take_damage(5, "virus")
            }
        },
        "requirements": {
            "min_skill": {"security": 3}
        },
        "chance": 30,
        "repeatable": True
    },
    "energy_surge": {
        "id": "energy_surge",
        "name": "Energy Grid Surge",
        "description": "A power surge in the system temporarily boosts your energy reserves.",
        "event_type": "beneficial",
        "effects": {
            "energy": 30,
            "credits": 15
        },
        "requirements": {},
        "chance": 25,
        "repeatable": True
    },
    "emergency_supplies": {
        "id": "emergency_supplies",
        "name": "Emergency Supply Cache",
        "description": "You discover a hidden cache of emergency supplies.",
        "event_type": "discovery",
        "effects": {
            "health": 20,
            "energy": 20,
            "consumable": {
                "name": "Emergency Patch",
                "count": 2
            }
        },
        "requirements": {},
        "chance": 20,
        "repeatable": True
    },

    # Global Events
    "system_update": {
        "id": "system_update",
        "name": "System-Wide Update",
        "description": "A major update is being rolled out across all AWS services, causing temporary disruption.",
        "event_type": "global",
        "effects": {
            "credits": -20,
            "time": -1,
            "status_effect": {
                "name": "System Lag",
                "duration": 2,
                "per_turn_effect": lambda player: player.use_energy(5)
            }
        },
        "requirements": {},
        "chance": 15,
        "repeatable": True
    },
    "cloud_conference": {
        "id": "cloud_conference",
        "name": "Cloud Tech Conference",
        "description": "A major cloud technology conference is happening. Attend to learn new skills and make connections.",
        "event_type": "opportunity",
        "effects": {
            "credits": -50,
            "skill": {"cloud": 1, "networking": 1},
            "faction_rep": {"CorpSec": 3, "ServerlessCollective": 3, "DataBrokers": 3}
        },
        "requirements": {},
        "chance": 10,
        "repeatable": False
    }
}
