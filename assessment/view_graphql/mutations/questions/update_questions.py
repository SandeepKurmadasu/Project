import graphene

from assessment.models.models import Difficulty,QuestionType
from assessment.view_graphql.types.input_types import UpdateQuestionParams
from assessment.view_graphql.types.types import QuestionsType, QuestionTyped
from assessment.view_graphql.types.error_types import (
QuestionNotFounded,DuplicateQuestionIds,UnExpectedQuestionType,UnExpectedDifficulty
)

from assessment.view_graphql.types.response_types import UpdateQuestionsResponse
from assessment.interactors.questions.update_questions_interactor import UpdateQuestionInteractor
from assessment.storages.question_storage import QuestionStorage
from assessment.interactors.dtos import UpdateQuestionDTO
from assessment.exceptions.custom_exceptions import DuplicateQuestionIdsFound,UnexpectedDifficultyFound,UnexpectedQuestionTypeFound, QuestionNotFound


class UpdateQuestions(graphene.Mutation):
    class Arguments:
        params = UpdateQuestionParams(required=True)
    Output=UpdateQuestionsResponse

    @staticmethod
    def mutate(root, info, params):

        try:
            question_type = QuestionType(params.question_type) if params.question_type else None
            difficulty = Difficulty(params.difficulty) if params.difficulty else None

            dto = UpdateQuestionDTO(
                question_id=params.question_id,
                correct_answer=params.correct_answer,
                question_text=params.question_text,
                options=params.options,
                question_type=question_type,
                difficulty=difficulty,
            )

            updated_questions = UpdateQuestionInteractor(
                question_storage=QuestionStorage()
            ).update_questions([dto])

            questions= [
                QuestionTyped(
                    question_id=uq.question_id,
                    question_text = uq.question_text,
                    question_type =  uq.question_type,
                    difficulty_level = uq.difficulty_level,
                    correct_answer = uq.correct_answer,
                    options = uq.options
                )
                for uq in updated_questions
            ]

            return QuestionsType(question_ids=questions)

        except DuplicateQuestionIdsFound as e:
            return DuplicateQuestionIds(questions=e.question_ids)
        except UnexpectedDifficultyFound as e:
            return UnExpectedDifficulty(questions=e.difficulties)
        except UnexpectedQuestionTypeFound as e:
            return UnExpectedQuestionType(questions=e.question_type)
        except QuestionNotFound as e:
            return QuestionNotFounded(questions=e.question_ids)


