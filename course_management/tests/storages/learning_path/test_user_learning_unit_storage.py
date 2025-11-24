import pytest

from course_management.interactors.dtos import CreateUserLearningUnit, \
    UpdateLearningUnitProgressDTO, AttemptedTopicStatusEnum
from course_management.storages.user_learning_unit_storage import \
    UserLearningUnitStorage
from course_management.tests.factories.storage_factories import \
    UserLearningPathFactory, LearningUnitFactory, UserLearningUnitFactory, \
    CourseLearningPathFactory, UserFactory, CourseFactory, TopicFactory


class TestUserLearningUnit:

    @pytest.mark.django_db
    def test_create_user_learning_units(self, snapshot):
        user_learning_path_id = "12345678-1234-5678-1234-567812345130"
        learning_unit_id_1 = "22345678-1234-5678-1234-567812345131"
        learning_unit_id_2 = "32345678-1234-5678-1234-567812345132"

        UserLearningPathFactory(user_learning_path_id=user_learning_path_id)
        LearningUnitFactory(learning_unit_id=learning_unit_id_1)
        LearningUnitFactory(learning_unit_id=learning_unit_id_2)

        user_learning_units_dto = [
            CreateUserLearningUnit(user_learning_path_id=user_learning_path_id,
                                   learning_unit_id=learning_unit_id_1),
            CreateUserLearningUnit(user_learning_path_id=user_learning_path_id,
                                   learning_unit_id=learning_unit_id_2),
        ]

        storage = UserLearningUnitStorage()

        result = storage.create_user_learning_units(user_learning_units_dto)

        snapshot.assert_match(repr(result),
                              "test_create_user_learning_units.txt")

    @pytest.mark.django_db
    def test_get_all_user_learning_unit_progress(self, snapshot):
        user_learning_path_id = "12345678-1234-5678-1234-567812345130"
        learning_unit_id_1 = "22345678-1234-5678-1234-567812345131"
        learning_unit_id_2 = "32345678-1234-5678-1234-567812345132"

        user_learning_path = UserLearningPathFactory(
            user_learning_path_id=user_learning_path_id)
        unit1 = LearningUnitFactory(learning_unit_id=learning_unit_id_1,
                                    order=1)
        unit2 = LearningUnitFactory(learning_unit_id=learning_unit_id_2,
                                    order=2)

        UserLearningUnitFactory(user_learning_path=user_learning_path,
                                learning_unit=unit1, percentage=50,
                                status="IN_PROGRESS")
        UserLearningUnitFactory(user_learning_path=user_learning_path,
                                learning_unit=unit2, percentage=100,
                                status="COMPLETED")

        storage = UserLearningUnitStorage()

        result = storage.get_all_user_learning_unit_progress(
            user_learning_path_id=user_learning_path_id)

        snapshot.assert_match(repr(result),
                              "test_get_all_user_learning_unit_progress.txt")

    @pytest.mark.django_db
    def test_get_user_learning_unit_progress(self, snapshot):
        user_learning_path_id = "12345678-1234-5678-1234-567812345130"
        learning_unit_id = "22345678-1234-5678-1234-567812345131"

        user_learning_path = UserLearningPathFactory(
            user_learning_path_id=user_learning_path_id)
        learning_unit = LearningUnitFactory(learning_unit_id=learning_unit_id,
                                            order=1)

        UserLearningUnitFactory(
            user_learning_path=user_learning_path,
            learning_unit=learning_unit,
            percentage=25,
            status="IN_PROGRESS",
            is_locked=False
        )

        storage = UserLearningUnitStorage()

        result = storage.get_user_learning_unit_progress(
            user_learning_path_id=user_learning_path_id,
            learning_unit_id=learning_unit_id)

        snapshot.assert_match(repr(result),
                              "test_get_user_learning_unit_progress.txt")

    @pytest.mark.django_db
    def test_update_learning_unit_progress(self, snapshot):
        user_learning_path_id = "12345678-1234-5678-1234-567812345130"
        learning_unit_id = "22345678-1234-5678-1234-567812345131"

        user_learning_path = UserLearningPathFactory(
            user_learning_path_id=user_learning_path_id)
        learning_unit = LearningUnitFactory(learning_unit_id=learning_unit_id)

        user_unit = UserLearningUnitFactory(
            user_learning_path=user_learning_path,
            learning_unit=learning_unit,
            percentage=30,
            status="IN_PROGRESS"
        )

        storage = UserLearningUnitStorage()

        update_dto = UpdateLearningUnitProgressDTO(
            user_learning_path_id=user_learning_path_id,
            user_learning_unit_id=user_unit.id,
            percentage=80,
            status=AttemptedTopicStatusEnum.COMPLETE
        )

        result = storage.update_learning_unit_progress(update_dto)

        snapshot.assert_match(repr(result),
                              "test_update_learning_unit_progress.txt")

    @pytest.mark.django_db
    def test_get_next_learning_unit(self, snapshot):
        user_id = "12345678-1234-5678-1234-567812345123"
        learning_path_id = "12345678-1234-5678-1234-567812345127"
        user_learning_path_id = "12345678-1234-5678-1234-567812345130"

        user = UserFactory(user_id=user_id)
        course = CourseFactory(
            course_id="12345678-1234-5678-1234-567812345124")
        course_learning_path = CourseLearningPathFactory(
            learning_path_id=learning_path_id,
            course=course
        )

        first_unit = LearningUnitFactory(
            learning_unit_id="12345678-1234-5678-1234-567812345125",
            learning_path=course_learning_path,
            order=1
        )
        second_unit = LearningUnitFactory(
            learning_unit_id="12345678-1234-5678-1234-567812345126",
            learning_path=course_learning_path,
            order=2
        )

        user_learning_path = UserLearningPathFactory(
            user_learning_path_id=user_learning_path_id,
            user=user,
            learning_path=course_learning_path,
            current_learning_unit=first_unit,
            overall_percentage=50,
            status="IN_PROGRESS"
        )

        UserLearningUnitFactory(
            user_learning_path=user_learning_path,
            learning_unit=first_unit,
            is_locked=False,
            status="COMPLETED",
            percentage=100
        )
        UserLearningUnitFactory(
            user_learning_path=user_learning_path,
            learning_unit=second_unit,
            is_locked=True,
            status="LOCKED",
            percentage=0
        )

        storage = UserLearningUnitStorage()

        result = storage.get_next_learning_unit(
            user_learning_path_id=str(
                user_learning_path.user_learning_path_id),
            current_order=1
        )

        snapshot.assert_match(repr(result), "test_next_unit.txt")

    @pytest.mark.django_db
    def test_unlock_learning_unit(self, snapshot):
        user_learning_path_id = "12345678-1234-5678-1234-567812345130"
        learning_unit_id = "22345678-1234-5678-1234-567812345131"

        user_learning_path = UserLearningPathFactory(
            user_learning_path_id=user_learning_path_id)
        learning_unit = LearningUnitFactory(learning_unit_id=learning_unit_id)

        user_unit = UserLearningUnitFactory(
            user_learning_path=user_learning_path,
            learning_unit=learning_unit,
            is_locked=True,
            percentage=50,
            status="IN_PROGRESS"
        )

        storage = UserLearningUnitStorage()

        result = storage.unlock_learning_unit(
            user_learning_path_id=user_learning_path_id,
            user_learning_unit_id=user_unit.id)

        snapshot.assert_match(repr(result), "test_unlock_learning_unit.txt")

    @pytest.mark.django_db
    def test_get_learning_units_by_topic_ids(self, snapshot):
        user_id = "12345678-1234-5678-1234-567812345123"
        topic_id_1 = "22345678-1234-5678-1234-567812345131"
        topic_id_2 = "32345678-1234-5678-1234-567812345132"
        user_learning_path_id = "12345678-1234-5678-1234-567812345130"
        learning_unit_id = "22345678-1234-5678-1234-567812345131"
        learning_unit_id1 = "22345678-1234-5678-1234-567812345132"

        user = UserFactory(user_id=user_id)
        course = CourseFactory()
        learning_path = CourseLearningPathFactory(course=course)

        topic1 = TopicFactory(topic_id=topic_id_1)
        topic2 = TopicFactory(topic_id=topic_id_2)

        learning_unit1 = LearningUnitFactory(
            learning_unit_id=learning_unit_id,
            topic=topic1,
            learning_path=learning_path
        )
        learning_unit2 = LearningUnitFactory(
            learning_unit_id=learning_unit_id1,
            topic=topic2,
            learning_path=learning_path
        )

        user_learning_path = UserLearningPathFactory(
            user_learning_path_id=user_learning_path_id,
            user=user,
            learning_path=learning_path
        )

        UserLearningUnitFactory(
            user_learning_path=user_learning_path,
            learning_unit=learning_unit1,
            percentage=20,
            status="IN_PROGRESS"
        )
        UserLearningUnitFactory(
            user_learning_path=user_learning_path,
            learning_unit=learning_unit2,
            percentage=40,
            status="COMPLETED"
        )

        storage = UserLearningUnitStorage()

        result = storage.get_learning_units_by_topic_ids(
            user_id=user_id,
            topic_ids=[topic_id_1, topic_id_2]
        )

        snapshot.assert_match(repr(result),
                              "test_get_learning_units_by_topic_ids.txt")
