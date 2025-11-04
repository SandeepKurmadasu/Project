from assessment.interactors.questions.evaluate_strategy_pattern import (
    MCQSingleQuestionStrategy,
    MultiChoiceMCQQuestionStrategy,
    FillInTheBlankQuestionStrategy,
    TrueOrFalseQuestionStrategy,
    MatchThePairsQuestionStrategy
)


def test_mcq_single_strategy_correct():
    strategy = MCQSingleQuestionStrategy()
    result = strategy.evaluate("4", "4")
    assert result.is_correct is True


def test_mcq_single_strategy_incorrect():
    strategy = MCQSingleQuestionStrategy()
    result = strategy.evaluate("3", "4")
    assert result.is_correct is False


def test_mcq_multi_strategy_correct():
    strategy = MultiChoiceMCQQuestionStrategy()
    result = strategy.evaluate("2,4", "2,4")
    assert result.is_correct is True


def test_mcq_multi_strategy_incorrect():
    strategy = MultiChoiceMCQQuestionStrategy()
    result = strategy.evaluate("2,3", "2,4")
    assert result.is_correct is False


def test_fill_blank_strategy_correct():
    strategy = FillInTheBlankQuestionStrategy()
    result = strategy.evaluate("new delhi", "New Delhi")
    assert result.is_correct is True


def test_true_false_strategy_correct():
    strategy = TrueOrFalseQuestionStrategy()
    result = strategy.evaluate("true", "True")
    assert result.is_correct is True


def test_match_pairs_strategy_correct_dict():
    strategy = MatchThePairsQuestionStrategy()
    user = {"India": "Delhi", "USA": "Washington"}
    correct = "India:Delhi,USA:Washington"
    result = strategy.evaluate(user, correct)
    assert result.is_correct is True


def test_match_pairs_strategy_incorrect():
    strategy = MatchThePairsQuestionStrategy()
    user = {"India": "Mumbai"}
    correct = "India:Delhi"
    result = strategy.evaluate(user, correct)
    assert result.is_correct is False
