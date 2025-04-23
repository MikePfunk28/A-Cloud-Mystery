import random
from typing import Dict, Any, List, Optional

from neon_shadow.constants import (
    CLR_BRIGHT, CLR_CYAN, CLR_RESET, CLR_SUCCESS,
    CLR_ERROR, CLR_WARNING
)
from neon_shadow.ui import print_slow
from neon_shadow.artifact import CloudArtifact
from neon_shadow.service import CloudService


class CloudEvent:
    """Represents an event that can occur at a location."""

    def __init__(self, id: str, name: str, description: str, event_type: str,
                 effects: Optional[Dict[str, Any]] = None,
                 requirements: Optional[Dict[str, Any]] = None,
                 chance: int = 100, repeatable: bool = False) -> None:
        """Initialize a new CloudEvent.
        
        Args:
            id: Unique identifier for this event
            name: Name of the event
            description: Description of what happens
            event_type: Type of event ('encounter', 'discovery', 'disaster', 'reward', etc.)
            effects: Effects on player (health, credits, faction_rep, etc.)
            requirements: Requirements to trigger (min_skill, artifacts, clues, min_faction_rep)
            chance: Percentage chance of occurring
            repeatable: Whether this event can occur multiple times
        """
        self.id = id
        self.name = name
        self.description = description
        self.event_type = event_type
        self.effects = effects if effects else {}
        self.requirements = requirements if requirements else {}
        self.chance = chance
        self.repeatable = repeatable
        self.has_occurred = False
        self.cooldown = 0  # Turns until event can trigger again
        self.cooldown_duration = 0  # How long the cooldown should be when triggered

    def can_trigger(self, player) -> bool:
        """Check if the event can be triggered.
        
        Args:
            player: The player object to check requirements against
            
        Returns:
            True if the event can be triggered, False otherwise
        """
        if self.cooldown > 0:
            return False

        if not self.repeatable and self.has_occurred:
            return False

        # Check player requirements
        if 'min_skill' in self.requirements:
            for skill, level in self.requirements['min_skill'].items():
                if player.skills.get(skill, 0) < level:
                    return False

        if 'artifacts' in self.requirements:
            for artifact in self.requirements['artifacts']:
                if not player.has_artifact(artifact):
                    return False

        if 'clues' in self.requirements:
            for clue in self.requirements['clues']:
                if clue not in player.clues:
                    return False

        # Check faction reputation requirements
        if 'min_faction_rep' in self.requirements:
            for faction, level in self.requirements['min_faction_rep'].items():
                if player.faction_reputation.get(faction, 0) < level:
                    return False

        # Random chance
        if random.randint(1, 100) > self.chance:
            return False

        return True

    def trigger(self, player) -> bool:
        """Trigger the event and apply its effects.
        
        Args:
            player: The player object to apply effects to
            
        Returns:
            True if the event was successfully triggered
        """
        print(f"\n{CLR_BRIGHT}{CLR_CYAN}══════ EVENT: {self.name} ══════{CLR_RESET}")
        print_slow(self.description, color=CLR_CYAN)

        # Apply effects
        if 'credits' in self.effects:
            player.cloud_credits += self.effects['credits']
            if self.effects['credits'] > 0:
                print(
                    f"{CLR_SUCCESS}Gained {self.effects['credits']} Cloud Credits{CLR_RESET}")
            else:
                print(
                    f"{CLR_ERROR}Lost {-self.effects['credits']} Cloud Credits{CLR_RESET}")

        if 'skill' in self.effects:
            for skill, amount in self.effects['skill'].items():
                player.increase_skill(skill, amount)

        # Apply faction reputation changes
        if 'faction_rep' in self.effects:
            for faction, change in self.effects['faction_rep'].items():
                if faction in player.faction_reputation:
                    old_rep = player.faction_reputation[faction]
                    player.faction_reputation[faction] = max(
                        0, min(100, old_rep + change))
                    if change > 0:
                        print(
                            f"{CLR_SUCCESS}{faction} reputation increased by {change} (Now: {player.faction_reputation[faction]}){CLR_RESET}")
                    else:
                        print(
                            f"{CLR_ERROR}{faction} reputation decreased by {-change} (Now: {player.faction_reputation[faction]}){CLR_RESET}")
                else:
                    print(
                        f"{CLR_WARNING}Warning: Unknown faction '{faction}' in event effect.{CLR_RESET}")

        if 'artifact' in self.effects:
            artifact = CloudArtifact(
                self.effects['artifact']['name'],
                self.effects['artifact']['description'],
                self.effects['artifact']['artifact_type'],
                self.effects['artifact'].get('aws_service'),
                self.effects['artifact'].get('cost', 0),
                self.effects['artifact'].get('power', 1)
            )
            player.add_artifact(artifact)

        if 'clue' in self.effects:
            player.add_clue(self.effects['clue'])

        if 'service' in self.effects:
            service = CloudService(
                name=self.effects['service']['name'],
                description=self.effects['service']['description'],
                service_type=self.effects['service'].get(
                    'service_type', self.effects['service']['type']),
                cost_per_hour=self.effects['service'].get('cost_per_hour', 1),
                deploy_cost=self.effects['service'].get('deploy_cost', 10),
                region_availability=self.effects['service'].get(
                    'region_availability', ['us-east-1']),
                dependencies=self.effects['service'].get('dependencies', [])
            )
            player.add_service(service)

        if 'time' in self.effects:
            player.time_left += self.effects['time']
            if self.effects['time'] > 0:
                print(
                    f"{CLR_SUCCESS}Gained {self.effects['time']} days{CLR_RESET}")
            else:
                print(
                    f"{CLR_ERROR}Lost {-self.effects['time']} days{CLR_RESET}")

        if 'health' in self.effects:
            if self.effects['health'] > 0:
                player.heal(self.effects['health'])
            else:
                player.take_damage(-self.effects['health'], self.name)

        if 'energy' in self.effects:
            if self.effects['energy'] > 0:
                amt = player.restore_energy(self.effects['energy'])
                print(f"{CLR_SUCCESS}Restored {amt} energy{CLR_RESET}")
            else:
                if player.use_energy(-self.effects['energy']):
                    print(
                        f"{CLR_WARNING}Used {-self.effects['energy']} energy{CLR_RESET}")
                else:
                    print(f"{CLR_ERROR}Not enough energy!{CLR_RESET}")

        if 'status_effect' in self.effects:
            player.add_status_effect(self.effects['status_effect'])

        if 'consumable' in self.effects:
            item_name = self.effects['consumable']['name']
            count = self.effects['consumable'].get('count', 1)
            player.inventory.add_consumable(item_name, count)
            print(f"{CLR_SUCCESS}Acquired {count}x {item_name}{CLR_RESET}")

        self.has_occurred = True
        # Set cooldown if defined
        if self.cooldown_duration > 0:
            self.cooldown = self.cooldown_duration
        return True

    def update_cooldown(self) -> bool:
        """Update the cooldown timer for this event.
        
        Returns:
            True if cooldown was decreased, False if no active cooldown
        """
        if self.cooldown > 0:
            self.cooldown -= 1
            return True
        return False
