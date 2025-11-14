"""Create the Assessment Interactor"""
from assessment.exceptions.custom_exceptions import \
    InvalidAssessmentTypesFound, AssessmentInvalidPassPercentage
from assessment.interactors.dtos import AssessmentDTO, \
    CreateAssessmentDTO, AssessmentTypeEnum
from assessment.interactors.storage_interface.assessments_storage_interface import \
    AssessmentStorageInterface


class CreateAssessmentsInteractor:
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

        return self.assessment_storage.create_assessments(
            assessments=assessments)

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
            AssessmentInvalidPassPercentage(percentages=invalid_percentages)
