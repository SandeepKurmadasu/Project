from typing import Any
from assessment.interactors.dtos import QuestionDTO, EvaluateQuestionDTO
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface


class EvaluateQuestionInteractor:
    def __init__(self, storage: QuestionStorageInterface):
        self.storage = storage

    @staticmethod
    def evaluate(question: QuestionDTO, answer: Any) -> EvaluateQuestionDTO:
        if answer is None:
            return EvaluateQuestionDTO(is_correct=False)

        correct = question.correct_answer
        is_correct = False

        if question.question_type == "MCQ_SINGLE":
            is_correct = str(answer) == correct

        elif question.question_type == "MCQ_MULTI":
            user_set = set(str(a) for a in (answer or []))
            correct_set = set(correct.split(",")) if correct else set()
            is_correct = user_set == correct_set

        elif question.question_type == "TRUE_FALSE":
            is_correct = str(answer).lower() == correct.lower()

        elif question.question_type == "FILL_BLANK":
            is_correct = str(answer).strip().lower() == correct.strip().lower()

        elif question.question_type == "MATCH_PAIRS":
            correct_pairs = {}
            if correct:
                for pair in correct.split(","):
                    if pair:
                        left, right = pair.split(":")
                        correct_pairs[left] = right
            user_pairs = answer or {}
            is_correct = user_pairs == correct_pairs

        return EvaluateQuestionDTO(is_correct=is_correct)