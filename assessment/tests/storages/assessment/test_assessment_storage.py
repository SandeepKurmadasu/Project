import uuid

import pytest

from assessment.interactors.dtos import CreateAssessmentDTO, \
    AssessmentTypeEnum, CreateAssessmentDBDTO
from assessment.storages.assessment_storage import AssessmentStorage
from assessment.tests.factories.storage_factories import AssessmentFactory
from course_management.tests.factories.storage_factories import CourseFactory, \
    TopicFactory


class TestAssessment:

    @pytest.mark.django_db
    def test_assessment_exist(self, snapshot):
        assessment_id = "12345678-1234-5678-1234-567812345678"
        topic = TopicFactory()
        assessment_storage = AssessmentStorage()
        AssessmentFactory(assessment_id=assessment_id)

        result = assessment_storage.assessment_exists(
            assessment_id=assessment_id)

        (snapshot.assert_match(repr(result), "test_assessment_exists.txt"))

    @pytest.mark.django_db
    def test_create_assessments(self, snapshot):
        assessment_storage = AssessmentStorage()
        topic = TopicFactory()

        create_dtos = [
            CreateAssessmentDBDTO(
                topic_id=str(topic.topic_id),
                assessment_title="Sample 1",
                description="Description 1",
                icon="icon1.png",
                assessment_type=AssessmentTypeEnum.QUIZ,
                no_of_questions=5,
                pass_percentage=70,
                easy_count=1,
                medium_count=2,
                hard_count=2,
                estimate_duration_in_mins=30,
                attempts_limit=0,
                marks=30,
                pass_marks=21
            )
        ]

        result = assessment_storage.create_assessments(create_dtos)

        output = [f"{x.assessment_title} - {x.assessment_type}" for x in
                  result]
        snapshot.assert_match(repr(output), "test_create_assessments.txt")

    @pytest.mark.django_db
    def test_get_assessment(self, snapshot):
        # Use fixed UUIDs for reproducible tests
        fixed_topic_id = uuid.UUID('1d39093b-fd67-45d1-adc9-ff2d1f9d9180')
        fixed_assessment_id = uuid.UUID('16753fc0-de9b-4bf4-92dc-22b7bfc32c0e')

        topic = TopicFactory(topic_id=fixed_topic_id)
        assessment_storage = AssessmentStorage()

        assessment = AssessmentFactory(
            assessment_id=fixed_assessment_id,
            topic=topic,
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

        result = assessment_storage.get_assessment(str(assessment.assessment_id))
        snapshot.assert_match(repr(result), "test_get_assessment.txt")
