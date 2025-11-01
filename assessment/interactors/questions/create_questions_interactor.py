from assessment.interactors.common_validation_mixin import ValidationMixIns
from assessment.interactors.dtos import QuestionDTO,CreateQuestionDTO
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface
from assessment.interactors.questions.create_question_factory import QuestionFactory


class CreateQuestionsInteractor(ValidationMixIns):

    def __init__(self,question_storage: QuestionStorageInterface):
        self.question_storage=question_storage

    def create_questions(self,questions:list[CreateQuestionDTO])-> list[QuestionDTO]:
        self.check_duplicate_question_texts(questions=questions)
        self.check_invalid_question_type(questions=questions)
        self.check_invalid_difficulty(questions=questions)

        question_objects = QuestionFactory.bulk_create_questions(questions)

        created_questions = self.question_storage.create_questions(question_objects)

        return created_questions
