from assessment.interactors.dtos import AssessmentDTO, \
    CreateAssessmentDBDTO
from assessment.interactors.storage_interface.assessments_storage_interface import \
    AssessmentStorageInterface
from assessment.models import Assessment
from course_management.models import Course, Topic


class AssessmentStorage(AssessmentStorageInterface):

    def assessment_exists(self, assessment_id: str) -> bool:
        return Assessment.objects.filter(assessment_id=assessment_id).exists()

    def create_assessments(self, assessments: list[CreateAssessmentDBDTO]) -> \
            list[AssessmentDTO]:
        topic = Topic.objects.get(topic_id=assessments[0].topic_id)
        assessment_data = [
            Assessment(
                title=assessment.assessment_title,
                description=assessment.description,
                icon=assessment.icon,
                topic=topic,
                assessment_type=assessment.assessment_type,
                no_of_questions=assessment.no_of_questions,
                pass_percentage=assessment.pass_percentage,
                easy_count=assessment.easy_count,
                medium_count=assessment.medium_count,
                hard_count=assessment.hard_count,
                estimated_duration_in_minutes=assessment.estimate_duration_in_mins,
                attempts_limit=assessment.attempts_limit,
                marks=assessment.marks,
                pass_marks=assessment.pass_marks

            ) for assessment in assessments
        ]
        created_assessments = Assessment.objects.bulk_create(
            assessment_data)

        return [AssessmentDTO(
            assessment_id=assessment.assessment_id,
            assessment_title=assessment.title,
            topic_id=assessment.topic.topic_id,
            assessment_type=assessment.assessment_type,
            description=assessment.description,
            pass_marks=assessment.pass_marks,
            icon=assessment.icon,
            marks=assessment.marks,
            pass_percentage=assessment.pass_percentage,
            no_of_questions=assessment.no_of_questions,
            easy_count=assessment.easy_count,
            medium_count=assessment.medium_count,
            hard_count=assessment.hard_count,
            estimate_duration_in_mins=assessment.estimated_duration_in_minutes,
            attempts_limit=assessment.attempts_limit
        ) for assessment in created_assessments]

    def get_assessment(self, assessment_id: str) -> AssessmentDTO:
        assessment = Assessment.objects.get(assessment_id=assessment_id)

        return AssessmentDTO(
            assessment_id=assessment_id,
            assessment_title=assessment.title,
            topic_id=assessment.topic.topic_id,
            assessment_type=assessment.assessment_type,
            description=assessment.description,
            pass_marks=assessment.pass_marks,
            icon=assessment.icon,
            marks=assessment.marks,
            pass_percentage=assessment.pass_percentage,
            no_of_questions=assessment.no_of_questions,
            easy_count=assessment.easy_count,
            medium_count=assessment.medium_count,
            hard_count=assessment.hard_count,
            estimate_duration_in_mins=assessment.estimated_duration_in_minutes,
            attempts_limit=assessment.attempts_limit
        )

    def update_marks_in_assessment(self, assessment_id: str, marks: int,
                                   pass_marks: int) -> AssessmentDTO:
        assessment = Assessment.objects.get(assessment_id=assessment_id)

        assessment.marks = marks
        assessment.pass_marks = pass_marks
        assessment.save()

        return AssessmentDTO(
            assessment_id=assessment_id,
            assessment_title=assessment.title,
            topic_id=assessment.topic.topic_id,
            assessment_type=assessment.assessment_type,
            description=assessment.description,
            pass_marks=assessment.pass_marks,
            icon=assessment.icon,
            marks=assessment.marks,
            pass_percentage=assessment.pass_percentage,
            no_of_questions=assessment.no_of_questions,
            easy_count=assessment.easy_count,
            medium_count=assessment.medium_count,
            hard_count=assessment.hard_count,
            estimate_duration_in_mins=assessment.estimated_duration_in_minutes,
            attempts_limit=assessment.attempts_limit
        )
