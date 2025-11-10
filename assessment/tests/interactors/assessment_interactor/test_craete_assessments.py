import pytest
from unittest.mock import create_autospec
from faker import Faker

from cyber_edu_verse.assessment.interactors.assessment_interactor.create_assessment import (
    CreateAssessmentsInteractor,
)
from cyber_edu_verse.assessment.interactors.dtos import (
    AssessmentDTO
)
from cyber_edu_verse.assessment.interactors.storage_interface.assessments_storage_interface import (
    AssessmentStorageInterface,
)
from cyber_edu_verse.assessment.exceptions.custom_exceptions import (
    DuplicateQuestionsFound,
    InvalidAssessmentTypesFound,
    PassingMarksExceedTotalError,
)
from cyber_edu_verse.assessment.tests.factories.interactor_factories import (
    QuestionDTOFactory,
    CreateAssessmentDTOFactory,
)

Faker.seed(1)


class TestCreateAssessmentsInteractor:

    def setup_method(self):
        self.assessment_storage = create_autospec(AssessmentStorageInterface)
        self.interactor = CreateAssessmentsInteractor(
            assessment_storage=self.assessment_storage
        )

    def test_create_assessments_success(self, snapshot):
        q1 = QuestionDTOFactory(question_id="q1", question_text="Title 1",
                                options=[], correct_answer="A")
        q2 = QuestionDTOFactory(question_id="q2", question_text="Title 2",
                                options=[], correct_answer="B")

        create_assessment = CreateAssessmentDTOFactory(marks=30,
                                                       questions=[q1, q2],
                                                       pass_marks=15)

        expected_dto = AssessmentDTO(
            assessment_id="a1",
            assessment_title="Cyber Basics",
            assessment_type=create_assessment.assessment_type,
            description=create_assessment.description,
            icon="icon.png",
            questions=create_assessment.questions,
            attempts_limit=2,
            marks=30,
            pass_marks=create_assessment.pass_marks,
            estimate_duration_in_mins=30,
            no_of_questions=2,
        )

        self.assessment_storage.create_assessments.return_value = [
            expected_dto]

        result = self.interactor.create_assessments([create_assessment])

        snapshot.assert_match(repr(result), "create_assessment_success.json")

    def test_validate_no_duplicate_questions_found(self, snapshot):
        q1 = QuestionDTOFactory(question_id="q1", question_text="Title 1",
                                options=[], correct_answer="A")
        q2 = QuestionDTOFactory(question_id="q1", question_text="Title 2",
                                options=[], correct_answer="B")  # duplicate

        create_assessment = CreateAssessmentDTOFactory(
            assessment_title="Ethical Hacking",
            icon="icon.png",
            questions=[q1, q2],
            estimate_duration_in_mins=15,
            attempts_limit=2,
            marks=30,
            pass_marks=25
        )

        with pytest.raises(DuplicateQuestionsFound) as exc:
            self.interactor.create_assessments([create_assessment])

        snapshot.assert_match(repr(exc.value.question_ids),
                              "duplicate_question_found.json")

    def test_validate_multiple_assessments_no_duplicates(self, snapshot):
        topic_id = "topic_12"
        q1 = QuestionDTOFactory(question_id="q1", question_text="Q1",
                                options=[], question_type="MCQ",
                                correct_answer="A", topic_id=topic_id)
        q2 = QuestionDTOFactory(question_id="q2", question_text="Q2",
                                options=[], question_type="MCQ",
                                correct_answer="B", topic_id=topic_id)
        q3 = QuestionDTOFactory(question_id="q3", question_text="Q3",
                                options=[], question_type="MCQ",
                                correct_answer="C", topic_id=topic_id)

        assessment1 = CreateAssessmentDTOFactory(
            assessment_title="Course 1",
            icon="icon1.png",
            marks=30,
            pass_marks=25,
            questions=[q1, q2],
            estimate_duration_in_mins=10,
            attempts_limit=2,
        )

        assessment2 = CreateAssessmentDTOFactory(
            assessment_title="Course 2",
            icon="icon2.png",
            marks=30,
            pass_marks=25,
            questions=[q3],
            estimate_duration_in_mins=15,
            attempts_limit=1,
        )

        expected_dtos = [
            AssessmentDTO(
                assessment_id="a1",
                assessment_title="Course 1",
                description=assessment1.assessment_type,
                assessment_type=assessment1.assessment_type,
                icon="icon1.png",
                questions=assessment1.questions,
                marks=assessment1.marks,
                pass_marks=assessment1.pass_marks,
                estimate_duration_in_mins=10,
                attempts_limit=2,
                no_of_questions=2,
            ),
            AssessmentDTO(
                assessment_id="a2",
                assessment_title="Course 2",
                icon="icon2.png",
                description=assessment2.description,
                assessment_type=assessment1.assessment_type,
                questions=assessment2.questions,
                marks=assessment2.marks,
                pass_marks=assessment1.pass_marks,
                estimate_duration_in_mins=15,
                attempts_limit=1,
                no_of_questions=1,
            ),
        ]

        self.assessment_storage.create_assessments.return_value = expected_dtos

        result = self.interactor.create_assessments([assessment1, assessment2])

        snapshot.assert_match(repr(result),
                              "multiple_assessments_snapshot.txt")

    def test_invalid_assessment_type(self, snapshot):
        q1 = QuestionDTOFactory(question_id="q1", question_text="Title 1",
                                options=[], correct_answer="A")

        invalid_assessment = CreateAssessmentDTOFactory(
            assessment_type="INVALID_TYPE",
            questions=[q1],
            marks=50,
            pass_marks=25,
            icon="icon.png",
            estimate_duration_in_mins=20,
            attempts_limit=1,
        )

        with pytest.raises(InvalidAssessmentTypesFound) as exc:
            self.interactor.create_assessments([invalid_assessment])

        snapshot.assert_match(repr(exc.value.assessment_types),
                              "invalid_assessment_type.json")

    def test_passing_marks_exceed_total_marks(self, snapshot):
        q1 = QuestionDTOFactory(question_id="q1", question_text="Title 1",
                                options=[], correct_answer="A")

        invalid_assessment = CreateAssessmentDTOFactory(
            questions=[q1],
            marks=50,
            pass_marks=60,  # invalid
            icon="icon.png",
            estimate_duration_in_mins=30,
            attempts_limit=2,
        )

        with pytest.raises(PassingMarksExceedTotalError):
            self.interactor.create_assessments([invalid_assessment])

        snapshot.assert_match(
            f"PassingMarksExceedTotalError(passing_marks={invalid_assessment.pass_marks}, total_marks={invalid_assessment.marks})",
            "passing_marks_exceed_total.json",
        )
