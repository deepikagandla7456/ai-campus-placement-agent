import logging
from typing import Dict, Any, List
import prompts
from utils.gemini import generate_json_response

logger = logging.getLogger(__name__)

class InterviewAgent:
    """
    Agent responsible for structuring, validating the initial 15 mock interview questions,
    and dynamically evaluating user answers using Gemini during the live interview session.
    """
    def __init__(self) -> None:
        pass

    def process(self, data: Any) -> Dict[str, List[str]]:
        """
        Validates the generated question sets from the coordinator.
        Ensures exactly 5 questions per section (HR, Technical, Behavioral).
        """
        logger.info("InterviewAgent: Verifying mock interview questions array.")

        if not isinstance(data, dict):
            logger.warning("InterviewAgent received invalid question payload. Loading system defaults.")
            data = {}

        hr_qs = self._sanitize_list(data.get("hr"))
        tech_qs = self._sanitize_list(data.get("technical"))
        behavioral_qs = self._sanitize_list(data.get("behavioral"))

        # Enforce exactly 5 questions for each list with standard fallbacks if short
        hr_qs = self._enforce_five_items(hr_qs, "HR", [
            "Tell me about yourself and walk me through your resume.",
            "Why are you interested in joining our company specifically?",
            "What are your core strengths and areas of improvement?",
            "Where do you see yourself five years from now?",
            "How do you prioritize tasks when working under tight deadlines?"
        ])

        tech_qs = self._enforce_five_items(tech_qs, "Technical", [
            "What are the differences between SQL and NoSQL databases?",
            "Explain the concept and practical benefits of polymorphism in OOP.",
            "How do you analyze and optimize the complexity of a slow algorithm?",
            "What is the difference between TCP and UDP protocols?",
            "How does virtual memory work in modern operating systems?"
        ])

        behavioral_qs = self._enforce_five_items(behavioral_qs, "Behavioral", [
            "Tell me about a challenging team project where a conflict arose and how you handled it.",
            "Describe a time you had to learn a complex new skill or framework in a very short time.",
            "Share an example of a mistake or failure in your academic/professional life and what you learned.",
            "Describe a situation where you went above and beyond to deliver a project on time.",
            "How do you handle receiving critical feedback from team members or mentors?"
        ])

        return {
            "hr": hr_qs,
            "technical": tech_qs,
            "behavioral": behavioral_qs
        }

    def _sanitize_list(self, raw_list: Any) -> List[str]:
        if isinstance(raw_list, list):
            return [str(q).strip() for q in raw_list if q and str(q).strip()]
        return []

    def _enforce_five_items(self, questions: List[str], label: str, defaults: List[str]) -> List[str]:
        if len(questions) >= 5:
            return questions[:5]
        else:
            diff = 5 - len(questions)
            logger.info(f"InterviewAgent: Injecting {diff} fallback questions for '{label}' list.")
            return questions + defaults[:diff]

    def evaluate_answer(self, question_type: str, question: str, answer: str) -> Dict[str, Any]:
        """
        Performs a dynamic API evaluation call to score a single answer response.
        """
        logger.info(f"InterviewAgent: Dynamic response evaluation started for type: '{question_type}'")

        if not answer or not answer.strip():
            return {
                "confidence_score": 0,
                "communication_score": 0,
                "technical_accuracy": 0,
                "suggestions": [
                    "Answer field was submitted empty.",
                    "Please formulate a response of at least 2-3 sentences."
                ],
                "feedback": "The candidate did not provide an answer. Prompt evaluation requires written input."
            }

        prompt = prompts.INTERVIEW_EVAL_USER_PROMPT_TEMPLATE.format(
            question_type=question_type,
            question=question,
            candidate_answer=answer.strip()
        )

        try:
            # Query Gemini for the answer evaluation
            res = generate_json_response(
                system_instruction=prompts.INTERVIEW_EVAL_SYSTEM_INSTRUCTION,
                prompt=prompt
            )

            # Sanitize scores
            conf = res.get("confidence_score", 50)
            comm = res.get("communication_score", 50)
            tech = res.get("technical_accuracy", 50)
            try:
                conf = int(conf)
                comm = int(comm)
                tech = int(tech)
            except (ValueError, TypeError):
                conf, comm, tech = 50, 50, 50

            return {
                "confidence_score": max(0, min(100, conf)),
                "communication_score": max(0, min(100, comm)),
                "technical_accuracy": max(0, min(100, tech)),
                "suggestions": self._sanitize_list(res.get("suggestions")) or ["Incorporate clear structured responses (STAR method)."],
                "feedback": str(res.get("feedback", "Feedback generation completed."))
            }

        except Exception as e:
            logger.error(f"InterviewAgent: Evaluation execution failed: {str(e)}")
            return {
                "confidence_score": 50,
                "communication_score": 50,
                "technical_accuracy": 50,
                "suggestions": [
                    "Use quantitative metrics where possible.",
                    "Break down explanations into clear steps."
                ],
                "feedback": f"Evaluation system was unable to analyze this response. Context: {str(e)}"
            }
