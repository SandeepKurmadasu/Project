import graphene

from assessment.exceptions.custom_exceptions import DuplicateBankNameFound, AssessmentIdNotFound
from assessment.graphql.types import DuplicateBankName, AssessmentIdNotFounded
from assessment.graphql.types.input_types import CreateQuestionBankParams
from assessment.graphql.types.response_types import CreateQuestionBankResponse
from assessment.graphql.types.types import QuestionBankType
from assessment.interactors.questionbank.create_question_bank_interactor import CreateQuestionBankInteractor
from assessment.storages.assessment_storage import AssessmentStorage
from assessment.storages.question_bank_storage import QuestionBankStorage


class CreateQuestionBank(graphene.Mutation):
    class Arguments:
        question_bank = CreateQuestionBankParams(required=True)

    Output = CreateQuestionBankResponse

    @staticmethod
    def mutate(root, info, question_bank):

        try:
            interactor = CreateQuestionBankInteractor(
                question_bank_storage=QuestionBankStorage(),
                assessment_storage=AssessmentStorage()
            )

            created_bank = interactor.create_question_bank(
                name=question_bank.name,
                assessment_id=question_bank.assessment_id
            )

            return QuestionBankType(
                bank_id=created_bank.bank_id,
                name=created_bank.name,
                assessment_id=created_bank.assessment_id,
                created_at=created_bank.created_at,
                updated_at=created_bank.updated_at
            )

        except DuplicateBankNameFound as e:
            return DuplicateBankName(name=e.name)

        except AssessmentIdNotFound as e:
            return AssessmentIdNotFounded(assessment_id=e.assessment_id)
