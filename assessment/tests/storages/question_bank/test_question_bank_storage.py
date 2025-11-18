import json
import pytest

from assessment.storages.question_bank_storage import QuestionBankStorage
from assessment.tests.factories.assessment_factory import AssessmentFactory
from assessment.models import QuestionBank


def clean_bank(dto):
    d = dto.__dict__.copy()

    d["bank_id"] = "BANK_ID"
    d["assessment_id"] = "ASSESSMENT_ID"

    d["created_at"] = "2025-01-01T00:00:00Z"
    d["updated_at"] = "2025-01-01T00:00:00Z"

    return d


@pytest.mark.django_db
def test_create_question_bank_for_assessment(snapshot):
    assessment = AssessmentFactory()

    storage = QuestionBankStorage()
    result = storage.create_question_bank_for_assessment(
        name="Bank A",
        assessment_id=str(assessment.assessment_id)
    )

    snapshot.assert_match(
        json.dumps(clean_bank(result), indent=2, sort_keys=True),
        "create_question_bank_for_assessment"
    )


@pytest.mark.django_db
def test_get_question_bank(snapshot):
    assessment = AssessmentFactory()
    bank = QuestionBank.objects.create(title="Bank A", assessment=assessment)

    storage = QuestionBankStorage()
    result = storage.get_question_bank(str(bank.bank_id))

    snapshot.assert_match(
        json.dumps(clean_bank(result), indent=2, sort_keys=True),
        "get_question_bank"
    )


@pytest.mark.django_db
def test_get_question_bank_by_name(snapshot):
    assessment = AssessmentFactory()
    QuestionBank.objects.create(title="Bank ABC", assessment=assessment)

    storage = QuestionBankStorage()
    result = storage.get_question_bank_by_name("Bank ABC")

    snapshot.assert_match(
        json.dumps(clean_bank(result), indent=2, sort_keys=True),
        "get_question_bank_by_name"
    )


@pytest.mark.django_db
def test_get_assessment_question_bank(snapshot):
    assessment = AssessmentFactory()
    QuestionBank.objects.create(title="Bank Z", assessment=assessment)

    storage = QuestionBankStorage()
    result = storage.get_assessment_question_bank(str(assessment.assessment_id))

    snapshot.assert_match(
        json.dumps(clean_bank(result), indent=2, sort_keys=True),
        "get_assessment_question_bank"
    )
