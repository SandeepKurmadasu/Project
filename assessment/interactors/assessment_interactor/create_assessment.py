"""Create the Assessment Interactor"""
from assessment.exceptions.custom_exceptions import \
    DuplicateQuestionsFound, InvalidAssessmentTypesFound, \
    PassingMarksExceedTotalError
from assessment.interactors.dtos import AssessmentDTO, \
    CreateAssessmentDTO, AssessmentTypeEnum
from assessment.interactors.dtos import QuestionDTO
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
        self._validate_the_passing_marks(assessments=assessments)

        return self.assessment_storage.create_assessments(
            assessments=assessments)

    @staticmethod
    def validate_no_duplicate_questions(questions: list[QuestionDTO]):
        """Validate the no duplicate question in each assessment """
        unique_ids = []
        duplicates = []

        for question in questions:
            if question.question_id in unique_ids:
                duplicates.append(question.question_id)
            else:
                unique_ids.append(question.question_id)

        if duplicates:
            raise DuplicateQuestionsFound(question_ids=duplicates)

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
    def _validate_the_passing_marks(assessments: list[CreateAssessmentDTO]):
        """ Validate the passing marks are less than or equal to the total marks"""

        for assessment in assessments:
            if assessment.marks < assessment.pass_marks:
                raise PassingMarksExceedTotalError(
                    passing_marks=assessment.pass_marks,
                    total_marks=assessment.marks,
                )
