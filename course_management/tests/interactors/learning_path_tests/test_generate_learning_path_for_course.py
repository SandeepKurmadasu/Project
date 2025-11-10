from unittest.mock import create_autospec

from course_management.interactors.dtos import (
    LearningPathForCourseDTO,
    LearningUnitDTO,
    TopicTypeEnum,
)
from course_management.interactors.learning_path.generate_learning_path_for_course import (
    GenerateLearningPathForCourseInteractor,
)
from course_management.interactors.storage_interfaces.course_storage_interface import (
    CourseStorageInterface,
)
from course_management.interactors.storage_interfaces.learning_path_storage_interface import (
    LearningPathStorageInterface,
)
from course_management.interactors.storage_interfaces.learning_unit_storage_interface import (
    LearningUnitStorageInterface,
)
from course_management.interactors.storage_interfaces.module_storage_interface import (
    ModuleStorageInterface,
)
from course_management.interactors.storage_interfaces.topic_storage_interface import (
    TopicStorageInterface,
)
from course_management.tests.factories.interactor_factories import (
    CourseDTOFactory,
    ModuleDTOFactory,
    TopicDTOFactory, LearningUnitDTOFactory,
)


class TestGenerateLearningPathForCourseInteractor:
    def setup_method(self):
        self.course_storage = create_autospec(CourseStorageInterface)
        self.module_storage = create_autospec(ModuleStorageInterface)
        self.topic_storage = create_autospec(TopicStorageInterface)
        self.learning_path_storage = create_autospec(LearningPathStorageInterface)
        self.learning_unit_storage = create_autospec(LearningUnitStorageInterface)

        self.interactor = GenerateLearningPathForCourseInteractor(
            course_storage=self.course_storage,
            module_storage=self.module_storage,
            topic_storage=self.topic_storage,
            learning_path_storage=self.learning_path_storage,
            learning_unit_storage=self.learning_unit_storage,
        )

        self.course_id = "course-1"

    def test_generate_new_learning_path_when_none_exists(self, snapshot):
        """Should create a new learning path when no existing one is found."""
        course = CourseDTOFactory(course_id=self.course_id, title="Cyber Security 101", estimated_duration=120)
        modules = [ModuleDTOFactory(module_id="m1")]
        topics = [TopicDTOFactory(topic_id="t1", module_id="m1")]

        self.course_storage.get_courses.return_value = [course]
        self.learning_path_storage.get_latest_learning_path_by_course_id.return_value = None
        self.module_storage.get_course_modules.return_value = modules
        self.topic_storage.get_topics_by_module_ids.return_value = topics

        new_learning_path = LearningPathForCourseDTO(
            learning_path_id="lp1",
            course_id=self.course_id,
            course_title=course.title,
            total_units=0,
            estimated_total_duration_in_minutes=course.estimated_duration,
            learning_units=[],
        )
        self.learning_path_storage.create_course_learning_path.return_value = new_learning_path

        new_units = [
            LearningUnitDTO(
                learning_unit_id="lu1",
                learning_path_id="lp1",
                topic_id="t1",
                unit_title="Intro",
                order=1,
                unit_type=TopicTypeEnum.LEARNING,
                estimated_duration_in_minutes=10,
            )
        ]
        self.learning_unit_storage.create_learning_units.return_value = new_units

        # Act
        result = self.interactor.generate_learning_path_for_course(self.course_id)

        # Assert
        snapshot.assert_match(repr(result), "generate_new_learning_path.json")
        self.learning_path_storage.create_course_learning_path.assert_called_once_with(course_id=self.course_id)
        self.learning_unit_storage.create_learning_units.assert_called_once()

    def test_reuse_existing_learning_path_when_structure_is_same(self, snapshot):
        """Should return existing path when modules/topics match existing units."""
        course = CourseDTOFactory(course_id=self.course_id, title="Network Security", estimated_duration=90)
        existing_path = LearningPathForCourseDTO(
            learning_path_id="lp1",
            course_id=self.course_id,
            course_title=course.title,
            total_units=2,
            estimated_total_duration_in_minutes=course.estimated_duration,
            learning_units=[],
        )
        self.course_storage.get_courses.return_value = [course]
        self.learning_path_storage.get_latest_learning_path_by_course_id.return_value = existing_path

        existing_units = [LearningUnitDTOFactory(topic_id="t1", order=1)]
        self.learning_unit_storage.get_learning_units_by_learning_path_id.return_value = existing_units

        modules = [ModuleDTOFactory(module_id="m1", order=1)]
        topics = [TopicDTOFactory(topic_id="t1", module_id="m1", order=1)]
        self.module_storage.get_course_modules.return_value = modules
        self.topic_storage.get_topics_by_module_ids.return_value = topics

        # Act
        result = self.interactor.generate_learning_path_for_course(self.course_id)

        # Assert
        snapshot.assert_match(repr(result), "reuse_existing_learning_path.json")
        self.learning_path_storage.create_course_learning_path.assert_not_called()
        self.learning_unit_storage.create_learning_units.assert_not_called()

    def test_create_new_path_when_topics_changed(self, snapshot):
        """Should create a new learning path when topics differ."""
        course = CourseDTOFactory(course_id=self.course_id, title="Data Security", estimated_duration=100)
        old_path = LearningPathForCourseDTO(
            learning_path_id="lp_old",
            course_id=self.course_id,
            course_title=course.title,
            total_units=1,
            estimated_total_duration_in_minutes=course.estimated_duration,
            learning_units=[],
        )
        self.course_storage.get_courses.return_value = [course]
        self.learning_path_storage.get_latest_learning_path_by_course_id.return_value = old_path

        existing_units = [LearningUnitDTOFactory(topic_id="t1", order=1)]
        self.learning_unit_storage.get_learning_units_by_learning_path_id.return_value = existing_units

        modules = [ModuleDTOFactory(module_id="m1", order=1)]
        new_topics = [TopicDTOFactory(topic_id="t2", module_id="m1", order=1)]
        self.module_storage.get_course_modules.return_value = modules
        self.topic_storage.get_topics_by_module_ids.return_value = new_topics

        new_path = LearningPathForCourseDTO(
            learning_path_id="lp_new",
            course_id=self.course_id,
            course_title=course.title,
            total_units=0,
            estimated_total_duration_in_minutes=course.estimated_duration,
            learning_units=[],
        )
        self.learning_path_storage.create_course_learning_path.return_value = new_path

        new_units = [
            LearningUnitDTO(
                learning_unit_id="lu1",
                learning_path_id="lp_new",
                topic_id="t2",
                unit_title="New Topic",
                order=1,
                unit_type=TopicTypeEnum.LEARNING,
                estimated_duration_in_minutes=10,
            )
        ]
        self.learning_unit_storage.create_learning_units.return_value = new_units

        # Act
        result = self.interactor.generate_learning_path_for_course(self.course_id)

        # Assert
        snapshot.assert_match(repr(result), "create_new_path_when_topics_changed.json")
        self.learning_path_storage.create_course_learning_path.assert_called_once_with(course_id=self.course_id)
        self.learning_unit_storage.create_learning_units.assert_called_once()

    def test_modules_and_topics_sorted_by_order(self, snapshot):
        """Should correctly sort modules and topics by their order."""
        modules = [
            ModuleDTOFactory(module_id="m2", order=2),
            ModuleDTOFactory(module_id="m1", order=1),
        ]
        topics = [
            TopicDTOFactory(topic_id="t2", module_id="m1", order=2, title="Second"),
            TopicDTOFactory(topic_id="t1", module_id="m1", order=1, title="First"),
        ]
        self.module_storage.get_course_modules.return_value = modules
        self.topic_storage.get_topics_by_module_ids.return_value = topics

        ordered_modules = self.interactor._get_ordered_modules(self.course_id)
        ordered_module_ids = [m.module_id for m in ordered_modules]

        topics_by_module = self.interactor._get_ordered_topics_by_module(ordered_modules)
        ordered_topic_ids = [t.topic_id for t in topics_by_module["m1"]]

        snapshot.assert_match(repr(ordered_module_ids), "ordered_modules.json")
        snapshot.assert_match(repr(ordered_topic_ids), "ordered_topics.json")
