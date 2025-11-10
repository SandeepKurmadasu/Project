from assessment.interactors.dtos import AssessmentDTO, \
    CreateAssessmentDTO
from assessment.interactors.storage_interface.assessments_storage_interface import \
    AssessmentStorageInterface
from assessment.models import Assessment


class AssessmentStorage(AssessmentStorageInterface):

    def assessment_exists(self, assessment_id: str) -> bool:
        return Assessment.objects.filter(assessment_id=assessment_id).exists()

    def create_assessments(self, assessments: list[CreateAssessmentDTO]) -> \
            list[AssessmentDTO]:
        assessment_instances = [
            Assessment(
                title=assessment.assessment_title,
                description=assessment.description,
                icon=assessment.icon,
                assessment_type=assessment.assessment_type,
                pass_marks=assessment.pass_marks,
                marks=assessment.marks,
                estimated_duration_in_minutes=assessment.estimate_duration_in_mins,
                attempts_limit=assessment.attempts_limit
            ) for assessment in assessments
        ]
        created_assessments = Assessment.objects.bulk_create(
            assessment_instances)

        return created_assessments

    def get_assessment(self, assessment_id: str) -> AssessmentDTO:
        assessment = Assessment.objects.get(assessment_id=assessment_id)

        return AssessmentDTO(
            assessment_id=assessment_id,
            assessment_title=assessment.title,
            assessment_type=assessment.assessment_type,
            description=assessment.description,
            pass_marks=assessment.pass_marks,
            icon=assessment.icon,
            marks=assessment.marks,
            no_of_questions=len(assessment.questions),
            questions=assessment.questions,
            estimate_duration_in_mins=assessment.estimated_duration_in_minutes,
            attempts_limit=assessment.attempts_limit
        )
