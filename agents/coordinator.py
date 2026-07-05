import json
import logging
from pathlib import Path
from typing import Dict, Any

import prompts
import config
from utils.gemini import generate_json_response

# Import specialized agents
from agents.resume_agent import ResumeAgent
from agents.job_match_agent import JobMatchAgent
from agents.skill_gap_agent import SkillGapAgent
from agents.roadmap_agent import RoadmapAgent
from agents.interview_agent import InterviewAgent

logger = logging.getLogger(__name__)

class CoordinatorAgent:
    """
    Central orchestrator agent. Coordinates loading static company profiles,
    invoking Gemini for a single JSON analysis, and delegating sections of that
    response to specialized sub-agent classes for validation and cleanup.
    """
    def __init__(self) -> None:
        self.resume_agent = ResumeAgent()
        self.job_match_agent = JobMatchAgent()
        self.skill_gap_agent = SkillGapAgent()
        self.roadmap_agent = RoadmapAgent()
        self.interview_agent = InterviewAgent()

    def _load_company_data(self, company_name: str) -> Dict[str, Any]:
        """
        Loads static company interview details from data/companies.json.
        """
        companies_file_path = Path(config.BASE_DIR) / "data" / "companies.json"
        try:
            if companies_file_path.exists():
                with open(companies_file_path, "r") as f:
                    companies_dict = json.load(f)
                return companies_dict.get(company_name, {})
            else:
                logger.warning(f"companies.json not found at: {companies_file_path}")
        except Exception as e:
            logger.error(f"Failed to load static company profiles: {str(e)}")
        return {}

    def analyze(self, resume_text: str, job_description: str = "", company_name: str = "General") -> Dict[str, Any]:
        """
        Runs the placement preparation analysis workflow using a single Gemini model call.
        """
        logger.info(f"CoordinatorAgent: Starting analysis cycle for company target: '{company_name}'")

        # 1. Load static company metadata to supply relevant hiring details
        company_profile = self._load_company_data(company_name)
        company_profile_str = json.dumps(company_profile, indent=2) if company_profile else "Generic technical engineering placement guidelines."

        # 2. Format the user prompt combining all parameters
        job_desc_str = job_description if job_description.strip() else "None provided. Assume General Software Development Engineer Role."
        user_prompt = prompts.ANALYSIS_USER_PROMPT_TEMPLATE.format(
            company_name=company_name,
            company_details=company_profile_str,
            job_description=job_desc_str,
            resume_text=resume_text
        )

        # 3. Call the Gemini API with structured JSON configs
        logger.info("CoordinatorAgent: Issuing request to Gemini model.")
        raw_json_response = generate_json_response(
            system_instruction=prompts.ANALYSIS_SYSTEM_INSTRUCTION,
            prompt=user_prompt
        )

        # 4. Extract data blocks from the root JSON response
        logger.info("CoordinatorAgent: Extracting and delegating JSON payload blocks.")
        resume_block = raw_json_response.get("resume_analysis", {})
        job_match_block = raw_json_response.get("job_match", {})
        skill_gap_block = raw_json_response.get("skill_gap", [])
        roadmap_block = raw_json_response.get("learning_roadmap", [])
        interview_block = raw_json_response.get("interview_questions", {})
        overall_summary_block = raw_json_response.get("overall_recommendation_summary", "Overall campus placement analysis successfully compiled.")

        # 5. Hand over subsections to specialized sub-agents for parsing & structural safety
        processed_resume = self.resume_agent.process(resume_block)
        processed_job_match = self.job_match_agent.process(job_match_block)
        processed_skill_gap = self.skill_gap_agent.process(skill_gap_block)
        processed_roadmap = self.roadmap_agent.process(roadmap_block)
        processed_interview = self.interview_agent.process(interview_block)

        # 6. Combine validated data into a final coordinated results payload
        combined_payload = {
            "resume_analysis": processed_resume,
            "job_match": processed_job_match,
            "skill_gap": processed_skill_gap,
            "learning_roadmap": processed_roadmap,
            "interview_questions": processed_interview,
            "overall_recommendation_summary": overall_summary_block
        }

        logger.info("CoordinatorAgent: Multi-agent processing complete.")
        return combined_payload
