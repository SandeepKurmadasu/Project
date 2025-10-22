from dataclasses import dataclass
from typing import List

@dataclass
class CreateUserDTO:
    name : str
    username : str
    password : str
    email : str
    phone_number : int

@dataclass
class UpdateUserDTO:
    user_id: str
    name: str
    username: str
    password: str
    email: str
    phone_number: int


@dataclass
class UserDTO:
    user_id : str
    name: str
    username: str
    password: str
    email: str
    phone_number: int
    is_active : bool
    otp_count : int



@dataclass
class CreateUserEnrollmentDTO:
    user_id : str
    course_id : str


@dataclass
class CreateCourseDTO:
    title: str
    description : str
    category: str
    level: str


@dataclass
class UpdateCourseDTO:
    course_id : str
    title: str
    description: str
    category: str
    level: str


@dataclass
class CourseDTO:
    course_id : str
    title: str
    description: str
    category: str
    level: str
    average_rating : int
    estimated_duration : int


@dataclass
class CreateTopicDTO:
    title : str
    description : str
    topic_type : str
    content : str
    estimate_duration : int


@dataclass
class TopicDTO:
    topic_id : str
    module_id : str
    title :str
    description : str
    topic_type : str
    content: str
    estimated_duration : int


@dataclass
class CreateModuleDTO:
    module_title: str
    description : str


@dataclass
class UpdateModuleDTO:
    module_id: str
    course_id: str
    module_title: str
    description: str


@dataclass
class ModuleDTO:
    module_id : str
    course_id: str
    module_title : str
    description: str
    estimated_duration : int



@dataclass
class GetCourseModulesDTO:
    course_id :str
    modules : List[ModuleDTO]



@dataclass
class CourseLearningPathDTO:
    course_id : str
    modules : List[ModuleDTO]
    estimated_duration : int


@dataclass
class UserLearningPathDTO:
    user_id : str
    course_id : str
    modules : List[ModuleDTO]
    percentage : int



@dataclass
class UserLearningPathPercentageDTO:
    user_id :str
    course_id : str
    percentage : int


@dataclass
class UserCurrentTopicLearningStatusDTO:
    user_id : str
    course_id : str
    current_topic : TopicDTO
    status : str
    percentage_of_completion : int


@dataclass
class UserModuleCompletionPercentageDTO:
    course_id :str
    module_id : str
    percentage : str

@dataclass
class EnrollmentDTO:
    id : int
    user_id : str
    course_id : str
    course_percentage : int


@dataclass
class UserTopicCompletionPercentageDTO:
    user_id : str
    topic_id : str
    status : str
    percentage : int