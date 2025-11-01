from abc import ABC,abstractmethod
from assessment.interactors.dtos import CreateQuestionDTO, QuestionType
from assessment.models import Question


class BaseQuestionFactory(ABC):
    @abstractmethod
    def create(self,question: CreateQuestionDTO):
        pass


class MCQSingleQuestionFactory(BaseQuestionFactory):
    def create(self,question: CreateQuestionDTO):
        return Question(
            question_text= question.question_text,
            type= question.question_type.value,
            difficulty= question.difficulty.value,
            options= question.options,
            correct_option_ids= question.correct_option_ids
        )


class MCQMultiChoiceQuestionFactory(BaseQuestionFactory):
    def create(self,question: CreateQuestionDTO):
        return Question(
            question_text= question.question_text,
            type= question.question_type.value,
            difficulty= question.difficulty.value,
            options= question.options,
            correct_option_ids= question.correct_option_ids
        )

class FillInTheBlankQuestionFactory(BaseQuestionFactory):
    def create(self,question: CreateQuestionDTO):
        return Question(
            question_text= question.question_text,
            type= question.question_type.value,
            difficulty= question.difficulty.value,
            correct_fill_text= question.correct_fill_text
        )

class TrueOrFalseQuestionFactory(BaseQuestionFactory):
    def create(self, question: CreateQuestionDTO):

        return Question(
            question_text= question.question_text,
            type= question.question_type.value,
            difficulty= question.difficulty.value,
            correct_boolean= question.correct_boolean
        )

class MatchThePairsQuestionFactory(BaseQuestionFactory):
    def create(self,question: CreateQuestionDTO):
        return Question(
            question_text= question.question_text,
            type= question.question_type.value,
            difficulty= question.difficulty.value,
            correct_pairs= question.correct_pairs
        )

class QuestionFactory:
    @staticmethod
    def get_factory(question_type:QuestionType) -> BaseQuestionFactory:
        all_classes={
            QuestionType.MCQ_SINGLE: MCQSingleQuestionFactory(),
            QuestionType.MCQ_MULTI: MCQMultiChoiceQuestionFactory(),
            QuestionType.TRUE_FALSE: TrueOrFalseQuestionFactory(),
            QuestionType.FILL_BLANK: FillInTheBlankQuestionFactory(),
            QuestionType.MATCH_PAIRS: MatchThePairsQuestionFactory()
        }
        return all_classes.get(question_type)

    @staticmethod
    def bulk_create_questions(questions: list[CreateQuestionDTO]):
        question_objects = []
        for q in questions:
            factory = QuestionFactory.get_factory(q.question_type)
            question_obj = factory.create(q)
            question_objects.append(question_obj)
        return question_objects