class NotInDBCourseIdsFound(Exception):
    def __init__(self, course_ids: list[str]):
        self.course_ids = course_ids


class DuplicateCourseIdsFound(Exception):
    def __init__(self, course_ids: list[str]):
        self.course_ids = course_ids


class UserNotFound(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id


class CourseNotFound(Exception):
    def __init__(self, course_id: str):
        self.course_id = course_id


class DBNotFoundedModuleIds(Exception):
    def __init__(self, module_ids: list[str]):
        self.module_ids = module_ids


class DuplicateCourseTitleFound(Exception):
    def __init__(self, course_ids: list[str]):
        self.course_ids = course_ids


class DuplicateTitlesFound(Exception):
    def __init__(self, titles: list[str]):
        self.titles = titles


class UnexpectedLevelTypeFound(Exception):
    def __init__(self, level_types: list[str]):
        self.level_types = level_types


class UserNotEnrolledCourse(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__(user_id)


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


class NotExistedEmailFound(Exception):
    def __init__(self, email: str):
        self.email=email


class WrongPasswordFound(Exception):
    def __init__(self, password: str):
        self.password=password

class ExistedPhoneNumberFound(Exception):
    def __init__(self, phone_number: str):
        self.phone_number = phone_number


class UsernameNotFound(Exception):
    def __init__(self, username: str):
        self.username = username


class CourseInProgressException(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id


class UserNotEnrolledInModule(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id


class UserLearningPathNotFound(Exception):
    def __init__(self, user_learning_path_id: str):
        self.user_learning_path_id = user_learning_path_id
        super().__init__(
            f"User learning path not found for ID: {user_learning_path_id}")

    def __repr__(self):
        return f"UserLearningPathNotFound(user_learning_path_id={self.user_learning_path_id!r})"


class LearningUnitIdNotFound(Exception):
    def __init__(self, learning_unit_id: str):
        self.learning_unit_id = learning_unit_id


class LearningUnitLockedException(Exception):
    def __init__(self, learning_unit_id: str):
        self.learning_unit_id = learning_unit_id


class UserLearningUnitLockedException(Exception):
    def __init__(self, user_learning_unit_id: int):
        self.user_learning_unit_id = user_learning_unit_id


class LearningPathNotFound(Exception):
    def __init__(self, course_id: str):
        self.course_id = course_id


class LearningPathIdNotFound(Exception):
    def __init__(self, learning_path_id: str):
        self.learning_path_id = learning_path_id


class UserLearningUnitNotFound(Exception):
    def __init__(self, user_learning_unit_id: int):
        self.user_learning_unit_id = user_learning_unit_id


class AlreadyExistedTitlesFound(Exception):
    def __init__(self, module_ids: list[str]):
        self.module_ids = module_ids


class UserLearningPathIdNotFound(Exception):
    def __init__(self, user_learning_path_id: int):
        self.user_learning_path_id = user_learning_path_id

class TopicAssessmentTypeFound(Exception):
    def __init__(self,topic_id: str):
        self.topic_id = topic_id