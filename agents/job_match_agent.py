import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class JobMatchAgent:
    """
    Agent responsible for processing, validating, and structuring the
    Job Match section of the coordinated JSON payload.
    """
    def __init__(self) -> None:
        pass

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Accepts the job_match section from the coordinator JSON,
        validates values, and returns a clean dictionary.
        """
        logger.info("JobMatchAgent: Starting job match block validation.")
        
        if not isinstance(data, dict):
            logger.warning("JobMatchAgent received malformed or empty data. Creating defaults.")
            data = {}

        # Validate Match Percentage
        raw_percentage = data.get("match_percentage", 0)
        try:
            match_percentage = int(raw_percentage)
        except (ValueError, TypeError):
            logger.warning(f"JobMatchAgent: Invalid match percentage '{raw_percentage}'. Defaulting to 0.")
            match_percentage = 0
            
        match_percentage = max(0, min(100, match_percentage))

        processed_data = {
            "match_percentage": match_percentage,
            "matched_skills": self._sanitize_string_list(data.get("matched_skills")),
            "missing_skills": self._sanitize_string_list(data.get("missing_skills")),
            "required_certifications": self._sanitize_string_list(data.get("required_certifications")),
            "recommended_improvements": self._sanitize_string_list(data.get("recommended_improvements")),
            "top_5_resume_changes": self._sanitize_string_list(data.get("top_5_resume_changes"))
        }

        # Fallback values if top 5 changes list is empty
        if not processed_data["top_5_resume_changes"]:
            processed_data["top_5_resume_changes"] = [
                "Tailor the resume header and summary to highlight relevant keywords.",
                "Explicitly list all matched technical skills in the skills section.",
                "Detail past projects that utilize the missing skills identified.",
                "Incorporate action verbs when describing role responsibilities.",
                "Showcase certifications that demonstrate expertise in core areas."
            ]
        # Keep maximum of 5 changes
        processed_data["top_5_resume_changes"] = processed_data["top_5_resume_changes"][:5]

        logger.info("JobMatchAgent: Job match processing completed.")
        return processed_data

    def _sanitize_string_list(self, raw_list: Any) -> List[str]:
        """
        Helper to sanitize input lists into string lists.
        """
        if isinstance(raw_list, list):
            return [str(item).strip() for item in raw_list if item and str(item).strip()]
        elif isinstance(raw_list, str) and raw_list.strip():
            return [raw_list.strip()]
        return []
