import graphene

from assessment.exceptions.custom_exceptions import QuestionBankNotFound, QuestionNotInBank
from assessment.view_graphql.types.error_types import BankNotFound, QuestionNotInBankError
from assessment.view_graphql.types.input_types import ReorderQuestionsInput
from assessment.view_graphql.types.response_types import ReorderQuestionsResponse
from assessment.view_graphql.types.types import QuestionBankQuestionType
from assessment.interactors.questionbank.reorder_questions_interactor import ReorderQuestionsInteractor
from assessment.storages.question_bank_question_storage import QuestionBankQuestionStorage
from assessment.storages.question_bank_storage import QuestionBankStorage


class ReorderQuestionsMutation(graphene.Mutation):
    class Arguments:
        params = ReorderQuestionsInput(required=True)

    Output = ReorderQuestionsResponse

    @staticmethod
    def mutate(root, info, params):
        try:
            interactor = ReorderQuestionsInteractor(
                question_bank_storage=QuestionBankStorage(),
                question_bank_question_storage=QuestionBankQuestionStorage(),
            )

            dto = interactor.reorder_questions(
                bank_id=params.bank_id,
                ordered_question_ids=params.question_ids
            )

            return QuestionBankQuestionType(
                bank_id=dto.bank_id,
                question_ids=[q.question_id for q in dto.questions]
            )

        except QuestionBankNotFound as e:
            return BankNotFound(bank_id=e.bank_id)

        except QuestionNotInBank as e:
            return QuestionNotInBankError(
                bank_id=e.bank_id,
                question_ids=e.question_ids
            )
    # @staticmethod
    # def mutate(root, info, params):
    #     try:
    #         interactor = ReorderQuestionsInteractor(
    #             question_bank_storage=QuestionBankStorage(),
    #             question_bank_question_storage=QuestionBankQuestionStorage(),
    #         )
    #
    #         dto = interactor.reorder_questions(
    #             bank_id=params.bank_id,
    #             ordered_question_ids=params.question_ids
    #         )
    #
    #         return QuestionBankQuestionType(
    #             bank_id=dto.bank_id,
    #             question_ids=[q.question_id for q in dto.questions]
    #         )
    #
    #     except Exception as e:
    #         raise e

