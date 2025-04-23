"""
CloudArtifact class for the Neon Shadow game.
"""

from .constants import *
from .utils import display_notification


class CloudArtifact:
    """Represents an AWS service or tool the player can use."""

    def __init__(self, name: str, description: str, artifact_type: str, aws_service: str, cost: int, power: int):
        self.name = name
        self.description = description
        self.artifact_type = artifact_type
        self.aws_service = aws_service
        self.cost = cost
        self.power = power
        self.upgrade_level = 0  # Current upgrade level
        self.max_upgrade = 3  # Maximum upgrade level
        self.cooldown = 0  # Turns until artifact can be used again

    def __str__(self):
        upgrade_stars = '★' * self.upgrade_level + \
            '☆' * (self.max_upgrade - self.upgrade_level)
        return f"{CLR_ARTIFACT}{self.name} {upgrade_stars}{CLR_RESET} ({self.artifact_type})"

    def upgrade(self):
        """Upgrade the artifact if possible."""
        if self.upgrade_level < self.max_upgrade:
            self.upgrade_level += 1
            self.power += 2
            return True
        return False

    def use(self, target=None):
        """Use the artifact on an optional target."""
        if self.cooldown > 0:
            display_notification(
                f"{self.name} is on cooldown for {self.cooldown} more turns", "warning")
            return False

        print(f"Using {self.name}...")
        # Set cooldown based on power - more powerful artifacts have longer cooldowns
        self.cooldown = 1 + (self.power // 3)
        return True

    def update_cooldown(self):
        """Update the artifact cooldown timer."""
        if self.cooldown > 0:
            self.cooldown -= 1
            return True
        return False
