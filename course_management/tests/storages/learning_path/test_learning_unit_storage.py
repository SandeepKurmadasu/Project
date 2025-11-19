import pytest

from course_management.interactors.dtos import CreateLearningUnitDTO
from course_management.storages.learning_unit_storage import \
    LearningUnitStorage
from course_management.tests.factories.storage_factories import \
    LearningUnitFactory, CourseFactory, TopicFactory, ModuleFactory, \
    CourseLearningPathFactory


class TestLearningUnit:

    @pytest.mark.django_db
    def test_check_learning_unit_exists(self, snapshot):
        # Arrange
        learning_unit_id = "12345678-1234-5678-1234-567812345123"
        learning_path_id = "12345678-1234-5678-1234-567812345127"
        course = CourseFactory(
            course_id="12345678-1234-5678-1234-567812345124",
            title="Test Title")
        module = ModuleFactory(
            module_id="12345678-1234-5678-1234-567812345126",
            module_title="Test module title")
        topic = TopicFactory(topic_id="12345678-1234-5678-1234-567812345125",
                             module=module)

        learning_path = CourseLearningPathFactory(
            learning_path_id=learning_path_id, course=course)

        LearningUnitFactory(learning_unit_id=learning_unit_id,
                            learning_path=learning_path, topic=topic)
        learning_unit_storage = LearningUnitStorage()

        # Act

        result = learning_unit_storage.check_learning_unit_exists(
            learning_unit_id=learning_unit_id)

        # Assert
        snapshot.assert_match(repr(result), "test_learning_unit_exists.txt")

    @pytest.mark.django_db
    def test_get_learning_unit(self, snapshot):
        # Arrange
        learning_unit_id = "12345678-1234-5678-1234-567812345123"
        learning_path_id = "12345678-1234-5678-1234-567812345127"
        course = CourseFactory(
            course_id="12345678-1234-5678-1234-567812345124",
            title="Test Title")
        module = ModuleFactory(
            module_id="12345678-1234-5678-1234-567812345126",
            module_title="Test module title")
        topic = TopicFactory(topic_id="12345678-1234-5678-1234-567812345125",
                             module=module, topic_title="Test_topic_title")

        learning_path = CourseLearningPathFactory(
            learning_path_id=learning_path_id, course=course)

        LearningUnitFactory(learning_unit_id=learning_unit_id,
                            learning_path=learning_path, topic=topic)
        learning_unit_storage = LearningUnitStorage()

        # Act

        result = learning_unit_storage.get_learning_unit(
            learning_unit_id=learning_unit_id)

        # Assert
        snapshot.assert_match(repr(result), "test_get_learning_unit.txt")

    @pytest.mark.django_db
    def test_create_learning_units(self, snapshot):
        # Arrange
        learning_path_id = "12345678-1234-5678-1234-567812345123"
        course_id = "12345678-1234-5678-1234-567812340001"

        course = CourseFactory(
            course_id=course_id,
            title="Test Course"
        )

        module = ModuleFactory(
            module_id="12345678-1234-5678-1234-567812340002",
            course=course,
            module_title="Test Module"
        )

        topic1 = TopicFactory(
            topic_id="12345678-1234-5678-1234-567812340003",
            module=module,
            topic_title="Topic 1",
            topic_type="LEARNING",
            estimated_duration_in_mins=15
        )
        topic2 = TopicFactory(
            topic_id="12345678-1234-5678-1234-567812340004",
            module=module,
            topic_title="Topic 2",
            topic_type="LEARNING",
            estimated_duration_in_mins=20
        )

        CourseLearningPathFactory(
            learning_path_id=learning_path_id,
            course=course
        )

        learning_unit_storage = LearningUnitStorage()

        learning_units_input = [
            CreateLearningUnitDTO(
                learning_path_id=learning_path_id,
                topic_id=topic1.topic_id,
                order=1
            ),
            CreateLearningUnitDTO(
                learning_path_id=learning_path_id,
                topic_id=topic2.topic_id,
                order=2
            ),
        ]

        # Act
        result = learning_unit_storage.create_learning_units(
            learning_units=learning_units_input
        )

        # Assert
        snapshot.assert_match(
            repr([(lu.unit_title, lu.order) for lu in result]),
            "test_create_learning_units.txt"
        )

    @pytest.mark.django_db
    def test_get_learning_units_by_learning_path_id(self, snapshot):
        # Arrange
        learning_path_id = "12345678-1234-5678-1234-567812349900"
        course_id = "12345678-1234-5678-1234-567812349901"

        course = CourseFactory(
            course_id=course_id,
            title="Fixed Course"
        )

        module = ModuleFactory(
            module_id="12345678-1234-5678-1234-567812349902",
            module_title="Fixed Module",
            course=course
        )

        topic1 = TopicFactory(
            topic_id="12345678-1234-5678-1234-567812349903",
            module=module,
            topic_title="Topic One",
            topic_type="LEARNING",
            estimated_duration_in_mins=10
        )

        topic2 = TopicFactory(
            topic_id="12345678-1234-5678-1234-567812349904",
            module=module,
            topic_title="Topic Two",
            topic_type="LEARNING",
            estimated_duration_in_mins=20
        )

        learning_path = CourseLearningPathFactory(
            learning_path_id=learning_path_id,
            course=course
        )

        LearningUnitFactory(
            learning_unit_id="12345678-1234-5678-1234-567812349910",
            learning_path=learning_path,
            topic=topic1,
            order=1
        )

        LearningUnitFactory(
            learning_unit_id="12345678-1234-5678-1234-567812349911",
            learning_path=learning_path,
            topic=topic2,
            order=2
        )

        learning_unit_storage = LearningUnitStorage()

        # Act
        result = learning_unit_storage.get_learning_units_by_learning_path_id(
            learning_path_id=learning_path_id
        )

        # Assert
        snapshot.assert_match(repr(result),
                              "test_get_learning_units_by_learning_path_id.txt")
