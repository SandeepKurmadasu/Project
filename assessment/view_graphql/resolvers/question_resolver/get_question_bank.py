import graphene
from assessment.view_graphql.types.types import QuestionBankType
from assessment.view_graphql.types.error_types import BankNotFound
from assessment.interactors.questionbank.get_question_bank_interactor import GetQuestionBankInteractor
from assessment.storages.question_bank_storage import QuestionBankStorage
from  assessment.exceptions.custom_exceptions import QuestionBankNotFound


def resolve_get_question_bank(root, info, params):
    try:
        dto = GetQuestionBankInteractor(storage=QuestionBankStorage()).get_question_bank(params.bank_id)

        bank = QuestionBankType(
            bank_id=dto.bank_id,
            name=dto.name,
            assessment_id=dto.assessment_id,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

        return bank

    except QuestionBankNotFound as e:
        return BankNotFound(bank_id=e.bank_id)

