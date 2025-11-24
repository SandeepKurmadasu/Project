import graphene

from assessment.view_graphql.types.error_types import AssessmentNotFoundType, \
    AssessmentUserNotFoundType, AlreadyAttemptedExistType, AttemptNotFoundType
from assessment.view_graphql.types.types import AttemptsCompletedType, \
    AssessmentAttemptType, AssessmentAttemptProgressType, AttemptScoreType, \
    DisplayQuestionType, AttemptEndType, AutoEndAttemptType


class StartAttemptResponse(graphene.Union):
    class Meta:
        types = (
            AttemptsCompletedType,
            AssessmentAttemptType,
            AssessmentNotFoundType,
            AssessmentUserNotFoundType
        )

        @classmethod
        def resolve_type(cls, instance, info):
            if isinstance(instance, AttemptsCompletedType):
                return AttemptsCompletedType
            if isinstance(instance, AssessmentAttemptType):
                return AssessmentAttemptType
            return None

class GetLatestAttemptResponse(graphene.Union):
    class Meta:
        types = (
            AssessmentAttemptType,
            AssessmentNotFoundType,
            AssessmentUserNotFoundType,
        )


class SubmitAnswerResponse(graphene.Union):
    class Meta:
        types = (
            AssessmentAttemptType,
            AlreadyAttemptedExistType
        )


class GetAssessmentAttemptProgressResponse(graphene.Union):
    class Meta:
        types = (
            AssessmentAttemptProgressType,
            AttemptNotFoundType,
        )

class GetAttemptScoreResponse(graphene.Union):
    class Meta:
        types = (
            AttemptScoreType,
            AttemptNotFoundType,
        )

class GetNextQuestionResponse(graphene.Union):
    class Meta:
        types = (
            DisplayQuestionType,
            AssessmentAttemptProgressType,
            AttemptNotFoundType,
        )

class AttemptEndResponse(graphene.Union):
    class Meta:
        types = (
            AttemptEndType,
            AttemptNotFoundType
        )

class AutoEndAttemptResponse(graphene.Union):
    class Meta:
        types = (
            AutoEndAttemptType,
            AttemptNotFoundType
        )


import graphene

from .types import QuestionsType, QuestionBankType, QuestionBankQuestionType, EvaluateQuestionType, \
    GetNextQuestionsResponse, AssessmentType, AssessmentListType
from .error_types import (
    UnExpectedQuestionType,
    UnExpectedDifficulty, CheckQuestionExist, QuestionNotFounded, DuplicateBankName, AssessmentIdNotFounded,
    BankNotFound, DuplicateQuestionIds, QuestionsAlreadyBank, QuestionNotInBankError, QuestionNotFoundError,
    EvaluationError, BankNotFoundError, InvalidAlgorithmError, InvalidNumberOfQuestionsError, DifficultyWeightError,
    InvalidAssessmentTypesError, InvalidPassPercentageError,
)


class CreateQuestionsResponse(graphene.Union):
    class Meta:
        types = (QuestionsType, UnExpectedQuestionType, UnExpectedDifficulty)

    @classmethod
    def resolve_type(cls, instance, info):
        if isinstance(instance, QuestionsType):
            return QuestionsType
        if isinstance(instance, UnExpectedQuestionType):
            return UnExpectedQuestionType
        if isinstance(instance, UnExpectedDifficulty):
            return UnExpectedDifficulty
        return type(instance)


class GetQuestionsResponse(graphene.Union):
    class Meta:
        types = (QuestionsType, CheckQuestionExist)

    @classmethod
    def resolve_type(cls, instance, info):
        if isinstance(instance, QuestionsType):
            return QuestionsType
        if isinstance(instance, CheckQuestionExist):
            return CheckQuestionExist
        return type(instance)


class UpdateQuestionsResponse(graphene.Union):
    class Meta:
        types = (QuestionsType, QuestionNotFounded, UnExpectedQuestionType, UnExpectedDifficulty)

    @classmethod
    def resolve_type(cls, instance, info):
        if isinstance(instance, QuestionsType):
            return QuestionsType
        if isinstance(instance, QuestionNotFounded):
            return QuestionNotFounded
        if isinstance(instance, UnExpectedQuestionType):
            return UnExpectedQuestionType
        if isinstance(instance, UnExpectedDifficulty):
            return UnExpectedDifficulty
        return type(instance)


