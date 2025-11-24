import graphene

from assessment.view_graphql.mutations import CreateAttempt, SubmitAnswer, \
    AttemptEnd, AutoEndAttempt, UpdateQuestion, CreateQuestionBankMutation, \
    RemoveQuestionsFromBank, AddQuestionsToBank, CreateAssessmentsMutation, \
    CreateQuestion, ReorderQuestions, EvaluateQuestionMutation
from assessment.view_graphql.queries import GetLatestAttempt, \
    GetAssessmentAttemptProgress, GetAttemptScore, GetNextQuestion, \
    GetNextNQuestions, GetQuestions, GetQuestionBank

QUERY_CLASSES = [GetLatestAttempt, GetAssessmentAttemptProgress,
                 GetAttemptScore, GetNextQuestion,GetNextNQuestions, GetQuestions, GetQuestionBank]

MUTATION_CLASSES = {CreateAttempt, SubmitAnswer, AttemptEnd, AutoEndAttempt,
                    UpdateQuestion, CreateQuestionBankMutation,
                    AddQuestionsToBank, RemoveQuestionsFromBank,
                    ReorderQuestions,EvaluateQuestionMutation,
                    CreateAssessmentsMutation, CreateQuestion}


class Query(*QUERY_CLASSES):
    """
    Class to define the Query Object
    """


class Mutation(*MUTATION_CLASSES):
    """
    Class to define the Mutation Object
    """


schema = graphene.Schema(query=Query, mutation=Mutation)
