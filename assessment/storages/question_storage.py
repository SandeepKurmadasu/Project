from assessment.interactors.dtos import QuestionDTO, UpdateQuestionDTO, CreateQuestionDTO, QuestionTypeDTO, Difficulty
from assessment.interactors.questions.create_question_factory import CreateQuestionFactory
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface
from assessment.models import Question


class QuestionStorage(QuestionStorageInterface):


    def create_questions(self, questions: list[CreateQuestionDTO]) -> list[QuestionDTO]:
        models = CreateQuestionFactory.bulk_create_questions(questions)
        created_questions = Question.objects.bulk_create(models,ignore_conflicts=False)
        print(f"Created questions: {created_questions}")
        for q in created_questions:
            print(f"Question ID: {q.question_id}, Text: {q.question_text}")

        dtos = []
        for q in created_questions:
            if q.question_id is None:
                print(f"WARNING: question_id is None for {q.question_text}")

            dtos.append(
                QuestionDTO(
                    question_id=str(q.question_id),
                    question_text=q.question_text,
                    question_type=q.question_type,
                    difficulty_level=q.difficulty,
                    options=q.options,
                    correct_answer=q.correct_answer,
                )
            )
        return dtos

    def get_questions(self,question_ids:list[str]) ->list[QuestionDTO]:
        questions=Question.objects.filter(question_id__in=question_ids)

        dtos = []
        for q in questions:

            dtos.append(
                QuestionDTO(
                    question_id=str(q.question_id),
                    question_text=q.question_text,
                    question_type=QuestionTypeDTO(q.question_type),
                    difficulty_level=Difficulty(q.difficulty),
                    options=q.options,
                    correct_answer=q.correct_answer,
                )
            )
        return dtos

    def update_questions(self,questions: list[UpdateQuestionDTO]) ->list[QuestionDTO]:
        question_ids = [each_question.question_id for each_question in questions]
        question_objects = list(Question.objects.filter(question_id__in=question_ids))

        dto_map = {str(dto.question_id): dto for dto in questions}

        for question_obj in question_objects:
            dto = dto_map[str(question_obj.question_id)]
            question_obj.question_type=dto.question_type
            question_obj.question_text=dto.question_text
            question_obj.correct_answer=dto.correct_answer
            question_obj.difficulty=dto.difficulty
            question_obj.options=dto.options

        Question.objects.bulk_update(question_objects,
                                     fields=["question_type","question_text","correct_answer","difficulty","options"])


        return [
            QuestionDTO(
                    question_id=str(q.question_id),
                    question_text=q.question_text,
                    question_type=QuestionTypeDTO(q.question_type),
                    difficulty_level=Difficulty(q.difficulty),
                    options=q.options,
                    correct_answer=q.correct_answer,
            )
            for q in question_objects
        ]