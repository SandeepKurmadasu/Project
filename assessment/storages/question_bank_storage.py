from assessment.exceptions.custom_exceptions import AssessmentIdNotFound
from assessment.interactors.dtos import QuestionBankDTO
from assessment.interactors.storage_interface.question_bank_storage_interface import QuestionBankStorageInterface
from assessment.models import QuestionBank, Assessment


class QuestionBankStorage(QuestionBankStorageInterface):

    def get_question_bank(self, bank_id: str) -> QuestionBankDTO:
        bank = QuestionBank.objects.filter(bank_id=bank_id).first()

        return QuestionBankDTO(
            bank_id=bank.bank_id,
            name=bank.title,
            assessment_id=bank.assessment.assessment_id,
            created_at=bank.created_at,
            updated_at=bank.updated_at
        )

    def get_question_bank_by_name(self, name: str) -> QuestionBankDTO:
        question = QuestionBank.objects.filter(title=name).first()
        if question is None:
            return None

        return QuestionBankDTO(
            name=question.title,
            bank_id=question.bank_id,
            assessment_id=question.assessment.assessment_id,
            created_at=question.created_at,
            updated_at=question.updated_at
        )

    def create_question_bank_for_assessment(self, name: str, assessment_id: str) -> QuestionBankDTO:
        assessments = Assessment.objects.filter(assessment_id=assessment_id).first()
        if assessments is None:
            raise AssessmentIdNotFound(assessment_id)

        bank = QuestionBank.objects.create(
            title=name,
            assessment=assessments
        )

        return QuestionBankDTO(
            bank_id=str(bank.bank_id),
            name=bank.title,
            assessment_id=str(assessments.assessment_id),
            created_at=bank.created_at.isoformat(),
            updated_at=bank.updated_at.isoformat(),
        )

    def get_assessment_question_bank(self, assessment_id: str) -> QuestionBankDTO:
        bank = QuestionBank.objects.filter(assessment__assessment_id=assessment_id).first()

        return QuestionBankDTO(
            bank_id=str(bank.bank_id),
            name=bank.title,
            assessment_id=bank.assessment.assessment_id,
            created_at=bank.created_at,
            updated_at=bank.updated_at
        )
