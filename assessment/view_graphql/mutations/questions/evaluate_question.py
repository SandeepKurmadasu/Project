import graphene

from assessment.view_graphql.types.error_types import QuestionNotFoundError, EvaluationError
from assessment.view_graphql.types.input_types import EvaluateQuestionInput
from assessment.view_graphql.types.response_types import EvaluateQuestionResponse
from assessment.view_graphql.types.types import EvaluateQuestionType
from assessment.interactors.evaluate_questions.evaluate_question_interactor import EvaluateQuestionInteractor
from assessment.storages.question_storage import QuestionStorage


class EvaluateQuestion(graphene.Mutation):
    class Arguments:
        params = EvaluateQuestionInput(required=True)

    Output = EvaluateQuestionResponse

    @staticmethod
    def mutate(root, info, params):
        try:
            interactor = EvaluateQuestionInteractor(
                storage=QuestionStorage()
            )

            dto = interactor.evaluate(
                question_id=params.question_id,
                user_answer=params.user_answer
            )

            return EvaluateQuestionType(
                status=dto.is_correct.value,
                correct_count=dto.correct_count,
                total_count=dto.total_count
            )

        except IndexError:
            return QuestionNotFoundError(question_id=params.question_id)

        except Exception as e:
            return EvaluationError(message=str(e))
