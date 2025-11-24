import graphene
from django.db import IntegrityError
from graphql import GraphQLError

from assessment.view_graphql.types.input_types import AddQuestionsToBank
from assessment.view_graphql.types.error_types import DuplicateQuestionIds, BankNotFound, CheckQuestionExist, QuestionsAlreadyBank
from assessment.view_graphql.types.response_types import AddQuestionsToBankResponse
from assessment.view_graphql.types.types import QuestionBankQuestionType
from assessment.interactors.questionbank.add_questions_to_bank_interactor import AddQuestionsToBankInteractor
from assessment.storages.question_bank_question_storage import QuestionBankQuestionStorage
from assessment.storages.question_bank_storage import QuestionBankStorage
from assessment.storages.question_storage import QuestionStorage
from assessment.exceptions.custom_exceptions import DuplicateQuestionIdsFound, QuestionBankNotFound, QuestionNotFound, QuestionAlreadyInBank



class AddingQuestionsToBank(graphene.Mutation):
    class Arguments:
        params = AddQuestionsToBank(required=True)

    Output = AddQuestionsToBankResponse

    @staticmethod
    def mutate(root, info, params):

        try:
            interactor = AddQuestionsToBankInteractor(
                question_storage=QuestionStorage(),
                question_bank_storage=QuestionBankStorage(),
                question_bank_question_storage=QuestionBankQuestionStorage(),
            )

            dto = interactor.add_questions_to_bank(
                bank_id=params.bank_id,
                question_ids=params.question_ids
            )

            return QuestionBankQuestionType(
                bank_id=dto.bank_id,
                question_ids=[q.question_id for q in dto.questions]
            )

        except DuplicateQuestionIdsFound as e:
            return DuplicateQuestionIds(questions=e.question_ids)

        except QuestionBankNotFound as e:
            return BankNotFound(bank_id=e.bank_id)

        except QuestionNotFound as e:
            return CheckQuestionExist(questions=e.question_ids)

        except QuestionAlreadyInBank as e:
            return QuestionsAlreadyBank(question_ids=e.question_ids)

        except IntegrityError:
            raise GraphQLError("Order number already exists in this question bank.")
