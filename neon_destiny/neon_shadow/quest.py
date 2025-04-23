from typing import Dict, List, Optional, Any, Union
from neon_shadow.constants import (
    CLR_BRIGHT, CLR_YELLOW, CLR_RESET, CLR_GREEN, CLR_RED
)


class Quest:
    """Represents a quest or mission that the player can undertake."""

    def __init__(self, id: str, title: str, description: str,
                 objectives: List[Dict[str, Any]], reward: Dict[str, Any],
                 prereq_quests: Optional[List[str]] = None,
                 min_skill_level: Optional[Dict[str, int]] = None,
                 min_faction_rep: Optional[Dict[str, int]] = None,
                 location: Optional[str] = None) -> None:
        """Initialize a new quest.
        
        Args:
            id: Unique identifier for the quest
            title: Display title of the quest
            description: Quest description
            objectives: List of objective dicts with 'id', 'description', 'completed'
            reward: Dict with 'credits', 'artifacts', 'faction_rep', 'skill', etc.
            prereq_quests: List of quest IDs that must be completed first
            min_skill_level: Dictionary of skill requirements (e.g. {'hacking': 3})
            min_faction_rep: Dictionary of faction reputation requirements
            location: Location where quest is available
        """
        self.id = id
        self.title = title
        self.description = description
        self.objectives = objectives
        self.reward = reward
        self.prereq_quests = prereq_quests if prereq_quests else []
        self.min_skill_level = min_skill_level if min_skill_level else {}
        self.min_faction_rep = min_faction_rep if min_faction_rep else {}
        self.location = location
        self.time_limit = None  # Optional time limit in days
        self.difficulty = 1  # Quest difficulty (1-10)
        self.hidden = False  # Is this a hidden quest?
        self.completion_date = None  # When the quest was completed

    def is_available(self, player) -> bool:
        """Check if the quest is available to the player.
        
        Args:
            player: The player object to check requirements against
            
        Returns:
            True if quest is available, False otherwise
        """
        # Check prerequisites
        for quest_id in self.prereq_quests:
            if quest_id not in player.completed_quests:
                return False

        # Check skill requirements
        for skill, level in self.min_skill_level.items():
            if player.skills.get(skill, 0) < level:
                return False

        # Check faction reputation requirements
        for faction, level in self.min_faction_rep.items():
            if player.faction_reputation.get(faction, 0) < level:
                return False

        return True

    def start(self, player) -> bool:
        """Start the quest.
        
        Args:
            player: The player object to add the quest to
            
        Returns:
            True if quest was started, False otherwise
        """
        if self.is_available(player):
            player.add_quest(self.id)
            return True
        return False

    def complete_objective(self, objective_id: str) -> bool:
        """Mark an objective as completed.
        
        Args:
            objective_id: ID of the objective to complete
            
        Returns:
            True if objective was found and completed, False otherwise
        """
        for obj in self.objectives:
            if obj['id'] == objective_id:
                obj['completed'] = True
                return True
        return False

    def check_completion(self) -> bool:
        """Check if all objectives are completed.
        
        Returns:
            True if all objectives are completed, False otherwise
        """
        return all(obj['completed'] for obj in self.objectives)

    def display(self) -> None:
        """Display quest details."""
        print(
            f"\n{CLR_BRIGHT}{CLR_YELLOW}╔══════ QUEST: {self.title} ══════╗{CLR_RESET}")
        print(f"{CLR_BRIGHT}{CLR_YELLOW}║{CLR_RESET} {self.description}{CLR_RESET}")

        if self.difficulty:
            diff_stars = '★' * self.difficulty + '☆' * (10 - self.difficulty)
            print(
                f"{CLR_BRIGHT}{CLR_YELLOW}║{CLR_RESET} Difficulty: {diff_stars}{CLR_RESET}")

        if self.time_limit:
            print(
                f"{CLR_BRIGHT}{CLR_YELLOW}║{CLR_RESET} Time Limit: {self.time_limit} days{CLR_RESET}")

        print(f"{CLR_BRIGHT}{CLR_YELLOW}╠══════ OBJECTIVES ══════╣{CLR_RESET}")

        for obj in self.objectives:
            status = f"{CLR_GREEN}✓{CLR_RESET}" if obj['completed'] else f"{CLR_RED}□{CLR_RESET}"
            print(
                f"{CLR_BRIGHT}{CLR_YELLOW}║{CLR_RESET} {status} {obj['description']}")

        print(f"{CLR_BRIGHT}{CLR_YELLOW}╠══════ REWARDS ══════╣{CLR_RESET}")
        if 'credits' in self.reward:
            print(
                f"{CLR_BRIGHT}{CLR_YELLOW}║{CLR_RESET} • {self.reward['credits']} Cloud Credits")
        if 'artifacts' in self.reward:
            for artifact in self.reward['artifacts']:
                print(f"{CLR_BRIGHT}{CLR_YELLOW}║{CLR_RESET} • Artifact: {artifact}")
        if 'faction_rep' in self.reward:
            for faction, change in self.reward['faction_rep'].items():
                print(f"{CLR_BRIGHT}{CLR_YELLOW}║{CLR_RESET} • {faction}: +{change}")
        if 'skill' in self.reward:
            for skill, amount in self.reward['skill'].items():
                print(
                    f"{CLR_BRIGHT}{CLR_YELLOW}║{CLR_RESET} • Skill: {skill.capitalize()} +{amount}")
        if 'consumables' in self.reward:
            for item, count in self.reward['consumables'].items():
                print(
                    f"{CLR_BRIGHT}{CLR_YELLOW}║{CLR_RESET} • {item} x{count}")

        print(f"{CLR_BRIGHT}{CLR_YELLOW}╚═════════════════════════╝{CLR_RESET}")
