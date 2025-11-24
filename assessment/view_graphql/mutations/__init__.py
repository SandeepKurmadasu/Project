import graphene

from assessment.view_graphql.mutations.attempts.auto_end_attempt_mutation import \
    AutoEndAttemptMutation
from assessment.view_graphql.mutations.attempts.end_an_attempt_mutation import \
    AttemptEndMutation
from assessment.view_graphql.mutations.attempts.start_attempt_mutation import \
    StartAssessmentAttempt
from assessment.view_graphql.mutations.attempts.submit_response_mutation import \
    SubmitResponseMutation


class CreateAttempt(graphene.ObjectType):
    create_attempt = StartAssessmentAttempt.Field(required=True)


class SubmitAnswer(graphene.ObjectType):
    submit_answer = SubmitResponseMutation.Field(required=True)

class AttemptEnd(graphene.ObjectType):
    attempt_end = AttemptEndMutation.Field(required=True)

class AutoEndAttempt(graphene.ObjectType):
    auto_end_attempt = AutoEndAttemptMutation.Field(required=True)
    
    

import graphene

from assessment.view_graphql.mutations.questions.create_questions import CreateQuestions
from assessment.view_graphql.mutations.questions.update_questions import UpdateQuestions
from assessment.view_graphql.mutations.questionbank.create_question_bank import CreateQuestionBank
from assessment.view_graphql.mutations.questionbank.add_questions_to_bank import AddingQuestionsToBank
from assessment.view_graphql.mutations.questionbank.remove_questions_from_bank import RemoveQuestionFromBank
from assessment.view_graphql.mutations.questionbank.reorder_questions import ReorderQuestionsMutation
from assessment.view_graphql.mutations.questions.evaluate_question import EvaluateQuestion
from assessment.view_graphql.mutations.Assessments.create_assessments import CreateAssessments


class CreateQuestion(graphene.ObjectType):
    create_questions = CreateQuestions.Field(required=True)


class UpdateQuestion(graphene.ObjectType):
    update_questions = UpdateQuestions.Field(required=True)


class CreateQuestionBankMutation(graphene.ObjectType):
    create_question_bank = CreateQuestionBank.Field(required=True)


class AddQuestionsToBank(graphene.ObjectType):
    add_questions_to_bank = AddingQuestionsToBank.Field(required=True)


class RemoveQuestionsFromBank(graphene.ObjectType):
    remove_questions_from_bank = RemoveQuestionFromBank.Field(required=True)


class ReorderQuestions(graphene.ObjectType):
    reorder_questions = ReorderQuestionsMutation.Field(required=True)


class EvaluateQuestionMutation(graphene.ObjectType):
    evaluate_question = EvaluateQuestion.Field(required=True)


class CreateAssessmentsMutation(graphene.ObjectType):
    create_assessments = CreateAssessments.Field(required=True)