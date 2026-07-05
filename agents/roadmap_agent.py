import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class RoadmapAgent:
    """
    Agent responsible for processing, validating, and structuring the
    6-Week Learning Roadmap section of the coordinated JSON payload.
    """
    def __init__(self) -> None:
        pass

    def process(self, data: Any) -> List[Dict[str, Any]]:
        """
        Accepts the learning_roadmap list from the coordinator JSON.
        Validates elements, ensures exactly 6 weeks of data, and applies fallback defaults.
        """
        logger.info("RoadmapAgent: Starting roadmap block validation.")
        
        raw_list = data if isinstance(data, list) else []
        processed_roadmap = []

        # We must enforce exactly 6 weeks (from Week 1 to Week 6)
        for week_num in range(1, 7):
            week_title = f"Week {week_num}"
            found_week_dict = None

            # Look for a dictionary that represents this week by name
            for item in raw_list:
                if isinstance(item, dict) and str(item.get("week", "")).strip().lower() == week_title.lower():
                    found_week_dict = item
                    break

            # Fall back to index if not matched by name
            if not found_week_dict and (week_num - 1) < len(raw_list):
                candidate = raw_list[week_num - 1]
                if isinstance(candidate, dict):
                    found_week_dict = candidate

            if found_week_dict:
                raw_hours = found_week_dict.get("estimated_hours", 10)
                try:
                    estimated_hours = int(raw_hours)
                except (ValueError, TypeError):
                    logger.warning(f"RoadmapAgent: Invalid hours '{raw_hours}'. Defaulting to 10.")
                    estimated_hours = 10
                
                estimated_hours = max(1, min(80, estimated_hours))

                week_data = {
                    "week": week_title,
                    "topics": self._sanitize_string_list(found_week_dict.get("topics")),
                    "coding_practice": self._sanitize_string_list(found_week_dict.get("coding_practice")),
                    "mini_projects": self._sanitize_string_list(found_week_dict.get("mini_projects")),
                    "interview_questions": self._sanitize_string_list(found_week_dict.get("interview_questions")),
                    "revision_tasks": self._sanitize_string_list(found_week_dict.get("revision_tasks")),
                    "estimated_hours": estimated_hours
                }
            else:
                # Supply default roadmap details for empty/missing weeks
                week_data = {
                    "week": week_title,
                    "topics": ["Technical concept deep dive & DSA fundamentals."],
                    "coding_practice": ["Practice basic and intermediate coding problems (Arrays, Hashmaps)."],
                    "mini_projects": ["Design a small CLI utility or API integrating these concepts."],
                    "interview_questions": ["Explain common concepts and space/time complexities of operations."],
                    "revision_tasks": ["Re-run past programming test cases and verify edge cases."],
                    "estimated_hours": 10
                }
            
            processed_roadmap.append(week_data)

        logger.info("RoadmapAgent: Roadmap processing and structural formatting complete.")
        return processed_roadmap

    def _sanitize_string_list(self, raw_list: Any) -> List[str]:
        """
        Standardizes input items into a clean list of strings.
        """
        if isinstance(raw_list, list):
            return [str(item).strip() for item in raw_list if item and str(item).strip()]
        elif isinstance(raw_list, str) and raw_list.strip():
            return [raw_list.strip()]
        return []
