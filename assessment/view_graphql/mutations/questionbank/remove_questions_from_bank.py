import graphene
from graphql import GraphQLError

from assessment.view_graphql.types.input_types import RemoveQuestionsFromBankInput
from assessment.view_graphql.types.error_types import BankNotFound, CheckQuestionExist, QuestionNotInBankError
from assessment.view_graphql.types.response_types import RemoveQuestionsFromBankResponse
from assessment.view_graphql.types.types import QuestionBankQuestionType

from assessment.interactors.questionbank.remove_question_from_bank_interactor import RemoveQuestionFromBankInteractor
from assessment.storages.question_bank_question_storage import QuestionBankQuestionStorage
from assessment.storages.question_bank_storage import QuestionBankStorage
from assessment.storages.question_storage import QuestionStorage

from assessment.exceptions.custom_exceptions import (
    QuestionBankNotFound,
    QuestionNotFound,
    QuestionNotInBank
)


class RemoveQuestionFromBank(graphene.Mutation):
    class Arguments:
        params = RemoveQuestionsFromBankInput(required=True)

    Output = RemoveQuestionsFromBankResponse

    @staticmethod
    def mutate(root, info, params):

        try:
            interactor = RemoveQuestionFromBankInteractor(
                question_storage=QuestionStorage(),
                question_bank_storage=QuestionBankStorage(),
                question_bank_question_storage=QuestionBankQuestionStorage(),
            )

            dto = interactor.remove_question_from_bank(
                bank_id=params.bank_id,
                question_ids=params.question_ids
            )

            return QuestionBankQuestionType(
                bank_id=dto.bank_id,
                question_ids=[q.question_id for q in dto.questions]
            )

        except QuestionBankNotFound as e:
            return BankNotFound(bank_id=e.bank_id)

        except QuestionNotFound as e:
            return CheckQuestionExist(questions=e.question_ids)

        except QuestionNotInBank as e:
            return QuestionNotInBankError(
                bank_id=e.bank_id,
                question_ids=e.question_ids
            )

        except Exception as e:
            raise GraphQLError(f"Unexpected error: {str(e)}")
