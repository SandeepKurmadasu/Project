import graphene
from assessment.graphql.types.input_types import GetQuestionsParams
from assessment.graphql.types.types import QuestionTyped, QuestionsType
from assessment.graphql.types.error_types import CheckQuestionExist
from assessment.graphql.types.response_types import GetQuestionsResponse
from assessment.interactors.questions.get_questions_interactor import GetQuestionsInteractor
from assessment.storages.question_storage import QuestionStorage
from assessment.exceptions.custom_exceptions import QuestionNotFound


def resolve_get_questions(root, info, params):
    try:
        dtos= GetQuestionsInteractor(question_storage=QuestionStorage()).get_questions(params.question_ids)
        questions=[
            QuestionTyped(
                question_id=d.question_id,
                question_text=d.question_text,
                question_type=d.question_type,
                difficulty_level=d.difficulty_level,
                correct_answer=d.correct_answer,
                options=d.options
            )
            for d in dtos
        ]
        return QuestionsType(question_ids=questions)

    except QuestionNotFound as e:
        return CheckQuestionExist(questions=e.questions)


