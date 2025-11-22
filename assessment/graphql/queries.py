import graphene

from assessment.graphql.resolvers.get_next_n_questions import resolve_get_next_questions
from assessment.graphql.resolvers.get_question_bank import resolve_get_question_bank
from assessment.graphql.resolvers.get_questions import resolve_get_questions
from assessment.graphql.types.input_types import GetNextQuestionsInput, GetQuestionBankParams, GetQuestionsParams
from assessment.graphql.types.response_types import GetNextQuestionsUnion, GetQuestionBankResponse, GetQuestionsResponse


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