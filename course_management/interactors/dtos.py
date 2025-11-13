from dataclasses import dataclass
from enum import Enum


class CourseCategoryEnum(Enum):
    DEVELOPMENT = "DEVELOPMENT"
    DESIGN = "DESIGN"
    MARKETING = "MARKETING"
    BUSINESS = "BUSINESS"


class LevelEnum(Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"


class EnrollmentStatusEnum(Enum):
    IN_PROGRESS = "IN_PROGRESS"
    PASS = "PASS"
    FAIL = "FAIL"


class AttemptedTopicStatusEnum(Enum):
    START = "START"
    HALF_COMPLETED = "HALF_COMPLETED"
    COMPLETE = "COMPLETE"


class StatusEnum(Enum):
    START = "START"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"


class GenderEnum(Enum):
    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"
    OTHERS = "OTHERS", "Others"


@dataclass
class CreateUserDTO:
    name: str
    username: str
    password: str
    gender: GenderEnum
    email: str
    phone_number: int


@dataclass
class UpdateUserDTO:
    user_id: str
    name: str
    gender: GenderEnum
    username: str
    password: str
    email: str
    phone_number: int


@dataclass
class UserDTO:
    user_id: str
    name: str
    gender: GenderEnum
    username: str
    password: str
    email: str
    phone_number: int
    is_active: bool
    otp_count: int


@dataclass
class CreateCourseDTO:
    title: str
    description: str
    category: CourseCategoryEnum  # Enum like Programming,Design
    level: LevelEnum  # Enum like Beginner / Intermediate / Advanced


@dataclass
class UpdateCourseDTO:
    course_id: str
    title: str
    description: str
    category: CourseCategoryEnum
    level: LevelEnum


@dataclass
class CourseDTO:
    course_id: str
    title: str
    description: str
    category: CourseCategoryEnum  # Enum like Programming,Design
    level: LevelEnum  # Enum like Beginner / Intermediate / Advanced
    average_rating: float
    estimated_duration: int


class TopicTypeEnum(Enum):
    LEARNING = "LEARNING"
    ASSESSMENT = "ASSESSMENT"


@dataclass
class CreateTopicDTO:
    title: str
    description: str
    topic_type: TopicTypeEnum  #
    content: str
    estimate_duration: int


@dataclass
class TopicDTO:
    topic_id: str
    module_id: str
    title: str
    description: str
    topic_type: TopicTypeEnum  # enum like learning/assessment
    content: str
    order: int
    estimated_duration: int


@dataclass
class UserTopicCompletionPercentageDTO:
    user_id: str
    topic_id: str
    percentage: int


@dataclass
class CreateModuleDTO:
    module_title: str
    description: str


@dataclass
class UpdateModuleDTO:
    module_id: str
    course_id: str
    module_title: str
    description: str


@dataclass
class ModuleDTO:
    module_id: str
    course_id: str
    module_title: str
    description: str
    order: int
    estimated_duration: int


@dataclass
class UserCourseCompletionPercentageDTO:
    user_id: str
    course_id: str
    percentage: int


@dataclass
class UserModuleCompletionPercentageDTO:
    user_id: str
    module_id: str
    percentage: int


@dataclass
class EnrollmentDTO:
    id: int
    user_id: str
    course_id: str
    course_status: EnrollmentStatusEnum
    course_percentage: int
    user_learning_path_id: str



@dataclass
class LearningUnitDTO:
    learning_unit_id: str
    learning_path_id: str
    unit_type: TopicTypeEnum
    topic_id: str
    unit_title: str
    order: int
    estimated_duration_in_minutes: int


@dataclass
class CreateLearningUnitDTO:
    learning_path_id: str
    unit_type: TopicTypeEnum
    topic_id: str
    unit_title: str
    order: int
    estimated_duration_in_minutes: int


@dataclass
class LearningPathForCourseDTO:
    learning_path_id: str
    course_id: str
    course_title: str
    total_units: int
    estimated_total_duration_in_minutes: int
    learning_units: list[LearningUnitDTO]

    def __repr__(self):
        return (
            f"LearningPathForCourseDTO("
            f"learning_path_id='{self.learning_path_id}', "
            f"course_id='{self.course_id}', "
            f"course_title='{self.course_title}', "
            f"total_units={self.total_units}, "
            f"estimated_total_duration_minutes={self.estimated_total_duration_in_minutes}, "
        )


@dataclass
class CreateCourseLearningPathDTO:
    course_id: str
    course_title: str
    total_units: int
    estimated_total_duration_in_minutes: int


@dataclass
class UserLearningPathPercentageDTO:
    user_id: str
    learning_path_id: str
    percentage: int


@dataclass
class UserLearningPathDTO:
    user_learning_path_id: str
    user_id: str
    learning_path_id: str
    current_learning_unit_id: str
    overall_percentage: int
    status: StatusEnum


@dataclass
class LearningUnitProgressDTO:
    user_learning_path_id: str
    learning_unit_id: str
    status: AttemptedTopicStatusEnum
    percentage: int


@dataclass
class UpdateLearningUnitProgressDTO:
    user_learning_path_id: str
    learning_unit_id: str
    status: AttemptedTopicStatusEnum
    percentage: int


@dataclass
class UpdateLearningUnitProgressResponseDTO:
    user_learning_path_id: str
    learning_unit_id: str
    updated_status: AttemptedTopicStatusEnum
    updated_percentage: int
    next_unit_unlocked: bool
    next_unit_id: str
    overall_path_percentage: int


@dataclass
class UserLearningUnitProgressDTO:
    learning_unit_id: str
    user_learning_path_id: str
    status: AttemptedTopicStatusEnum
    percentage: int
    is_locked: bool
    order: int
    estimated_duration_in_minutes: int


@dataclass
class CourseFeedbackDTO:
    course_id: str
    user_id: str
    rating: int
    message: str
