"""Create the Assessment Interactor"""
from assessment.exceptions.custom_exceptions import \
    InvalidAssessmentTypesFound, AssessmentInvalidPassPercentage
from assessment.interactors.common_validation_mixin import \
    AssessmentValidationMixIn
from assessment.interactors.dtos import AssessmentDTO, \
    CreateAssessmentDTO, AssessmentTypeEnum, CreateAssessmentDBDTO, \
    ScoreConfigDTO, Difficulty, ResponseEnum
from assessment.interactors.storage_interface.assessments_storage_interface import \
    AssessmentStorageInterface


class CreateAssessmentsInteractor(AssessmentValidationMixIn):
    """Create Assessments Interactor"""

    def __init__(self, assessment_storage: AssessmentStorageInterface):
        self.assessment_storage = assessment_storage

    def create_assessments(self, assessments: list[CreateAssessmentDTO]) -> \
            list[AssessmentDTO]:
        """Create the assessments"""
        assessment_types = [assessment.assessment_type for assessment in
                            assessments]

        self._validate_assessment_type(assessment_types=assessment_types)
        self._validate_the_percentage(assessments=assessments)
        assessments_data = self._calculate_marks_assessments(assessments=assessments)

        return self.assessment_storage.create_assessments(
            assessments=assessments_data)

    @staticmethod
    def _validate_assessment_type(assessment_types: list[AssessmentTypeEnum]):
        """ Validate the assessments types"""
        valid_assessment_types = [each_type.value for each_type in
                                  AssessmentTypeEnum]
        invalid_assessment_types = []
        for each_type in assessment_types:
            type_value = each_type.value if hasattr(each_type,
                                                    "value") else each_type
            if type_value not in valid_assessment_types:
                invalid_assessment_types.append(type_value)

        if invalid_assessment_types:
            raise InvalidAssessmentTypesFound(
                assessment_types=invalid_assessment_types)

    @staticmethod
    def _validate_the_percentage(assessments: list[CreateAssessmentDTO]):
        """ Validate the passing percentage in each assessment """
        percentages = [obj.pass_percentage for obj in assessments]

        invalid_percentages = [each for each in percentages if
                               each > 100 or each < 0]

        if invalid_percentages:
            raise AssessmentInvalidPassPercentage(
                percentages=invalid_percentages)

    def _calculate_marks_assessments(self,
                                     assessments: list[CreateAssessmentDTO]
                                     ) -> list[CreateAssessmentDBDTO]:

        assessment_data = []

        for each in assessments:

            if each.assessment_type == AssessmentTypeEnum.QUIZ:

                marks = each.no_of_questions * self.fixed_scoring(True)
                pass_marks = round(marks * (each.pass_percentage / 100))

                assessment_data.append(
                    CreateAssessmentDBDTO(
                        assessment_title=each.assessment_title,
                        assessment_type=each.assessment_type,
                        topic_id=each.topic_id,
                        description=each.description,
                        icon=each.icon,
                        no_of_questions=each.no_of_questions,
                        pass_marks=pass_marks,
                        marks=marks,
                        attempts_limit=each.attempts_limit,
                        pass_percentage=each.pass_percentage,
                        easy_count=None,
                        medium_count=None,
                        hard_count=None,
                        estimate_duration_in_mins=each.estimate_duration_in_mins
                    )
                )
                continue

            easy_marks = (each.easy_count or 0) * ScoreConfigDTO.points[Difficulty.EASY][
                ResponseEnum.CORRECT.value]
            medium_marks = (each.medium_count or 0) * \
                           ScoreConfigDTO.points[Difficulty.MEDIUM][ResponseEnum.CORRECT.value]
            hard_marks = (each.hard_count or 0) * ScoreConfigDTO.points[Difficulty.HARD][
                ResponseEnum.CORRECT.value]

            marks = easy_marks + medium_marks + hard_marks
            pass_marks = round(marks * (each.pass_percentage / 100))

            assessment_data.append(
                CreateAssessmentDBDTO(
                    assessment_title=each.assessment_title,
                    assessment_type=each.assessment_type,
                    topic_id=each.topic_id,
                    description=each.description,
                    icon=each.icon,
                    no_of_questions=each.no_of_questions,
                    pass_marks=pass_marks,
                    marks=marks,
                    attempts_limit=each.attempts_limit,
                    pass_percentage=each.pass_percentage,
                    easy_count=each.easy_count,
                    medium_count=each.medium_count,
                    hard_count=each.hard_count,
                    estimate_duration_in_mins=each.estimate_duration_in_mins
                )
            )

        return assessment_data
