import json
import pytest

from assessment.storages.question_bank_question_storage import QuestionBankQuestionStorage
from assessment.models import QuestionBank, Question, QuestionBankQuestion, Assessment



def create_assessment():
    return Assessment.objects.create(
        title="Test Assessment",
        assessment_type="QUIZ",
        description="Test description",
        no_of_questions=1,
        pass_percentage=50,
        estimated_duration_in_minutes=10,
    )


def dto_to_json(dto):
    d = dto.__dict__.copy()
    d["bank_id"] = "STATIC-BANK-ID"

    if "questions" in d:
        cleaned_questions = []
        for q in d["questions"]:
            q_dict = q.__dict__.copy()
            q_dict["question_id"] = "STATIC-QUESTION-ID"
            cleaned_questions.append(q_dict)
        d["questions"] = cleaned_questions

    return d


def question_dto_to_json(dto):
    d = dto.__dict__.copy()
    d["question_id"] = "STATIC-QUESTION-ID"
    return d



@pytest.mark.django_db
def test_remove_question_from_bank(snapshot):
    assessment = create_assessment()

    bank = QuestionBank.objects.create(title="Test Bank", assessment=assessment)

    question = Question.objects.create(
        question_text="What is Python?",
        question_type="MCQ_SINGLE",
        difficulty="EASY",
        options=[{"1": "Programming language"}, {"2": "Snake"}, {"3": "Tool"}, {"4": "Framework"}],
        correct_answer=["1"]
    )

    QuestionBankQuestion.objects.create(
        question_bank=bank,
        question=question,
        order=1
    )

    storage = QuestionBankQuestionStorage()
    result = storage.remove_question_from_bank(
        bank_id=str(bank.bank_id),
        question_ids=[str(question.question_id)]
    )

    snapshot.assert_match(
        json.dumps(dto_to_json(result), sort_keys=True, indent=2),
        "test_remove_question_from_bank"
    )


@pytest.mark.django_db
def test_reorder_questions_in_bank(snapshot):
    assessment = create_assessment()

    bank = QuestionBank.objects.create(title="Test Bank", assessment=assessment)

    q1 = Question.objects.create(
        question_text="Question 1",
        question_type="MCQ_SINGLE",
        difficulty="EASY",
        options=[{"1": "Option A"}, {"2": "Option B"}],
        correct_answer=["1"]
    )

    q2 = Question.objects.create(
        question_text="Question 2",
        question_type="MCQ_SINGLE",
        difficulty="MEDIUM",
        options=[{"1": "Option X"}, {"2": "Option Y"}],
        correct_answer=["2"]
    )

    QuestionBankQuestion.objects.create(question_bank=bank, question=q1, order=1)
    QuestionBankQuestion.objects.create(question_bank=bank, question=q2, order=2)

    storage = QuestionBankQuestionStorage()
    result = storage.reorder_questions_in_bank(
        bank_id=str(bank.bank_id),
        ordered_question_ids=[
            str(q2.question_id),
            str(q1.question_id)
        ]
    )

    snapshot.assert_match(
        json.dumps(dto_to_json(result), sort_keys=True, indent=2),
        "test_reorder_questions_in_bank"
    )


@pytest.mark.django_db
def test_add_questions_to_bank_ordered(snapshot):
    assessment = create_assessment()

    bank = QuestionBank.objects.create(title="Test Bank", assessment=assessment)

    question = Question.objects.create(
        question_text="What is Django?",
        question_type="MCQ_SINGLE",
        difficulty="MEDIUM",
        options=[{"1": "Framework"}, {"2": "Language"}],
        correct_answer=["1"]
    )

    storage = QuestionBankQuestionStorage()
    result = storage.add_questions_to_bank_ordered(
        bank_id=str(bank.bank_id),
        ordered_ids=[{
            "question_id": question.question_id,
            "order": 1
        }]
    )

    snapshot.assert_match(
        json.dumps(dto_to_json(result), sort_keys=True, indent=2),
        "test_add_questions_to_bank_ordered"
    )


@pytest.mark.django_db
def test_get_bank_questions(snapshot):
    assessment = create_assessment()

    bank = QuestionBank.objects.create(title="Test Bank", assessment=assessment)

    question = Question.objects.create(
        question_text="Capital of India?",
        question_type="MCQ_SINGLE",
        difficulty="EASY",
        options=[{"1": "Delhi"}, {"2": "Mumbai"}],
        correct_answer=["1"]
    )

    QuestionBankQuestion.objects.create(question_bank=bank, question=question, order=1)

    storage = QuestionBankQuestionStorage()
    result = storage.get_bank_questions(str(bank.bank_id))

    cleaned = [question_dto_to_json(r) for r in result]

    snapshot.assert_match(
        json.dumps(cleaned, sort_keys=True, indent=2),
        "test_get_bank_questions"
    )
