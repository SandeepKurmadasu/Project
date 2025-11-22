import graphene


class UnExpectedQuestionType(graphene.ObjectType):
    types = graphene.List(graphene.String, required=True)


class UnExpectedDifficulty(graphene.ObjectType):
    difficulty = graphene.List(graphene.String, required=True)


class CheckQuestionExist(graphene.ObjectType):
    questions = graphene.List(graphene.String, required=True)


class DuplicateQuestionIds(graphene.ObjectType):
    questions = graphene.List(graphene.String, required=True)


class QuestionNotFounded(graphene.ObjectType):
    questions = graphene.List(graphene.String, required=True)


class DuplicateBankName(graphene.ObjectType):
    name = graphene.String(required=True)


class AssessmentIdNotFounded(graphene.ObjectType):
    assessment_id = graphene.String(required=True)


class BankNotFound(graphene.ObjectType):
    bank_id =graphene.String(required=True)


class QuestionsAlreadyBank(graphene.ObjectType):
    question_ids = graphene.List(graphene.String, required=True)


class QuestionNotInBankError(graphene.ObjectType):
    bank_id = graphene.String(required=True)
    question_ids = graphene.List(graphene.String, required=True)


class QuestionNotFoundError(graphene.ObjectType):
    question_id = graphene.String(required=True)


class EvaluationError(graphene.ObjectType):
    message = graphene.String(required=True)


class BankNotFoundError(graphene.ObjectType):
    bank_id = graphene.String()

class InvalidAlgorithmError(graphene.ObjectType):
    message = graphene.String(required=True)

class InvalidNumberOfQuestionsError(graphene.ObjectType):
    message = graphene.String(required=True)

class DifficultyWeightError(graphene.ObjectType):
    message = graphene.String(required=True)


class InvalidAssessmentTypesError(graphene.ObjectType):
    assessmentTypes = graphene.List(graphene.String)


class InvalidPassPercentageError(graphene.ObjectType):
    percentages = graphene.List(graphene.Int)

