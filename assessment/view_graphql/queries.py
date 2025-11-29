import graphene

from assessment.view_graphql.resolvers.assessment_resolvers.get_assessment_by_topic_resolver import \
    get_assessment_by_topic_resolver
from assessment.view_graphql.resolvers.attempts.get_attempt_progress_resolver import \
    get_attempt_progress_resolver
from assessment.view_graphql.resolvers.attempts.get_attempt_score_resolver import \
    get_attempt_score_resolver
from assessment.view_graphql.resolvers.attempts.get_latest_attempt_resolver import \
    get_latest_attempt_resolver
from assessment.view_graphql.resolvers.attempts.get_next_question_resolver import \
    get_next_question_resolver
from assessment.view_graphql.types.input_types import \
    GetLatestAttemptReqParams, GetAttemptProgressReqParams, \
    GetAttemptScoreReqParams, GetNextQuestionReqParams, \
    GetAssessmentByTopicReqParams
from assessment.view_graphql.types.response_types import \
    GetLatestAttemptResponse, GetAssessmentAttemptProgressResponse, \
    GetAttemptScoreResponse, GetNextQuestionResponse, \
    GetAssessmentByTopicResponse


class GetLatestAttempt(graphene.ObjectType):
    get_latest_attempt = graphene.Field(
        GetLatestAttemptResponse,
        required=True,
        params=GetLatestAttemptReqParams(required=True),
        resolver=get_latest_attempt_resolver
    )

class GetAssessmentAttemptProgress(graphene.ObjectType):
    get_assessment_attempt_progress = graphene.Field(
        GetAssessmentAttemptProgressResponse,
        required=True,
        params=GetAttemptProgressReqParams(required=True),
        resolver=get_attempt_progress_resolver
    )

class GetAttemptScore(graphene.ObjectType):
    get_attempt_score = graphene.Field(
        GetAttemptScoreResponse,
        required=True,
        params=GetAttemptScoreReqParams(required=True),
        resolver=get_attempt_score_resolver
    )

class GetNextQuestion(graphene.ObjectType):
    get_next_question = graphene.Field(
        GetNextQuestionResponse,
        required=True,
        params=GetNextQuestionReqParams(required=True),
        resolver=get_next_question_resolver
    )


import graphene

from assessment.view_graphql.resolvers.question_resolver.get_next_n_questions import resolve_get_next_questions
from assessment.view_graphql.resolvers.question_resolver.get_question_bank import resolve_get_question_bank
from assessment.view_graphql.resolvers.question_resolver.get_questions import resolve_get_questions
from assessment.view_graphql.types.input_types import GetNextQuestionsInput, GetQuestionBankParams, GetQuestionsParams
from assessment.view_graphql.types.response_types import GetNextQuestionsUnion, GetQuestionBankResponse, GetQuestionsResponse


class GetNextNQuestions(graphene.ObjectType):

    get_next_questions = graphene.Field(
        GetNextQuestionsUnion,
        params=GetNextQuestionsInput(required=True),
        resolver=resolve_get_next_questions
    )

class GetQuestionBank(graphene.ObjectType):
    get_question_bank = graphene.Field(
        GetQuestionBankResponse,
        params=GetQuestionBankParams(required=True),
        required=True,
        resolver=resolve_get_question_bank
    )


class GetQuestions(graphene.ObjectType):
    get_questions = graphene.Field(
        GetQuestionsResponse,
        params = GetQuestionsParams(required=True),
        required=True,
        resolver=resolve_get_questions
    )


class GetAssessmentByTopic(graphene.ObjectType):
    get_assessment_by_topic = graphene.Field(
        GetAssessmentByTopicResponse,
        required=True,
        params=GetAssessmentByTopicReqParams(required=True),
        resolver=get_assessment_by_topic_resolver
    )