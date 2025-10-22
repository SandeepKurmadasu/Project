from course_management.exceptions.custom_exceptions import NotInDBCourseIdsFound, UserNotFound, CourseNotFound, DBNotFoundedModuleIds, DuplicateCourseTitleFound, UnexpectedLevelTypeFound, \
    DuplicateTitlesFound, DuplicateCourseIdsFound
from course_management.interactors.storage_interface.course_storage_interface import CourseStorageInterface
from course_management.interactors.storage_interface.user_storage_interface import UserStorageInterface




class ValidationMixIns:

    @staticmethod
    def check_if_db_exists_course_ids(course_ids: list[str], course_storage: CourseStorageInterface):
        existing_course_ids = course_storage.get_valid_course_ids(course_ids)

        invalid_course_ids = [
            course_id
            for course_id in course_ids
            if course_id not in existing_course_ids
        ]

        if invalid_course_ids:
            raise NotInDBCourseIdsFound(course_ids=invalid_course_ids)

    @staticmethod
    def check_if_user_exists(user_id: str, user_storage: UserStorageInterface):
        is_user_found = user_storage.check_user_exists(user_id=user_id)

        if not is_user_found:
            raise UserNotFound(user_id=user_id)

    @staticmethod
    def check_if_course_exists(course_id: str, course_storage: CourseStorageInterface):
        is_course_found = course_storage.check_course_exists(course_id=course_id)

        if not is_course_found:
            raise CourseNotFound(course_id=course_id)

    @staticmethod
    def check_modules_in_db(module_ids: list[str], module_storage):

        existing_module_ids = module_storage.get_db_existing_module_ids(module_ids=module_ids)

        not_existing_module_ids = [
            module_id
            for module_id in module_ids
            if module_id not in existing_module_ids
        ]

        if not_existing_module_ids:
            raise DBNotFoundedModuleIds(not_existing_module_ids)

    @staticmethod
    def check_duplicate_course_titles(courses, course_storage: CourseStorageInterface):
        titles = [obj.title for obj in courses]
        duplicate_titles = [
            title for title in titles if titles.count(title) > 1
        ]
        if duplicate_titles:
            raise DuplicateTitlesFound(titles=list(set(duplicate_titles)))

    @staticmethod
    def check_if_titles_are_exists(courses,course_storage: CourseStorageInterface):
        titles = [obj.title for obj in courses]

        existing_course_ids = course_storage.get_title_course_ids(titles=titles)
        if existing_course_ids:
            raise DuplicateCourseTitleFound(course_ids=existing_course_ids)

    @staticmethod
    def check_invalid_level_type(courses):
        level_enum_types = [each_level.value for each_level in LevelEnum]
        not_enum_existed_type = [obj.level for obj in courses if obj.level not in level_enum_types]

        if not_enum_existed_type:
            raise UnexpectedLevelTypeFound(level_types=not_enum_existed_type)

    @staticmethod
    def check_duplicate_course_ids(course_ids: list[str]):
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
