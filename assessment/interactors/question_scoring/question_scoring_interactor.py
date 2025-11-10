from assessment.interactors.dtos import QuestionWithEvaluationDTO, ScoringConfigDTO
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface


class GetScoreForQuestionInteractor:
    def __init__(self, storage: QuestionStorageInterface):
        self.storage = storage

    @staticmethod
    def get_score(current_question: QuestionWithEvaluationDTO, config: ScoringConfigDTO) -> int:

        if current_question.evaluation_result:
            return config.marks_if_correct
        else:
            return config.marks_if_wrong

