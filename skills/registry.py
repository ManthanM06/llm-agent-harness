"""
skills/registry.py
Manages registration, lookup, and triggering of skills.
"""
from typing import Dict, Optional, Tuple, List
from skills.base import BaseSkill
from skills.leetcode import LeetCodeSkill

class SkillRegistry:
    def __init__(self):
        self._skills: Dict[str, BaseSkill] = {}
        
        # Register built-in skills
        self.register(LeetCodeSkill())

    def register(self, skill: BaseSkill) -> None:
        """Register a new skill by its trigger."""
        self._skills[skill.trigger.lower()] = skill

    def get_skill_by_trigger(self, trigger: str) -> Optional[BaseSkill]:
        """Look up a skill by exact trigger (e.g. '/leetcode')."""
        return self._skills.get(trigger.lower())

    def match_skill(self, prompt: str) -> Tuple[Optional[BaseSkill], str]:
        """
        Inspects the prompt to see if it matches any registered skill.
        Returns:
            (skill, extracted_content) if matched, or (None, prompt) if no skill matched.
        """
        prompt_stripped = prompt.strip()
        first_token = prompt_stripped.split()[0].lower() if prompt_stripped else ""
        
        if first_token in self._skills:
            skill = self._skills[first_token]
            content = skill.extract_content(prompt)
            return skill, content

        return None, prompt

    def get_all_skills(self) -> List[BaseSkill]:
        """Returns all registered skills."""
        return list(self._skills.values())

skill_registry = SkillRegistry()
