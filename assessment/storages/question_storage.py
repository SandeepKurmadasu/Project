from assessment.interactors.dtos import CreateQuestionDTO, QuestionDTO
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface


class QuestionStorage(QuestionStorageInterface):

    def create_questions(self,questions: list[CreateQuestionDTO]) ->list[QuestionDTO]:
        pass

    def get_questions(self,question_ids:list[str]) ->list[QuestionDTO]:
        pass