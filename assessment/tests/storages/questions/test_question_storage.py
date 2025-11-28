import json
import pytest
from assessment.tests.factories.storage_factories import QuestionFactory
from assessment.storages.question_storage import QuestionStorage
from assessment.interactors.dtos import (
    CreateQuestionDTO,
    UpdateQuestionDTO,
    QuestionTypeDTO,
    Difficulty,
)


def dto_to_json(dto):
    d = dto.__dict__.copy()
    if hasattr(d.get("question_type"), "value"):
        d["question_type"] = d["question_type"].value
    if hasattr(d.get("difficulty_level"), "value"):
        d["difficulty_level"] = d["difficulty_level"].value
    d["question_id"] = "STATIC-ID"
    return d


@pytest.fixture
def question_storage():
    return QuestionStorage()


@pytest.mark.django_db
def test_create_questions(question_storage, snapshot):
    payload = [
        CreateQuestionDTO(
            question_text="What is Python?",
            question_type=QuestionTypeDTO.MCQ_SINGLE,
            difficulty=Difficulty.EASY,
            options=[{"1": "Programming language"}, {"2": "Snake"}],
            correct_answer=["1"],
        )
    ]

    result = question_storage.create_questions(payload)
    cleaned = [dto_to_json(r) for r in result]
    snapshot.assert_match(
        json.dumps(cleaned, sort_keys=True, indent=2),
        "test_create_questions_successfully"
    )


@pytest.mark.django_db
def test_get_questions(question_storage, snapshot):
    q = QuestionFactory(
        question_text="Capital of India?",
        question_type="MCQ_SINGLE",
        difficulty="EASY",
        options=["Delhi", "Mumbai"],
        correct_answer=["Delhi"],
    )

    result = question_storage.get_questions([str(q.question_id)])
    cleaned = [dto_to_json(r) for r in result]
    snapshot.assert_match(
        json.dumps(cleaned, sort_keys=True, indent=2),
        "test_get_questions"
    )


@pytest.mark.django_db
def test_update_questions(question_storage, snapshot):
    q = QuestionFactory(
        question_text="Old text",
        question_type="MCQ_SINGLE",
        difficulty="EASY",
        options=["A", "B"],
        correct_answer=["A"],
    )

    update_payload = [
        UpdateQuestionDTO(
            question_id=str(q.question_id),
            question_text="Updated text",
            question_type=QuestionTypeDTO.MCQ_SINGLE,
            difficulty=Difficulty.MEDIUM,
            options=[{"1": "X"}, {"2": "Y"}],
            correct_answer=["1"],
        )
    ]

    result = question_storage.update_questions(update_payload)
    cleaned = [dto_to_json(r) for r in result]
    snapshot.assert_match(
        json.dumps(cleaned, sort_keys=True, indent=2),
        "test_update_questions"
    )