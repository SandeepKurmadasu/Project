import uuid

import pytest
from unittest.mock import create_autospec
from faker import Faker

from assessment.interactors.assessment_interactor.create_assessments import (
    CreateAssessmentsInteractor,
)
from assessment.interactors.dtos import (
    AssessmentDTO, CreateAssessmentDTO
)
from assessment.interactors.storage_interface.assessments_storage_interface import (
    AssessmentStorageInterface,
)
from assessment.exceptions.custom_exceptions import (
    InvalidAssessmentTypesFound,
    PassingMarksExceedTotalError,
)
from assessment.tests.factories.factories import CreateAssessmentDTOFactory

Faker.seed(1)


class TestCreateAssessmentsInteractor:

    def setup_method(self):
        self.assessment_storage = create_autospec(AssessmentStorageInterface)
        self.interactor = CreateAssessmentsInteractor(
            assessment_storage=self.assessment_storage
        )

    def test_create_assessments_success(self, snapshot):
        # Use fixed UUID instead of factory
        fixed_topic_id = uuid.UUID('c5364284-84cd-4958-ada7-f05446826cd0')  # Changed variable name

        create_assessment = CreateAssessmentDTO(
            topic_id=str(fixed_topic_id),
            assessment_title="Cyber Basics",
            assessment_type="QUIZ",
            description="Test description",
            icon="icon.png",
            estimate_duration_in_mins=30,
            attempts_limit=2,
            pass_percentage=80,
            easy_count=2,
            medium_count=2,
            hard_count=1,
            no_of_questions=5,
        )

        expected_dto = AssessmentDTO(
            assessment_id="a1",
            assessment_title="Cyber Basics",
            assessment_type=create_assessment.assessment_type,
            description=create_assessment.description,
            icon="icon.png",
            attempts_limit=2,
            topic_id=create_assessment.topic_id,  # Changed from course_id
            marks=30,
            pass_percentage=create_assessment.pass_percentage,
            easy_count=create_assessment.easy_count,
            medium_count=create_assessment.medium_count,
            hard_count=create_assessment.hard_count,
            pass_marks=24,
            estimate_duration_in_mins=30,
            no_of_questions=5,
        )

        self.assessment_storage.create_assessments.return_value = [expected_dto]

        result = self.interactor.create_assessments([create_assessment])

        snapshot.assert_match(repr(result), "create_assessment_success.json")

    def test_validate_multiple_assessments_no_duplicates(self, snapshot):
        # Use fixed UUIDs
        fixed_topic_id1 = uuid.UUID('c5364284-84cd-4958-ada7-f05446826cd0')  # Changed variable name
        fixed_topic_id2 = uuid.UUID('d6475395-95de-5069-beb8-f16557937de1')  # Changed variable name

        assessment1 = CreateAssessmentDTO(
            topic_id=fixed_topic_id1,  # Changed from course_id
            assessment_title="Course 1",
            assessment_type="QUIZ",
            description="Description 1",
            icon="icon1.png",
            estimate_duration_in_mins=10,
            attempts_limit=2,
            pass_percentage=80,
            easy_count=1,
            medium_count=1,
            hard_count=0,
            no_of_questions=2,
        )

        assessment2 = CreateAssessmentDTO(
            topic_id=fixed_topic_id2,  # Changed from course_id
            assessment_title="Course 2",
            assessment_type="QUIZ",
            description="Description 2",
            icon="icon2.png",
            estimate_duration_in_mins=15,
            attempts_limit=1,
            pass_percentage=70,
            easy_count=1,
            medium_count=0,
            hard_count=0,
            no_of_questions=1,
        )

        expected_dtos = [
            AssessmentDTO(
                assessment_id="a1",
                assessment_title="Course 1",
                description=assessment1.description,
                assessment_type=assessment1.assessment_type,
                icon="icon1.png",
                marks=30,
                topic_id=assessment1.topic_id,  # Changed from course_id
                pass_percentage=assessment1.pass_percentage,
                easy_count=assessment1.easy_count,
                medium_count=assessment1.medium_count,
                hard_count=assessment1.hard_count,
                pass_marks=24,
                estimate_duration_in_mins=10,
                attempts_limit=2,
                no_of_questions=2,
            ),
            AssessmentDTO(
                assessment_id="a2",
                assessment_title="Course 2",
                icon="icon2.png",
                description=assessment2.description,
                assessment_type=assessment2.assessment_type,
                marks=30,
                topic_id=assessment2.topic_id,  # Changed from course_id
                pass_percentage=assessment2.pass_percentage,
                easy_count=assessment2.easy_count,
                medium_count=assessment2.medium_count,
                hard_count=assessment2.hard_count,
                pass_marks=21,
                estimate_duration_in_mins=15,
                attempts_limit=1,
                no_of_questions=1,
            ),
        ]

        self.assessment_storage.create_assessments.return_value = expected_dtos

        result = self.interactor.create_assessments([assessment1, assessment2])

        snapshot.assert_match(repr(result), "multiple_assessments_snapshot.txt")

    def test_invalid_assessment_type(self, snapshot):
        invalid_assessment = CreateAssessmentDTOFactory(
            assessment_type="INVALID_TYPE",
            icon="icon.png",
            estimate_duration_in_mins=20,
            attempts_limit=1,
        )

        with pytest.raises(InvalidAssessmentTypesFound) as exc:
            self.interactor.create_assessments([invalid_assessment])

        snapshot.assert_match(repr(exc.value.assessment_types),
                              "invalid_assessment_type.json")