class CreateQuestionBankResponse(graphene.Union):
    class Meta:
        types = (QuestionBankType, DuplicateBankName, AssessmentIdNotFounded)

    @classmethod
    def resolve_type(cls, instance, info):
        if isinstance(instance, QuestionBankType):
            return QuestionBankType
        if isinstance(instance, DuplicateBankName):
            return DuplicateBankName
        if isinstance(instance, AssessmentIdNotFounded):
            return AssessmentIdNotFounded
        return type(instance)


class GetQuestionBankResponse(graphene.Union):
    class Meta:
        types = (QuestionBankType, BankNotFound)

    @classmethod
    def resolve_type(cls, instance, info):
        if isinstance(instance, QuestionsType):
            return QuestionsType
        if isinstance(instance, BankNotFound):
            return BankNotFound
        return type(instance)


class AddQuestionsToBankResponse(graphene.Union):
    class Meta:
        types = (QuestionBankQuestionType, DuplicateQuestionIds, BankNotFound, CheckQuestionExist, QuestionsAlreadyBank)

    @classmethod
    def resolve_type(cls, instance, info):
        if isinstance(instance, QuestionBankType):
            return QuestionBankType
        if isinstance(instance, DuplicateQuestionIds):
            return DuplicateQuestionIds
        if isinstance(instance, BankNotFound):
            return BankNotFound
        if isinstance(instance, CheckQuestionExist):
            return CheckQuestionExist
        if isinstance(instance, QuestionsAlreadyBank):
            return QuestionsAlreadyBank
        return type(instance)


class RemoveQuestionsFromBankResponse(graphene.Union):
    class Meta:
        types = (
            QuestionBankQuestionType,
            BankNotFound,
            CheckQuestionExist,
            QuestionNotInBankError,
        )

    @classmethod
    def resolve_type(cls, instance, info):
        if isinstance(instance, QuestionBankQuestionType):
            return QuestionBankQuestionType
        if isinstance(instance, BankNotFound):
            return BankNotFound
        if isinstance(instance, CheckQuestionExist):
            return CheckQuestionExist
        if isinstance(instance, QuestionNotInBankError):
            return QuestionNotInBankError
        return type(instance)


class ReorderQuestionsResponse(graphene.Union):
    class Meta:
        types = (
            QuestionBankQuestionType,
            BankNotFound,
            QuestionNotInBankError,
        )

    @classmethod
    def resolve_type(cls, instance, info):
        if isinstance(instance, QuestionBankQuestionType):
            return QuestionBankQuestionType
        if isinstance(instance, BankNotFound):
            return BankNotFound
        if isinstance(instance, QuestionNotInBankError):
            return QuestionNotInBankError
        return type(instance)


class EvaluateQuestionResponse(graphene.Union):
    class Meta:
        types = (
            EvaluateQuestionType,
            QuestionNotFoundError,
            EvaluationError,
        )

    @classmethod
    def resolve_type(cls, instance, info):
        if isinstance(isinstance, EvaluateQuestionType):
            return EvaluateQuestionType
        if isinstance(isinstance, QuestionNotFoundError):
            return QuestionNotFoundError
        if isinstance(isinstance, EvaluationError):
            return EvaluationError
        return type(instance)




class GetNextQuestionsUnion(graphene.Union):
    class Meta:
        types = (
            GetNextQuestionsResponse,
            BankNotFoundError,
            InvalidAlgorithmError,
            InvalidNumberOfQuestionsError,
            DifficultyWeightError,
        )

class CreateAssessmentsResponse(graphene.Union):
    class Meta:
        types = (
            AssessmentListType,
            InvalidAssessmentTypesError,
            InvalidPassPercentageError,
        )

    @classmethod
    def resolve_type(cls, instance, info):
        if isinstance(instance, AssessmentListType) :
            return AssessmentListType
        if isinstance(instance, InvalidAssessmentTypesError):
            return InvalidAssessmentTypesError
        if isinstance(instance, InvalidPassPercentageError):
            return InvalidPassPercentageError
        return type(instance)
