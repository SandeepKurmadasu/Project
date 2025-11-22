import graphene
from graphene.types.generic import GenericScalar


class QuestionTypeEnum(graphene.Enum):
    MCQ_SINGLE = "MCQ_SINGLE"
    MCQ_MULTI = "MCQ_MULTI"
    TRUE_FALSE = "TRUE_FALSE"
    FILL_BLANK = "FILL_BLANK"
    MATCH_PAIRS = "MATCH_PAIRS"


class DifficultyEnum(graphene.Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"



#input
class CreateQuestionInput(graphene.InputObjectType):
    question_text = graphene.String(required=True)
    question_type = QuestionTypeEnum(required=True)
    difficulty = DifficultyEnum(required=True)
    correct_answer = graphene.List(graphene.String,required=True)
    options =  GenericScalar(required=True)

class CreateQuestionsInput(graphene.InputObjectType):
    question_ids = graphene.List(CreateQuestionInput,required=True)


class GetQuestionsParams(graphene.InputObjectType):
    question_ids = graphene.List(graphene.String, required=True)


class UpdateQuestionParams(graphene.InputObjectType):
    question_id = graphene.String(required=True)
    question_text = graphene.String(required=True)
    question_type = QuestionTypeEnum(required=True)
    difficulty = DifficultyEnum(required=True)
    correct_answer = graphene.String(required=True)
    options =  GenericScalar(required=True)


class CreateQuestionBankParams(graphene.InputObjectType):
    name = graphene.String(required=True)
    assessment_id = graphene.String(required=True)


class GetQuestionBankParams(graphene.InputObjectType):
    bank_id = graphene.String(required=True)

class AddQuestionsToBank(graphene.InputObjectType):
    bank_id = graphene.String(required=True)
    question_ids = graphene.List(graphene.String, required=True)


class RemoveQuestionsFromBankInput(graphene.InputObjectType):
    bank_id = graphene.String(required=True)
    question_ids = graphene.List(graphene.String, required=True)


class ReorderQuestionsInput(graphene.InputObjectType):
    bank_id = graphene.String(required=True)
    question_ids = graphene.List(graphene.String, required=True)


class EvaluateQuestionInput(graphene.InputObjectType):
    question_id = graphene.String(required=True)
    user_answer = GenericScalar(required=True)


class DifficultyWeightInput(graphene.InputObjectType):
    EASY = graphene.Int()
    MEDIUM = graphene.Int()
    HARD = graphene.Int()


class GetNextQuestionsInput(graphene.InputObjectType):
    questionBankId = graphene.String(required=True)
    numberOfQuestions = graphene.Int(required=True)
    algorithm = graphene.String(required=True)   # FIXED, RANDOM, DIFFICULTY_MIX
    alreadyAttempted = graphene.List(graphene.String)
    difficultyWeights = DifficultyWeightInput()


class CreateAssessmentInput(graphene.InputObjectType):
    assessmentTitle = graphene.String(required=True)
    assessmentType = graphene.String(required=True)  # Enum string
    description = graphene.String(required=True)
    icon = graphene.String(required=True)
    noOfQuestions = graphene.Int(required=True)
    attemptsLimit = graphene.Int(required=True)
    passPercentage = graphene.Int(required=True)
    easyCount = graphene.Int()
    mediumCount = graphene.Int()
    hardCount = graphene.Int()
    estimateDurationInMins = graphene.Int(required=True)


class CreateAssessmentsInput(graphene.InputObjectType):
    assessments = graphene.List(CreateAssessmentInput, required=True)
