import graphene
from assessment.view_graphql.types.input_types import  CreateQuestionInput
from assessment.view_graphql.types.types import QuestionTyped, QuestionsType

from assessment.interactors.questions.create_questions_interactor import CreateQuestionsInteractor, CreateQuestionDTO
from assessment.storages.question_storage import QuestionStorage
from assessment.exceptions.custom_exceptions import (
    UnexpectedQuestionTypeFound,
    UnexpectedDifficultyFound
)
from assessment.view_graphql.types.error_types import UnExpectedQuestionType, UnExpectedDifficulty
from assessment.view_graphql.types.response_types import CreateQuestionsResponse
from assessment.interactors.dtos import QuestionTypeDTO, Difficulty


class CreateQuestions(graphene.Mutation):
    class Arguments:
        questions = graphene.List(CreateQuestionInput, required=True)

    Output=CreateQuestionsResponse

    @staticmethod
    def mutate(root, info, questions):

        try:

            dtos = [
                CreateQuestionDTO(
                    question_text=q.question_text,
                    question_type=QuestionTypeDTO(q.question_type.value),
                    difficulty=Difficulty(q.difficulty.value),
                    correct_answer=q.correct_answer,
                    options=q.options
                )
                for q in questions
            ]


            interactor = CreateQuestionsInteractor(question_storage=QuestionStorage())
            created_questions = interactor.create_questions(dtos)



            question_objs = [
                QuestionTyped(
                    question_id=cd.question_id,
                    question_type=cd.question_type,
                    difficulty_level=cd.difficulty_level,
                    question_text=cd.question_text,
                    correct_answer=cd.correct_answer,
                    options=cd.options
                )
                for cd in created_questions
            ]

            return QuestionsType(question_ids=question_objs)


        except UnexpectedQuestionTypeFound as e:
            print(f"\nCaught UnexpectedQuestionTypeFound: {e.types}")
            return UnExpectedQuestionType(types=e.types)
        except UnexpectedDifficultyFound as e:
            print(f"\nCaught UnexpectedDifficultyFound: {e.difficulty_level}")
            return UnExpectedDifficulty(difficulty=e.difficulty_level)
        except Exception as e:
            print(f"\n!!! UNEXPECTED EXCEPTION !!!")
            print(f"Type: {type(e)}")
            print(f"Message: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
