"""
Inventory class for the Neon Shadow game.
"""

from typing import List, Dict
from .constants import *
from .utils import display_notification


class Inventory:
    """Handles the player's inventory of artifacts and cloud services."""

    def __init__(self):
        self.artifacts = []
        self.services = []  # Undeployed service blueprints
        self.deployed_services = []  # Currently deployed service instances
        self.cloud_credits = 500
        self.max_artifacts = 10
        self.max_services = 5
        self.consumables = {}  # Dictionary of consumable items with counts

    def add_artifact(self, artifact):
        """Add an artifact to inventory if there's space."""
        if len(self.artifacts) < self.max_artifacts:
            self.artifacts.append(artifact)
            return True
        return False

    def remove_artifact(self, artifact_name):
        """Remove an artifact by name."""
        for i, art in enumerate(self.artifacts):
            if art.name == artifact_name:
                return self.artifacts.pop(i)
        return None

    def get_artifact(self, artifact_name):
        """Get an artifact by name."""
        for art in self.artifacts:
            if art.name == artifact_name:
                return art
        return None

    def has_artifact(self, artifact_name):
        """Check if player has an artifact."""
        return any(art.name == artifact_name for art in self.artifacts)

    def add_service(self, service):
        """Add a service to inventory if there's space."""
        if len(self.services) < self.max_services:
            self.services.append(service)
            return True
        return False

    def remove_service(self, service_name):
        """Remove a service by name."""
        for i, svc in enumerate(self.services):
            if svc.name == service_name:
                return self.services.pop(i)
        return None

    def get_service(self, service_name):
        """Get a service by name."""
        for svc in self.services:
            if svc.name == service_name:
                return svc
        return None

    def has_service(self, service_name):
        """Check if player has a service."""
        return any(svc.name == service_name for svc in self.services)

    def display(self):
        """Display the inventory contents."""
        print(f"\n{CLR_BRIGHT}{CLR_CYAN}══════ INVENTORY ══════{CLR_RESET}")
        print(f"{CLR_CREDITS}Cloud Credits: {self.cloud_credits}{CLR_RESET}")

        print(
            f"\n{CLR_ARTIFACT}Artifacts ({len(self.artifacts)}/{self.max_artifacts}):{CLR_RESET}")
        if self.artifacts:
            for idx, artifact in enumerate(self.artifacts, 1):
                cooldown_status = f" [COOLDOWN: {artifact.cooldown}]" if artifact.cooldown > 0 else ""
                print(f"{idx}. {artifact} - {artifact.description}{cooldown_status}")
        else:
            print("No artifacts in inventory.")

        print(
            f"\n{CLR_CLOUD_SERVICE}Cloud Services ({len(self.services)}/{self.max_services}):{CLR_RESET}")
        if self.services:
            for idx, service in enumerate(self.services, 1):
                print(f"{idx}. {service.name} - {service.description}")
        else:
            print("No cloud services in inventory.")

        print(f"\n{CLR_CLOUD_SERVICE}Deployed Services:{CLR_RESET}")
        if self.deployed_services:
            for idx, service in enumerate(self.deployed_services, 1):
                status = f"{CLR_GREEN}ONLINE{CLR_RESET}" if service.is_deployed else f"{CLR_RED}OFFLINE{CLR_RESET}"
                print(f"{idx}. {service.name} ({service.instance_id}) - {status}")
                if service.is_deployed:
                    print(f"   Region: {service.deployment_region}")
                    print(
                        f"   Health: {service.health}% | Security: {service.security_level}/10 | Performance: {service.performance}/10")
                    print(
                        f"   Revenue: {service.calculate_revenue():.2f} credits/hour | Uptime: {service.uptime_days} days")
                    if service.status_effects:
                        effects = ", ".join(
                            [f"{e['name']} ({e['duration']})" for e in service.status_effects])
                        print(f"   Status Effects: {effects}")
        else:
            print("No deployed services.")

        # Display consumables if any
        if self.consumables:
            print(f"\n{CLR_ARTIFACT}Consumables:{CLR_RESET}")
            for item_name, count in self.consumables.items():
                print(f"• {item_name} x{count}")

    def remove_deployed_service(self, instance_id):
        """Remove a deployed service by its instance ID."""
        for i, service in enumerate(self.deployed_services):
            if service.instance_id == instance_id:
                removed = self.deployed_services.pop(i)
                display_notification(
                    f"Service {removed.name} ({instance_id}) has been removed.", "warning")
                return removed
        return None

    def get_deployed_service(self, instance_id):
        """Get a deployed service by its instance ID."""
        for service in self.deployed_services:
            if service.instance_id == instance_id:
                return service
        return None

    def add_deployed_service(self, service):
        """Add a service to deployed services."""
        if service not in self.deployed_services:
            self.deployed_services.append(service)
            return True
        return False

    def add_consumable(self, item_name, count=1):
        """Add consumable items to inventory."""
        if item_name in self.consumables:
            self.consumables[item_name] += count
        else:
            self.consumables[item_name] = count
        return True

    def use_consumable(self, item_name):
        """Use a consumable item if available."""
        if item_name in self.consumables and self.consumables[item_name] > 0:
            self.consumables[item_name] -= 1
            if self.consumables[item_name] <= 0:
                del self.consumables[item_name]
            return True
        return False

    def update_all_artifacts(self):
        """Update cooldowns for all artifacts."""
        for artifact in self.artifacts:
            artifact.update_cooldown()
