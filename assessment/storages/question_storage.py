from assessment.interactors.dtos import QuestionDTO, UpdateQuestionDTO, CreateQuestionDTO
from assessment.interactors.questions.create_question_factory import CreateQuestionFactory
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface
from assessment.models import Question


class QuestionStorage(QuestionStorageInterface):

    def create_questions(self, questions: list[CreateQuestionDTO]) -> list[QuestionDTO]:
        models = CreateQuestionFactory.bulk_create_questions(questions)
        created_questions = Question.objects.bulk_create(models)


        return [
            QuestionDTO(
                question_id=str(q.id),
                question_text=q.question_text,
                question_type=q.question_type,
                difficulty_level=q.difficulty,
                options=q.options,
                correct_answer=q.correct_option_ids,
            )
            for q in created_questions
        ]

    def get_questions(self,question_ids:list[str]) ->list[QuestionDTO]:
        questions=Question.objects.filter(question_id__in=question_ids)
        question_dtos=[
            QuestionDTO(
                question_id=q.id,
                question_text=q.question_text,
                question_type=q.question_type,
                difficulty_level=q.difficulty,
                options=q.options,
                correct_answer=q.correct_option_ids,
                )
            for q in questions
        ]
        return question_dtos

    def update_questions(self,questions: list[UpdateQuestionDTO]) ->list[QuestionDTO]:
        pass

