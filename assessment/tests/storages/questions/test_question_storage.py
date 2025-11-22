import json
import pytest

from assessment.storages.question_storage import QuestionStorage
from assessment.interactors.dtos import (
    CreateQuestionDTO,
    UpdateQuestionDTO,
    QuestionTypeDTO,
    Difficulty,
)
from assessment.models import Question


def dto_to_json(dto):
    d = dto.__dict__.copy()

    # Convert enums to string values
    if hasattr(d["question_type"], "value"):
        d["question_type"] = d["question_type"].value

    if hasattr(d["difficulty_level"], "value"):
        d["difficulty_level"] = d["difficulty_level"].value

    # Normalize UUID for deterministic snapshots
    d["question_id"] = "STATIC-ID"

    return d


@pytest.mark.django_db
def test_create_questions(snapshot):
    payload = [
        CreateQuestionDTO(
            question_text="What is Python?",
            question_type=QuestionTypeDTO.MCQ_SINGLE,
            difficulty=Difficulty.EASY,
            options=[{"1": "Programming language"}, {"2": "Snake"}],
            correct_answer=["1"],
        )
    ]

    storage = QuestionStorage()
    result = storage.create_questions(payload)

    cleaned = [dto_to_json(r) for r in result]

    snapshot.assert_match(
        json.dumps(cleaned, sort_keys=True, indent=2),
        "test_create_questions_successfully"
    )


@pytest.mark.django_db
def test_get_questions(snapshot):
    q = Question.objects.create(
        question_text="Capital of India?",
        question_type=QuestionTypeDTO.MCQ_SINGLE.value,
        difficulty=Difficulty.EASY.value,
        options=["Delhi", "Mumbai"],
        correct_answer=["Delhi"],
    )

    storage = QuestionStorage()
    result = storage.get_questions([str(q.question_id)])

    cleaned = [dto_to_json(r) for r in result]

    snapshot.assert_match(
        json.dumps(cleaned, sort_keys=True, indent=2),
        "test_get_questions"
    )


@pytest.mark.django_db
def test_update_questions(snapshot):
    q = Question.objects.create(
        question_text="Old text",
        question_type=QuestionTypeDTO.MCQ_SINGLE.value,
        difficulty=Difficulty.EASY.value,
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

    storage = QuestionStorage()
    result = storage.update_questions(update_payload)

    cleaned = [dto_to_json(r) for r in result]

    snapshot.assert_match(
        json.dumps(cleaned, sort_keys=True, indent=2),
        "test_update_questions"
    )
