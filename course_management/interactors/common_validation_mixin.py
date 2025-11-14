""" Provides common validation methods used across different interactors. """
from course_management.exceptions.custom_exceptions import \
    (NotInDBCourseIdsFound, UserNotFound, CourseNotFound,
     DBNotFoundedModuleIds,
     DuplicateCourseTitleFound, UnexpectedLevelTypeFound, DuplicateTitlesFound,
     UserLearningPathNotFound, DuplicateCourseIdsFound)
from course_management.interactors.dtos import LevelEnum
from course_management.interactors.storage_interfaces.course_storage_interface import \
    CourseStorageInterface
from course_management.interactors.storage_interfaces.user_learning_path import \
    UserLearningPathStorageInterface
from course_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface


class ValidationMixIn:
    """ Validate the common validation the Course management validations mixins"""

    @staticmethod
    def check_course_ids_exist_in_db(course_ids: list[str],
                                     course_storage: CourseStorageInterface):
        """Check the course ids in database"""

        existing_course_ids = course_storage.get_valid_course_ids(course_ids)

        invalid_course_ids = [
            course_id
            for course_id in course_ids
            if course_id not in existing_course_ids
        ]

        if invalid_course_ids:
            raise NotInDBCourseIdsFound(course_ids=invalid_course_ids)

    @staticmethod
    def check_user_exists(user_id: str, user_storage: UserStorageInterface):
        """Check the user exists or not"""

        is_user_found = user_storage.check_user_exists(user_id=user_id)

        if not is_user_found:
            raise UserNotFound(user_id=user_id)

    @staticmethod
    def check_course_exists(course_id: str,
                            course_storage: CourseStorageInterface):
        """ Check the course exists or not """

        is_course_found = course_storage.check_course_exists(
            course_id=course_id)

        if not is_course_found:
            raise CourseNotFound(course_id=course_id)

    @staticmethod
    def check_modules_exist_in_db(module_ids: list[str], module_storage):
        """Check modules in database or not"""

        existing_module_ids = module_storage.get_db_existing_module_ids(
            module_ids=module_ids)

        not_existing_module_ids = [
            module_id
            for module_id in module_ids
            if module_id not in existing_module_ids
        ]

        if not_existing_module_ids:
            raise DBNotFoundedModuleIds(not_existing_module_ids)

    @staticmethod
    def check_duplicate_course_titles(course_titles: list[str]):
        """Check the duplicate course titles """

        duplicate_titles = [title for title in course_titles if
                            course_titles.count(title) > 1]

        if duplicate_titles:
            raise DuplicateTitlesFound(titles=list(set(duplicate_titles)))

    @staticmethod
    def check_existing_titles(courses, course_storage: CourseStorageInterface):
        """ Validate the course titles like already existed or not """
        titles = [obj.title for obj in courses]

        title_existing_course_ids = course_storage.get_course_ids_by_title(
            titles=titles)
        if title_existing_course_ids:
            raise DuplicateCourseTitleFound(
                course_ids=title_existing_course_ids)

    @staticmethod
    def check_invalid_level_type(course_level_types: list[str]):
        """ Validate the course level type """

        level_enum_types = [each_level.value for each_level in LevelEnum]

        not_enum_existed_type = [each_type for each_type in course_level_types if
                                 each_type not in level_enum_types]

        if not_enum_existed_type:
            raise UnexpectedLevelTypeFound(level_types=not_enum_existed_type)

    @staticmethod
    def validate_user_learning_path_exists(user_learning_path_id: str,
                                           user_learning_path_storage: UserLearningPathStorageInterface):
        """ Validate the user learning path exist or not """

        exists = user_learning_path_storage.check_user_learning_path_exists(
            user_learning_path_id=user_learning_path_id)
        if not exists:
            raise UserLearningPathNotFound(
                user_learning_path_id=user_learning_path_id)

    @staticmethod
    def check_duplicate_course_ids(course_ids: list[str]):
        """ Check the duplicate course ids """

        unique_course_ids = []
        duplicate_course_ids = []

        for each_course_id in course_ids:
            is_unique_course_id = each_course_id in unique_course_ids
            if is_unique_course_id:
                duplicate_course_ids.append(each_course_id)
            else:
                unique_course_ids.append(each_course_id)

        if duplicate_course_ids:
            raise DuplicateCourseIdsFound(course_ids=duplicate_course_ids)
