import json

from assessment.interactors.questions.create_question_factory import (
    MCQSingleQuestionFactory,
    MCQMultiChoiceQuestionFactory,
    FillInTheBlankQuestionFactory,
    TrueOrFalseQuestionFactory,
    MatchThePairsQuestionFactory,
)
from assessment.interactors.dtos import CreateQuestionDTO, QuestionType, Difficulty


def model_to_dict(obj):
    return {
        "question_text": obj.question_text,
        "question_type": obj.question_type,
        "difficulty": obj.difficulty,
        "options": obj.options if hasattr(obj, "options") else None,
        "correct_answer": obj.correct_answer,
    }


def test_mcq_single_factory(snapshot):
    factory = MCQSingleQuestionFactory()
    dto = CreateQuestionDTO(
        question_text="2 + 2 = ?",
        question_type=QuestionType.MCQ_SINGLE,
        difficulty=Difficulty.EASY,
        options=[{"id": "1", "text": "4"}],
        correct_answer=["1"],
    )
    question = factory.create(dto)
    snapshot.assert_match(
        json.dumps(model_to_dict(question), indent=2, sort_keys=True),
        "mcq_single_question",
    )


def test_mcq_multi_factory(snapshot):
    factory = MCQMultiChoiceQuestionFactory()
    dto = CreateQuestionDTO(
        question_text="Pick languages",
        question_type=QuestionType.MCQ_MULTI,
        difficulty=Difficulty.MEDIUM,
        options=[{"id": "1", "text": "Python"}, {"id": "2", "text": "Java"}],
        correct_answer=["1", "2"],
    )
    question = factory.create(dto)
    snapshot.assert_match(
        json.dumps(model_to_dict(question), indent=2, sort_keys=True),
        "mcq_multi_question",
    )


def test_fill_blank_factory(snapshot):
    factory = FillInTheBlankQuestionFactory()
    dto = CreateQuestionDTO(
        question_text="Capital of India is ___",
        question_type=QuestionType.FILL_BLANK,
        difficulty=Difficulty.EASY,
        correct_answer="Delhi",
    )
    question = factory.create(dto)
    snapshot.assert_match(
        json.dumps(model_to_dict(question), indent=2, sort_keys=True),
        "fill_blank_question",
    )


def test_true_false_factory(snapshot):
    factory = TrueOrFalseQuestionFactory()
    dto = CreateQuestionDTO(
        question_text="Python is fun",
        question_type=QuestionType.TRUE_FALSE,
        difficulty=Difficulty.EASY,
        correct_answer=True,
    )
    question = factory.create(dto)
    snapshot.assert_match(
        json.dumps(model_to_dict(question), indent=2, sort_keys=True),
        "true_false_question",
    )


def test_match_pairs_factory(snapshot):
    factory = MatchThePairsQuestionFactory()
    dto = CreateQuestionDTO(
        question_text="Match capitals",
        question_type=QuestionType.MATCH_PAIRS,
        difficulty=Difficulty.HARD,
        options=[{"left_items": ["France", "Japan"]}, {"right_items": ["Paris", "Tokyo"]}],
        correct_answer=[[0, 0], [1, 1]],
    )
    question = factory.create(dto)
    snapshot.assert_match(
        json.dumps(model_to_dict(question), indent=2, sort_keys=True),
        "match_pairs_question",
    )