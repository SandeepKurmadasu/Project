from typing import Any
from assessment.interactors.dtos import EvaluateQuestionDTO
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface
from assessment.exceptions.custom_exceptions import QuestionNotFound  # optional custom exception

class EvaluateQuestionInteractor:
    def __init__(self, storage: QuestionStorageInterface):
        self.storage = storage

    def evaluate(self, question_id: str, answer: Any) -> EvaluateQuestionDTO:
        if answer is None:
            return EvaluateQuestionDTO(is_correct=False)

        questions = self.storage.get_questions(question_ids=[question_id])
        if not questions:
            raise QuestionNotFound

        question = questions[0]
        correct = question.correct_answer
        is_correct = False

        if question.question_type == "MCQ_SINGLE":
            is_correct = answer == correct

        elif question.question_type == "MCQ_MULTI":
            user_set = {a.strip() for a in answer.split(",")} if isinstance(answer, str) and answer else set()
            correct_set = {c.strip() for c in correct.split(",")} if correct else set()
            is_correct = user_set == correct_set

        elif question.question_type == "TRUE_FALSE":
            is_correct = str(answer).lower() == str(correct).lower()

        elif question.question_type == "FILL_BLANK":
            is_correct = str(answer).strip().lower() == str(correct).strip().lower()

        elif question.question_type == "MATCH_PAIRS":
            correct_pairs = {}
            if correct:
                for pair in correct.split(","):
                    if ":" in pair:
                        left, right = pair.split(":", 1)
                        correct_pairs[left.strip()] = right.strip()

            user_pairs = {}
            if isinstance(answer, str):
                for pair in answer.split(","):
                    if ":" in pair:
                        left, right = pair.split(":", 1)
                        user_pairs[left.strip()] = right.strip()
            elif isinstance(answer, dict):
                user_pairs = answer

            is_correct = user_pairs == correct_pairs

        return EvaluateQuestionDTO(is_correct=is_correct)