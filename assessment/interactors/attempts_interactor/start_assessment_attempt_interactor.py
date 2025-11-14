from assessment.interactors.common_validation_mixin import \
    AssessmentValidationMixIn
from assessment.interactors.dtos import Algorithm, AssessmentAttemptDTO, \
    QuestionDTO, SelectionConfigDTO, AssessmentTypeEnum, Difficulty, \
    ScoreConfigDTO, ResponseEnum
from assessment.interactors.question_selection.get_next_n_questions_interactor import \
    GetNextNQuestionsInteractor
from assessment.interactors.storage_interface.assessment_attempt_storage_interface import \
    AttemptStorageInterface
from assessment.interactors.storage_interface.assessments_storage_interface import \
    AssessmentStorageInterface
from assessment.interactors.storage_interface.question_storage_interface import \
    QuestionStorageInterface
from assessment.interactors.storage_interface.question_bank_storage_interface import \
    QuestionBankStorageInterface
from course_management.interactors.common_validation_mixin import \
    ValidationMixIn
from course_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface


class StartAssessmentAttemptInteractor(ValidationMixIn,
                                       AssessmentValidationMixIn):
    """Start the user assessment attempt interactor"""

    def __init__(self, attempt_storage: AttemptStorageInterface,
                 user_storage: UserStorageInterface,
                 assessments_storage: AssessmentStorageInterface,
                 question_storage: QuestionStorageInterface,
                 question_bank_storage: QuestionBankStorageInterface):
        self.attempt_storage = attempt_storage
        self.user_storage = user_storage
        self.assessments_storage = assessments_storage
        self.question_storage = question_storage
        self.question_bank_storage = question_bank_storage

    def start_assessment_attempt(self, user_id: str, assessment_id: str) \
            -> AssessmentAttemptDTO:
        """Start the user attempt for assessment"""

        self.check_user_exists(user_id=user_id, user_storage=self.user_storage)
        self.validate_assessment_exists(assessment_id=assessment_id,
                                        assessment_storage=self.assessments_storage)

        assessment_data = self.assessments_storage.get_assessment(
            assessment_id=assessment_id)

        diff_mixin = [{}]
        if assessment_data.assessment_type == AssessmentTypeEnum.QUIZ:
            algo = Algorithm.FIXED
        elif assessment_data.assessment_type == AssessmentTypeEnum.MODULE_EXAM:
            algo = Algorithm.RANDOM
        else:
            algo = Algorithm.DIFFICULTY_MIX

        if assessment_data.assessment_type == AssessmentTypeEnum.COURSE_EXAM:
            diff_mixin.append({Difficulty.EASY: assessment_data.easy_count,
                               Difficulty.MEDIUM: assessment_data.medium_count,
                               Difficulty.HARD: assessment_data.hard_count})

        bank_data = self.question_bank_storage.get_assessment_question_bank(
            assessment_id=assessment_id)

        questions = self.get_next_n_questions(user_id=user_id,
                                              bank_id=bank_data.bank_id,
                                              diff_mixin=diff_mixin,
                                              question_selection=algo,
                                              assessment_id=assessment_id,
                                              no_of_questions=assessment_data.no_of_questions)
        self._calculate_and_update_assessment_marks(
            assessment_id=assessment_id,
            percentage=assessment_data.pass_percentage, questions=questions)

        question_ids = [obj.question_id for obj in questions]

        return self.attempt_storage.create_assessment_attempt(
            user_id=user_id,
            assessment_id=assessment_id,
            question_ids=question_ids)

    def get_next_n_questions(self, user_id: str, question_selection: Algorithm,
                             assessment_id: str, no_of_questions: int,
                             diff_mixin: list[dict[Difficulty, int]] | None,
                             bank_id: str) -> list[QuestionDTO]:
        """Get next N questions skipping already attempted (for random/difficulty)."""

        previously_attempted_questions = self.attempt_storage.get_assessment_attempted_questions(
            user_id=user_id,
            assessment_id=assessment_id)

        previously_attempted_question_ids = [obj.question_id for obj in
                                             previously_attempted_questions]

        get_question_interactor = GetNextNQuestionsInteractor(
            question_storage=self.question_storage,
            question_bank_storage=self.question_bank_storage)

        get_question_input = SelectionConfigDTO(
            question_bank_id=bank_id,
            number_of_questions=no_of_questions,
            algorithm=question_selection,
            already_attempted_questions=previously_attempted_question_ids,
            difficulty_weights=diff_mixin
        )

        questions = get_question_interactor.get_questions(get_question_input)

        return questions

    def _calculate_and_update_assessment_marks(self, percentage: int,
                                               assessment_id: str,
                                               questions: list[QuestionDTO]):
        questions_types = [obj.difficulty_level.value for obj in questions]

        easy_count = questions_types.count(Difficulty.EASY.value)
        medium_count = questions_types.count(Difficulty.MEDIUM.value)
        hard_count = questions_types.count(Difficulty.HARD.value)

        easy_mark = ScoreConfigDTO.points.get(Difficulty.EASY)
        medium_mark = ScoreConfigDTO.points.get(Difficulty.MEDIUM)
        hard_mark = ScoreConfigDTO.points.get(Difficulty.HARD)

        total_marks = (easy_count * easy_mark[ResponseEnum.CORRECT]) + (
                medium_count * medium_mark[ResponseEnum.CORRECT]) + (
                              hard_count * hard_mark[ResponseEnum.CORRECT])

        pass_marks = total_marks * (percentage // 100)

        return self.assessments_storage.update_marks_in_assessment(
            assessment_id=assessment_id, marks=total_marks,
            pass_marks=pass_marks)
