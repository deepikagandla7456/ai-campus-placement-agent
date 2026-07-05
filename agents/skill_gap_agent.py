import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class SkillGapAgent:
    """
    Agent responsible for processing, validating, and structuring the
    Skill Gap section of the coordinated JSON payload.
    """
    def __init__(self) -> None:
        pass

    def process(self, data: Any) -> List[Dict[str, Any]]:
        """
        Accepts the skill_gap list from the coordinator JSON,
        validates fields, standardizes categories, and returns a sanitized list.
        """
        logger.info("SkillGapAgent: Starting skill gap block validation.")
        
        if not isinstance(data, list):
            logger.warning("SkillGapAgent: Received non-list data. Returning empty list.")
            return []

        processed_list = []
        for idx, item in enumerate(data):
            if not isinstance(item, dict):
                logger.warning(f"SkillGapAgent: Skipping item at index {idx} due to incorrect type.")
                continue

            processed_item = {
                "skill": str(item.get("skill", "General Technical Concepts")).strip(),
                "importance": self._sanitize_enum(item.get("importance"), ["High", "Medium", "Low"], "Medium"),
                "difficulty": self._sanitize_enum(item.get("difficulty"), ["Easy", "Medium", "Hard"], "Medium"),
                "learning_time": str(item.get("learning_time", "2 weeks")).strip(),
                "learning_resource": str(item.get("learning_resource", "Coursera / Udemy / Official Documentation")).strip(),
                "project_suggestion": str(item.get("project_suggestion", "Design a custom proof-of-concept project incorporating this skill.")).strip(),
                "priority": self._sanitize_enum(item.get("priority"), ["High", "Medium", "Low"], "Medium")
            }
            processed_list.append(processed_item)

        logger.info(f"SkillGapAgent: Verified and structured {len(processed_list)} skill gap records.")
        return processed_list

    def _sanitize_enum(self, value: Any, options: List[str], default: str) -> str:
        """
        Helper to map input strings to a set of predefined valid categories.
        """
        if not value:
            return default
        val_str = str(value).strip().capitalize()
        for opt in options:
            if val_str == opt or val_str.lower() == opt.lower():
                return opt
        return default
