"""
Definition of all weather conditions that can affect game locations.
Weather conditions have various effects on gameplay.
"""

WEATHER_TYPES = [
    {
        "name": "Data Storm",
        "effect": "Bandwidth -20%",
        "description": "A storm of corrupted data packets. Network performance is reduced and connections are unstable.",
        "consequences": {
            "bandwidth": -0.2,  # 20% bandwidth reduction
            "service_risk": 0.1  # 10% increased chance of service issues
        }
    },
    {
        "name": "Processing Fog",
        "effect": "Investigation -2",
        "description": "Dense fog reducing visibility and making investigation more difficult.",
        "consequences": {
            "investigation_penalty": 2,
            "exploration_efficiency": -0.15  # 15% less effective exploration
        }
    },
    {
        "name": "CPU Heatwave",
        "effect": "Energy -10%",
        "description": "Extreme computational heat causing systems to require more energy to operate.",
        "consequences": {
            "energy_drain": 0.1,  # 10% faster energy drain
            "service_performance": -1  # -1 to service performance
        }
    },
    {
        "name": "Memory Frost",
        "effect": "Service performance -2",
        "description": "Cold conditions slowing memory access and overall service performance.",
        "consequences": {
            "service_performance": -2,
            "service_revenue": -0.1  # 10% less service revenue
        }
    },
    {
        "name": "Clear Signals",
        "effect": "All stats +5%",
        "description": "Perfect conditions with clear connections boosting all systems.",
        "consequences": {
            "all_bonus": 0.05,  # 5% bonus to all stats
            "service_performance": 1,  # +1 to service performance
            "energy_recovery": 0.2  # 20% faster energy recovery
        }
    },
    {
        "name": "Quantum Fluctuations",
        "effect": "Random effects",
        "description": "Unpredictable quantum effects causing systems to behave erratically.",
        "consequences": {
            "random_events": 0.2,  # 20% higher chance of random events
            "critical_success": 0.1,  # 10% higher chance of critical success
            "critical_failure": 0.1  # 10% higher chance of critical failure
        }
    },
    {
        "name": "Packet Precipitation",
        "effect": "Network -15%, Credits +10%",
        "description": "A rain of data packets slowing networks but occasionally containing valuable information.",
        "consequences": {
            "network_penalty": -0.15,
            "credit_discovery": 0.1  # 10% chance to find extra credits
        }
    },
    {
        "name": "Authentication Aurora",
        "effect": "Security +1, Energy -5%",
        "description": "Beautiful authentication patterns in the sky that enhance security but drain energy.",
        "consequences": {
            "security_bonus": 1,
            "energy_drain": 0.05
        }
    }
]

# Weather severity levels that modify the base effects
SEVERITY_LEVELS = {
    1: {"name": "Minimal", "multiplier": 0.5},
    2: {"name": "Light", "multiplier": 0.75},
    3: {"name": "Moderate", "multiplier": 1.0},
    4: {"name": "Heavy", "multiplier": 1.5},
    5: {"name": "Extreme", "multiplier": 2.0},
    6: {"name": "Catastrophic", "multiplier": 3.0}
}

# Typical weather patterns for different regions
REGIONAL_WEATHER_TENDENCIES = {
    "us-east-1": ["Clear Signals", "Processing Fog"],  # Balanced region
    "us-east-2": ["CPU Heatwave", "Clear Signals"],    # Compute-heavy region
    "us-west-1": ["Data Storm", "Packet Precipitation"],  # More network issues
    "us-west-2": ["Memory Frost", "Authentication Aurora"],  # Security focused
    "eu-west-1": ["Clear Signals", "Authentication Aurora"],  # Stable region
    "eu-central-1": ["Processing Fog", "Memory Frost"],  # Performance challenges
    "ap-southeast-1": ["Data Storm", "CPU Heatwave"],  # Challenging region
    "ap-northeast-1": ["Quantum Fluctuations", "Memory Frost"],  # Unpredictable
    "global": ["Quantum Fluctuations", "Data Storm"],  # Edge locations
    "unknown": ["Quantum Fluctuations"]  # Shadow Admin's region
}
