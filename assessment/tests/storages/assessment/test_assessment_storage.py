import pytest

from assessment.interactors.dtos import CreateAssessmentDTO, AssessmentTypeEnum
from assessment.storages.assessment_storage import AssessmentStorage
from assessment.tests.factories.storage_factories import AssessmentFactory


class TestAssessment:

    @pytest.mark.django_db
    def test_assessment_exist(self, snapshot):
        assessment_id = "12345678-1234-5678-1234-567812345678"
        assessment_storage = AssessmentStorage()
        AssessmentFactory(assessment_id=assessment_id)

        result = assessment_storage.assessment_exists(
            assessment_id=assessment_id)

        (snapshot.assert_match(repr(result), "test_assessment_exists.txt"))

    @pytest.mark.django_db
    def test_create_assessments(self, snapshot):
        assessment_storage = AssessmentStorage()

        create_dtos = [
            CreateAssessmentDTO(
                assessment_title="Sample 1",
                description="Description 1",
                icon="icon1.png",
                assessment_type=AssessmentTypeEnum.QUIZ,
                no_of_questions=5,
                pass_percentage=60,
                easy_count=1,
                medium_count=2,
                hard_count=2,
                estimate_duration_in_mins=30,
                attempts_limit=0
            ),
            CreateAssessmentDTO(
                assessment_title="Sample 2",
                description="Description 2",
                icon="icon2.png",
                assessment_type=AssessmentTypeEnum.MODULE_EXAM,
                no_of_questions=10,
                pass_percentage=70,
                easy_count=2,
                medium_count=3,
                hard_count=5,
                estimate_duration_in_mins=60,
                attempts_limit=2
            )
        ]

        result = assessment_storage.create_assessments(create_dtos)

        output = [f"{x.assessment_title} - {x.assessment_type}" for x in
                  result]
        snapshot.assert_match(repr(output), "test_create_assessments.txt")

    @pytest.mark.django_db
    def test_get_assessment(self, snapshot):
        assessment_storage = AssessmentStorage()
        assessment_id = "12345678-1234-5678-1234-567812345678"

        AssessmentFactory(
            assessment_id=assessment_id,
            title="Get Test",
            description="desc",
            icon="icon.png",
            marks=70,
            pass_marks=52,
            assessment_type="QUIZ",
            no_of_questions=10,
            pass_percentage=75,
            easy_count=3,
            medium_count=4,
            hard_count=3,
            estimated_duration_in_minutes=45,
            attempts_limit=2
        )

        result = assessment_storage.get_assessment(assessment_id)

        snapshot.assert_match(repr(result), "test_get_assessment.txt")

    @pytest.mark.django_db
    def test_update_marks_in_assessment(self, snapshot):
        assessment_storage = AssessmentStorage()
        assessment_id = "12345678-1234-5678-1234-567812345678"

        assessment = AssessmentFactory(
            assessment_id=assessment_id,
            title="Update Test",
            description="desc",
            icon="icon.png",
            assessment_type="COURSE_EXAM",
            no_of_questions=20,
            pass_percentage=80,
            easy_count=5,
            medium_count=7,
            hard_count=8,
            estimated_duration_in_minutes=90,
            attempts_limit=4,
            marks=50,
            pass_marks=30
        )

        result = assessment_storage.update_marks_in_assessment(
            str(assessment.assessment_id), marks=90, pass_marks=60
        )

        snapshot.assert_match(repr(result),
                              "test_update_marks_in_assessment.txt")
