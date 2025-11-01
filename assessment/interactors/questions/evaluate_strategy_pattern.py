from abc import ABC, abstractmethod

from assessment.interactors.dtos import EvaluateQuestionDTO, QuestionType


class QuestionEvaluationStrategy(ABC):
    @abstractmethod
    def evaluate(self,user_answer,correct_answer)-> EvaluateQuestionDTO:
        pass

class MCQSingleQuestionStrategy(QuestionEvaluationStrategy):
    def evaluate(self,user_answer,correct_answer) -> EvaluateQuestionDTO:
        is_correct = str(user_answer).strip() == str(correct_answer).strip()
        return EvaluateQuestionDTO(is_correct=is_correct)

class MULTIChoiceMCQQuestionStrategy(QuestionEvaluationStrategy):
    def evaluate(self,user_answer,correct_answer) -> EvaluateQuestionDTO:
        user_set = set(map(str.strip, str(user_answer).split(","))) if user_answer else set()
        correct_set = set(map(str.strip, str(correct_answer).split(","))) if correct_answer else set()
        is_correct = user_set == correct_set
        return EvaluateQuestionDTO(is_correct=is_correct)

class FillInTheBlankQuestionStrategy(QuestionEvaluationStrategy):
    def evaluate(self,user_answer,correct_answer) -> EvaluateQuestionDTO:
        is_correct = str(user_answer).strip().lower() == str(correct_answer).strip().lower()
        return EvaluateQuestionDTO(is_correct=is_correct)


class TrueOrFalseQuestionStrategy(QuestionEvaluationStrategy):
    def evaluate(self,user_answer,correct_answer) -> EvaluateQuestionDTO:
        is_correct = str(user_answer).strip().lower() == str(correct_answer).strip().lower()
        return EvaluateQuestionDTO(is_correct=is_correct)

class MatchThePairsQuestionStrategy(QuestionEvaluationStrategy):
    def evaluate(self,user_answer,correct_answer) -> EvaluateQuestionDTO:
        def parse_pairs(pairs_str):
            pairs = {}
            for pair in pairs_str.split(","):
                if ":" in pair:
                    left, right = pair.split(":", 1)
                    pairs[left.strip()] = right.strip()
            return pairs

        if isinstance(user_answer, dict):
            user_pairs = user_answer
        else:
            user_pairs = parse_pairs(str(user_answer))

        correct_pairs = parse_pairs(str(correct_answer)) if correct_answer else {}
        is_correct = user_pairs == correct_pairs
        return EvaluateQuestionDTO(is_correct=is_correct)


class QuestionStrategy:
    @staticmethod
    def get_strategy(question_type: QuestionType) -> QuestionEvaluationStrategy:
        all_classes={
            QuestionType.MCQ_SINGLE: MCQSingleQuestionStrategy(),
            QuestionType.MCQ_MULTI: MULTIChoiceMCQQuestionStrategy(),
            QuestionType.FILL_BLANK: FillInTheBlankQuestionStrategy(),
            QuestionType.TRUE_FALSE: TrueOrFalseQuestionStrategy(),
            QuestionType.MATCH_PAIRS: MatchThePairsQuestionStrategy()
        }
        return all_classes.get(question_type)
