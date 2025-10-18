from dataclasses import dataclass
from typing import List

@dataclass
class CourseDTO:
    course_id : str
    name : str
    description : str
    category: str

@dataclass
class UserDTO:
    user_id: str
    name: str
    field: str


@dataclass
class CreateCourseRequestDTO:
    name : str
    description : str

@dataclass
class UpdateCourseRequestDTO:
    course_id : str
    name : str
    description : str

@dataclass
class CourseRecommendationDTO:
    course_id : str
    name : str
    category: str

@dataclass
class CourseProgressDTO:
    course_id: str
    user_id: str
    total_topics: str
    completed_topics: str
    completion_percentage: float

@dataclass
class TopicProgressDTO:
    topic_id: str
    topic_name: str
    status: str
    progress_percentage: float

@dataclass
class CourseCompletionResponseDTO:
    course_id: str
    user_id: str
    completion_percentage: float
    total_topics: int
    completed_topics: int
    status: str  # not_started, in_progress, nearly_done, completed
    topics_progress: List[TopicProgressDTO]
    next_topic: str  # Name of next topic to complete
    estimated_hours_remaining: float
