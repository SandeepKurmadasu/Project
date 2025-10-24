class UserNotFound(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id

class UserNotEnrolledCourse(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id

class CourseNotFound(Exception):
    def __init__(self, course_id: str):
        self.course_id = course_id

class NotInDBCourseIdsFound(Exception):
    def __init__(self, course_ids: list[str]):
        self.course_ids = course_ids

class DBExistingCourseIdsFound(Exception):
    def __init__(self, course_ids: list[str]):
        self.course_ids = course_ids

class DuplicateCourseIdsFound(Exception):
    def __init__(self, course_ids: list[str]):
        self.course_ids = course_ids

class EmptyTitleCourseIdsFound(Exception):
    def __init__(self, course_ids: list[str]):
        self.course_ids = course_ids

class DuplicateCourseTitleFound(Exception):
    def __init__(self, course_ids: list[str]):
        self.course_ids = course_ids

class DuplicateTitlesFound(Exception):
    def __init__(self, titles: list[str]):
        self.titles = titles

class DBNotFoundedModuleIds(Exception):
    def __init__(self, module_ids: list[str]):
        self.module_ids = module_ids

class UnexpectedLevelTypeFound(Exception):
    def __init__(self, level_types: list[str]):
        self.level_types = level_types

class NotExistingTopicTypesFound(Exception):
    def __init__(self, topic_types: list[str]):
        self.topic_types = topic_types

class NotExistingTopicIdsFound(Exception):
    def __init__(self, topic_ids: list[str]):
        self.topic_ids = topic_ids

class NotExistedTopicFound(Exception):
    def __init__(self, topic_id: str):
        self.topic_id = topic_id

class ExistedUsernameFound(Exception):
    def __init__(self, username: str):
        self.username = username

class ExistedEmailFound(Exception):
    def __init__(self, email: str):
        self.email = email

class ExistedPhoneNumberFound(Exception):
    def __init__(self, phone_number: int):
        self.phone_number = phone_number

class UsernameNotFound(Exception):
    def __init__(self, username: str):
        self.username = username

class InvalidUserIdError(Exception):
    def __init__(self, message: str):
        self.message = message