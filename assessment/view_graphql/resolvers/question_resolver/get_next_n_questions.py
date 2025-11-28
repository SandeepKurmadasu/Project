import graphene

from assessment.exceptions.custom_exceptions import QuestionBankNotFound, InvalidAlgorithmError
from assessment.view_graphql.types.error_types import InvalidNumberOfQuestionsError, DifficultyWeightError, BankNotFoundError
from assessment.view_graphql.types.response_types import  GetNextQuestionsResponse
from assessment.view_graphql.types.types import QuestionItemType
from assessment.interactors.dtos import Algorithm, Difficulty, SelectionConfigDTO
from assessment.interactors.question_selection.get_next_n_questions_interactor import GetNextNQuestionsInteractor
from assessment.storages.question_bank_question_storage import QuestionBankQuestionStorage
from assessment.storages.question_bank_storage import QuestionBankStorage
from assessment.storages.question_storage import QuestionStorage



def resolve_get_next_questions(self, info, params):
    try:
        interactor = GetNextNQuestionsInteractor(
            question_storage=QuestionStorage(),
            question_bank_storage=QuestionBankStorage(),
            question_bank_question_storage=QuestionBankQuestionStorage()
        )

        algorithm_enum = Algorithm[params.algorithm]

        difficulty_weights = None
        if params.difficultyWeights:
            difficulty_weights = {
                Difficulty[key]: value
                for key, value in params.difficultyWeights.items()
            }

        config = SelectionConfigDTO(
            question_bank_id=params.questionBankId,
            number_of_questions=params.numberOfQuestions,
            algorithm=algorithm_enum,
            already_attempted_questions=params.alreadyAttempted or [],
            difficulty_weights=difficulty_weights
        )

        questions = interactor.get_questions(config)

        return GetNextQuestionsResponse(
            bank_id=params.questionBankId,
            questions=[
                QuestionItemType(
                    question_id=q.question_id,
                    questionText=q.question_text,
                    questionType=q.question_type.name,
                    difficultyLevel=q.difficulty_level.name
                ) for q in questions
            ]
        )

    except QuestionBankNotFound as e:
        return BankNotFoundError(bankId=e.bank_id)

    except InvalidAlgorithmError:
        return InvalidAlgorithmError(message="Invalid algorithm")

    except ValueError as e:
        return InvalidNumberOfQuestionsError(message=str(e))

    except Exception as e:
        return DifficultyWeightError(message=str(e))
