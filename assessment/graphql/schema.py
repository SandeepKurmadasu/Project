import graphene

from assessment.graphql.mutations import CreateQuestion, UpdateQuestion, CreateAssessmentsMutation, \
    RemoveQuestionsFromBank, AddQuestionsToBank, CreateQuestionBankMutation
from assessment.graphql.queries import GetNextNQuestions, GetQuestions, GetQuestionBank

QUERY_CLASSES = [GetNextNQuestions, GetQuestions, GetQuestionBank]


class ReorderQuestionsEvaluateQuestionMutation:
    pass


MUTATION_CLASSES = {UpdateQuestion,CreateQuestionBankMutation,AddQuestionsToBank,RemoveQuestionsFromBank,ReorderQuestionsEvaluateQuestionMutation,CreateAssessmentsMutation,CreateQuestion}

class Query(*QUERY_CLASSES):
    pass


class Mutation(*MUTATION_CLASSES):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
