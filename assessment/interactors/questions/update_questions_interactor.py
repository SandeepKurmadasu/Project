from assessment.interactors.common_validation_mixin import ValidationMixIns
from assessment.interactors.dtos import UpdateQuestionDTO, QuestionDTO
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface

class UpdateQuestionInteractor(ValidationMixIns):

    def __init__(self,question_storage:QuestionStorageInterface):
        self.question_storage=question_storage

    def update_questions(self,questions:list[UpdateQuestionDTO])->  list[QuestionDTO]:
        question_ids=[obj.question_id for obj in questions]
        self.check_duplicate_question_ids(question_ids=question_ids)
        self.check_if_question_ids_exists_in_db(question_ids=question_ids,question_storage=self.question_storage)
        return self.question_storage.update_questions(questions=questions)
