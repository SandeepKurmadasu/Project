import graphene
from graphene import String, DateTime
from graphene.types.generic import GenericScalar


class AssessmentAttemptType(graphene.ObjectType):
    attempt_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    assessment_id = graphene.String(required=True)
    total_points = graphene.Int(required=True)
    question_ids = graphene.List(graphene.String, required=True)
    status = graphene.String(required=True)
    started_at = DateTime(required=True)

class SubmitAnswerType(graphene.ObjectType):
    attempt_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    assessment_id = graphene.String(required=True)
    total_points = graphene.Int(required=True)
    is_correct = graphene.String(required=True)
    points = graphene.Float(required=True)

class AttemptsCompletedType(graphene.ObjectType):
    user_id = graphene.String(required=True)
    assessment_id = graphene.String(required=True)
    attempts_limit = graphene.Int(required=True)
    user_attempted_count = graphene.Int(required=True)


class AssessmentAttemptProgressType(graphene.ObjectType):
    attempt_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    assessment_id = graphene.String(required=True)
    total_points = graphene.Int(required=True)
    status = graphene.String(required=True)

class AttemptScoreType(graphene.ObjectType):
    attempt_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    score = graphene.Int(required=True)


class DisplayQuestionType(graphene.ObjectType):
    question_id = graphene.String(required=True)
    question_text = graphene.String(required=True)
    question_type = graphene.String(required=True)
    options = GenericScalar()

class AttemptEndType(graphene.ObjectType):
    attempt_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    assessment_id = graphene.String(required=True)
    total_points = graphene.Int(required=True)
    question_ids = graphene.List(graphene.String, required=True)
    status = graphene.String(required=True)
    started_at = DateTime(required=True)
    completed_at = DateTime(required=True)

class AutoEndAttemptType(graphene.ObjectType):
    attempt_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    assessment_id = graphene.String(required=True)
    total_points = graphene.Int(required=True)
    question_ids = graphene.List(graphene.String, required=True)
    status = graphene.String(required=True)
    started_at = DateTime(required=True)
    completed_at = DateTime(required=True)


import graphene
from graphene.types.generic import GenericScalar


class AnswerStatusEnum(graphene.Enum):
    CORRECT = "CORRECT"
    PARTIALLY_CORRECT = "PARTIALLY_CORRECT"
    INCORRECT = "INCORRECT"


class QuestionTyped(graphene.ObjectType):
    question_id = graphene.String(required=True)
    question_text = graphene.String(required=True)
    question_type = graphene.String(required=True)
    difficulty_level = graphene.String(required=True)
    correct_answer = GenericScalar(required=True)
    options = GenericScalar(required=True)

class QuestionsType(graphene.ObjectType):
    question_ids = graphene.List(QuestionTyped, required=True)

class QuestionBankType(graphene.ObjectType):
    bank_id = graphene.String(required=True)
    name = graphene.String(required=True)
    assessment_id = graphene.String(required=True)
    created_at = graphene.String(required=True)
    updated_at = graphene.String(required=True)


class QuestionBankQuestionType(graphene.ObjectType):
    bank_id = graphene.String(required=True)
    question_ids = graphene.List(graphene.String, required=True)


class EvaluateQuestionType(graphene.ObjectType):
    status = AnswerStatusEnum(required=True)
    correct_count = graphene.Int()
    total_count = graphene.Int()

class QuestionItemType(graphene.ObjectType):
    question_id = graphene.String()
    questionText = graphene.String()
    questionType = graphene.String()
    difficultyLevel = graphene.String()


class GetNextQuestionsResponse(graphene.ObjectType):
    bank_id = graphene.String()
    questions = graphene.List(QuestionItemType)


class AssessmentType(graphene.ObjectType):
    assessmentId = graphene.String(required=True)
    assessmentTitle = graphene.String(required=True)
    assessmentType = graphene.String(required=True)
    topic_id = graphene.String(required=True)
    description = graphene.String(required=True)
    passMarks = graphene.Int(required=True)
    icon = graphene.String(required=True)
    noOfQuestions = graphene.Int(required=True)
    marks = graphene.Int(required=True)
    passPercentage = graphene.Int(required=True)
    easyCount = graphene.Int()
    mediumCount = graphene.Int()
    hardCount = graphene.Int()
    attemptsLimit = graphene.Int(required=True)
    estimateDurationInMins = graphene.Int(required=True)


class AssessmentListType(graphene.ObjectType):
    assessments = graphene.List(AssessmentType)
