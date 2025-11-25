from assessment.exceptions.custom_exceptions import QuestionNotFound
from assessment.view_graphql.types.types import QuestionTyped, QuestionsType
from assessment.view_graphql.types.error_types import CheckQuestionExist
from assessment.interactors.questions.get_questions_interactor import GetQuestionsInteractor
from assessment.storages.question_storage import QuestionStorage


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


