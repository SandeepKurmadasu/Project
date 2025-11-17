from assessment.interactors.dtos import QuestionDTO, UpdateQuestionDTO, CreateQuestionDTO, QuestionType, Difficulty
from assessment.interactors.questions.create_question_factory import CreateQuestionFactory
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface
from assessment.models import Question


class QuestionStorage(QuestionStorageInterface):


    def create_questions(self, questions: list[CreateQuestionDTO]) -> list[QuestionDTO]:
        models = CreateQuestionFactory.bulk_create_questions(questions)
        created_questions = Question.objects.bulk_create(models)

        dtos = []
        for q in created_questions:
            if q.question_type in ["MCQ_SINGLE", "MCQ_MULTI"]:
                correct_answer = q.correct_option_ids
                options = q.options
            elif q.question_type == "TRUE_FALSE":
                correct_answer = q.correct_boolean
                options = None
            elif q.question_type == "FILL_BLANK":
                correct_answer = q.correct_fill_text
                options = None
            elif q.question_type == "MATCH_PAIRS":
                correct_answer = q.options.get("correct_pairs") if q.options else None
                options = q.options
            else:
                correct_answer = None
                options = None

            dtos.append(
                QuestionDTO(
                    question_id=str(q.question_id),
                    question_text=q.question_text,
                    question_type=q.question_type,
                    difficulty_level=q.difficulty,
                    options=options,
                    correct_answer=correct_answer,
                )
            )
        return dtos

    def get_questions(self,question_ids:list[str]) ->list[QuestionDTO]:
        questions=Question.objects.filter(id__in=question_ids)

        dtos = []
        for q in questions:
            if q.question_type in ["MCQ_SINGLE", "MCQ_MULTI"]:
                correct_answer = q.correct_option_ids
                options = q.options
            elif q.question_type == "TRUE_FALSE":
                correct_answer = q.correct_boolean
                options = None
            elif q.question_type == "FILL_BLANK":
                correct_answer = q.correct_fill_text
                options = None
            elif q.question_type == "MATCH_PAIRS":
                correct_answer = q.options.get("correct_pairs") if q.options else None
                options = q.options
            else:
                correct_answer = None
                options = None

            dtos.append(
                QuestionDTO(
                    question_id=str(q.question_id),
                    question_text=q.question_text,
                    question_type=QuestionType(q.question_type),
                    difficulty_level=Difficulty(q.difficulty),
                    options=options,
                    correct_answer=correct_answer,
                )
            )
        return dtos

    def update_questions(self,questions: list[UpdateQuestionDTO]) ->list[QuestionDTO]:
        questions = Question.objects.filter(id__in=questions)

        dtos = []
        for q in questions:
            question=q.question_type

            if question in ["MCQ_SINGLE", "MCQ_MULTI"]:
                correct_answer = q.correct_option_ids
                options = q.options
            elif question  == "TRUE_FALSE":
                correct_answer = q.correct_boolean
                options = None
            elif (
                question == "FILL_BLANK"):
                correct_answer = q.correct_fill_text
                options = None
            elif question == "MATCH_PAIRS":
                correct_answer = q.options.get("correct_pairs") if q.options else None
                options = q.options
            else:
                correct_answer = None
                options = None

            dtos.append(
                QuestionDTO(
                    question_id=str(q.question_id),
                    question_text=q.question_text,
                    question_type=QuestionType(q.question_type),
                    difficulty_level=Difficulty(q.difficulty),
                    options=options,
                    correct_answer=correct_answer,
                )
            )
        return dtos
