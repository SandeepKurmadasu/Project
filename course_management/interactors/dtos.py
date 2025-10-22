from typing import List

class CreateUserDTO:
    name : str
    username : str
    password : str
    email : str
    phone_number : int

class UpdateUserDTO:
    user_id: str
    name: str
    username: str
    password: str
    email: str
    phone_number: int

class UserDTO:
    user_id : str
    name: str
    username: str
    password: str
    email: str
    phone_number: int
    is_active : bool
    otp_count : int



class CreateUserEnrollmentDTO:
    user_id : str
    course_id : str

class CreateCourseDTO:
    title: str
    description : str
    category: str
    level: str

class UpdateCourseDTO:
    course_id : str
    title: str
    description: str
    category: str
    level: str

class CourseDTO:
    course_id : str
    title: str
    description: str
    category: str
    level: str
    average_rating : int
    estimated_duration : int

class CreateTopicDTO:
    title : str
    description : str
    topic_type : str
    content : str
    estimate_duration : int

class TopicDTO:
    topic_id : str
    module_id : str
    title :str
    description : str
    topic_type : str
    content: str
    estimated_duration : int

class CreateModuleDTO:
    module_title: str
    description : str

class UpdateModuleDTO:
    module_id: str
    course_id: str
    module_title: str
    description: str

class ModuleDTO:
    module_id : str
    course_id: str
    module_title : str
    description: str
    estimated_duration : int


class GetCourseModulesDTO:
    course_id :str
    modules : List[ModuleDTO]


class CourseLearningPathDTO:
    course_id : str
    modules : List[ModuleDTO]
    estimated_duration : int

class UserLearningPathDTO:
    user_id : str
    course_id : str
    modules : List[ModuleDTO]
    percentage : int


class UserLearningPathPercentageDTO:
    user_id :str
    course_id : str
    percentage : int


class UserCurrentTopicLearningStatusDTO:
    user_id : str
    course_id : str
    current_topic : TopicDTO
    status : str
    percentage_of_completion : int

class UserModuleCompletionPercentageDTO:
    course_id :str
    module_id : str
    percentage : str

class EnrollmentDTO:
    id : int
    user_id : str
    course_id : str
    course_percentage : int

class UserTopicCompletionPercentageDTO:
    user_id : str
    topic_id : str
    status : str
    percentage : int




