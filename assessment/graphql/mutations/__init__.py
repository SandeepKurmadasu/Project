import graphene

from assessment.graphql.mutations.questions.create_questions import CreateQuestions
from assessment.graphql.mutations.questions.update_questions import UpdateQuestions
from assessment.graphql.mutations.questionbank.create_question_bank import CreateQuestionBank
from assessment.graphql.mutations.questionbank.add_questions_to_bank import AddingQuestionsToBank
from assessment.graphql.mutations.questionbank.remove_questions_from_bank import RemoveQuestionFromBank
from assessment.graphql.mutations.questionbank.reorder_questions import ReorderQuestionsMutation
from .evaluate_question import EvaluateQuestion
from .create_assessments import CreateAssessments


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