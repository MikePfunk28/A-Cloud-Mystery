from typing import Dict, List, Set, Union, Optional, Any

from neon_shadow.constants import (
    CLR_LOCATION_NAME, CLR_LOCATION_DESC, CLR_RESET,
    CLR_INTERACTION, CLR_HAZARD, CLR_CLOUD_SERVICE
)
from neon_shadow.ui import display_notification


class Location:
    """Represents a location in the game world."""

    def __init__(self, name: str, description: str, region: Optional[str] = None,
                 connections: Optional[List[str]] = None,
                 events: Optional[List[str]] = None,
                 services: Optional[List[str]] = None,
                 difficulty: int = 1) -> None:
        """Initialize a new location.
        
        Args:
            name: Name of the location
            description: Description of the location
            region: AWS region this location is in
            connections: List of connected location names
            events: List of possible events at this location
            services: List of available services at this location
            difficulty: Difficulty level (1-10)
        """
        self.name = name
        self.description = description
        self.region = region
        self.connections = connections if connections else []
        self.events = events if events else []
        self.services = services if services else []
        self.difficulty = difficulty
        self.visited = False
        self.discovered_secrets: Set[str] = set()
        self.unlocked_areas: Set[str] = set()
        self.hazards: List[Dict[str, Any]] = []
        self.vendors: List[Dict[str, Any]] = []
        self.local_reputation = 0  # Location-specific reputation (0-100)

    def __str__(self) -> str:
        return f"{self.name}"

    def display(self) -> None:
        """Display location details."""
        if not self.visited:
            self.visited = True
            print(
                f"\n{CLR_LOCATION_NAME}[ NEW LOCATION DISCOVERED: {self.name} ]{CLR_RESET}")
        else:
            print(f"\n{CLR_LOCATION_NAME}[ {self.name} ]{CLR_RESET}")

        print(f"{CLR_LOCATION_DESC}{self.description}{CLR_RESET}")

        if self.region:
            print(f"{CLR_LOCATION_DESC}AWS Region: {self.region}{CLR_RESET}")

        if self.difficulty:
            diff_stars = '★' * self.difficulty + '☆' * (10 - self.difficulty)
            print(f"{CLR_LOCATION_DESC}Difficulty: {diff_stars}{CLR_RESET}")

        print(f"\n{CLR_INTERACTION}Connections:{CLR_RESET}")
        for connection in self.connections:
            print(f"• {connection}")

        if self.hazards:
            print(f"\n{CLR_HAZARD}Potential Hazards:{CLR_RESET}")
            for hazard in self.hazards:
                print(f"• {hazard['name']} - {hazard['description']}")

        if self.vendors:
            print(f"\n{CLR_CLOUD_SERVICE}Local Vendors:{CLR_RESET}")
            for vendor in self.vendors:
                print(f"• {vendor['name']} - {vendor['description']}")

    def add_connection(self, location_name: str) -> None:
        """Add a connection to another location.
        
        Args:
            location_name: Name of location to connect to
        """
        if location_name not in self.connections:
            self.connections.append(location_name)

    def has_secret(self, secret_id: str) -> bool:
        """Check if a particular secret has been discovered.
        
        Args:
            secret_id: ID of the secret to check
            
        Returns:
            True if secret has been discovered, False otherwise
        """
        return secret_id in self.discovered_secrets

    def discover_secret(self, secret_id: str) -> bool:
        """Discover a secret at this location.
        
        Args:
            secret_id: ID of the secret to discover
            
        Returns:
            True if secret was newly discovered, False if already known
        """
        if secret_id not in self.discovered_secrets:
            self.discovered_secrets.add(secret_id)
            return True
        return False

    def add_hazard(self, hazard: Dict[str, Any]) -> None:
        """Add a hazard to this location.
        
        Args:
            hazard: Dictionary containing hazard information
        """
        self.hazards.append(hazard)

    def add_vendor(self, vendor: Dict[str, Any]) -> None:
        """Add a vendor to this location.
        
        Args:
            vendor: Dictionary containing vendor information
        """
        self.vendors.append(vendor)

    def unlock_area(self, area_id: str) -> bool:
        """Unlock a sub-area within this location.
        
        Args:
            area_id: ID of the area to unlock
            
        Returns:
            True if area was newly unlocked, False if already unlocked
        """
        if area_id not in self.unlocked_areas:
            self.unlocked_areas.add(area_id)
            display_notification(
                f"Unlocked new area in {self.name}: {area_id}", "success")
            return True
        return False

    def increase_reputation(self, amount: int) -> int:
        """Increase local reputation at this location.
        
        Args:
            amount: Amount to increase reputation by
            
        Returns:
            Actual amount reputation increased by
        """
        old_rep = self.local_reputation
        self.local_reputation = min(100, self.local_reputation + amount)
        return self.local_reputation - old_rep
