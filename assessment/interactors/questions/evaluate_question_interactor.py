from assessment.interactors.dtos import EvaluateQuestionDTO
from assessment.interactors.questions.evaluate_strategy_pattern import QuestionStrategy
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface
from assessment.exceptions.custom_exceptions import QuestionNotFound

class EvaluateQuestionInteractor:
    def __init__(self, storage: QuestionStorageInterface):
        self.storage = storage

    def evaluate(self, question_id: str, user_answer) -> EvaluateQuestionDTO:
        question_list = self.storage.get_questions([question_id])
        if not question_list:
            raise QuestionNotFound([question_id])
        question=question_list[0]

        strategy = QuestionStrategy.get_strategy(question.question_type)
        return strategy.evaluate(user_answer, question.correct_answer)