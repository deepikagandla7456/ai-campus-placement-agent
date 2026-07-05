import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ResumeAgent:
    """
    Agent responsible for processing, validating, and structuring the
    Resume Analysis section of the coordinated JSON payload.
    """
    def __init__(self) -> None:
        pass

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Accepts the resume_analysis section from the coordinator JSON,
        validates its types and schemas, and returns a sanitized dictionary.
        """
        logger.info("ResumeAgent: Starting analysis block validation.")
        
        if not isinstance(data, dict):
            logger.warning("ResumeAgent received malformed or empty data. Creating defaults.")
            data = {}

        # Validate and coerce ATS Score (integer 0-100)
        raw_score = data.get("ats_score", 0)
        try:
            ats_score = int(raw_score)
        except (ValueError, TypeError):
            logger.warning(f"ResumeAgent: Invalid ATS score '{raw_score}'. Defaulting to 0.")
            ats_score = 0
            
        ats_score = max(0, min(100, ats_score))

        processed_data = {
            "ats_score": ats_score,
            "summary": str(data.get("summary", "Resume summary details are currently unavailable.")),
            "strengths": self._sanitize_string_list(data.get("strengths")),
            "weaknesses": self._sanitize_string_list(data.get("weaknesses")),
            "grammar_suggestions": self._sanitize_string_list(data.get("grammar_suggestions")),
            "formatting_suggestions": self._sanitize_string_list(data.get("formatting_suggestions")),
            "project_feedback": str(data.get("project_feedback", "Detailed project feedback is unavailable.")),
            "experience_feedback": str(data.get("experience_feedback", "Detailed professional experience feedback is unavailable.")),
            "missing_skills": self._sanitize_string_list(data.get("missing_skills")),
            "overall_recommendation": str(data.get("overall_recommendation", "Consider tailoring experience bullet points to matches."))
        }
        
        logger.info("ResumeAgent: Resume analysis processing completed.")
        return processed_data

    def _sanitize_string_list(self, raw_list: Any) -> List[str]:
        """
        Ensures input is represented as a clean list of non-empty strings.
        """
        if isinstance(raw_list, list):
            return [str(item).strip() for item in raw_list if item and str(item).strip()]
        elif isinstance(raw_list, str) and raw_list.strip():
            return [raw_list.strip()]
        return []
