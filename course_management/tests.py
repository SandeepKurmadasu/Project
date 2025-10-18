"""
GetTopicsForCourseInteractor - Get all topics/lessons for a course
"""

from typing import List
from dataclasses import dataclass
import abc


# ============================================================================
# DTOs
# ============================================================================

@dataclass
class TopicDTO:
    topic_id: str
    title: str
    description: str
    duration_minutes: int
    content_type: str  # Video, Reading, Interactive, Quiz
    order: int


@dataclass
class ModuleDTO:
    module_id: str
    title: str
    description: str
    topics: List[TopicDTO]
    order: int


@dataclass
class CourseTopicsResponseDTO:
    course_id: str
    total_topics: int
    total_duration_minutes: int
    total_modules: int
    modules: List[ModuleDTO]


# ============================================================================
# STORAGE INTERFACE
# ============================================================================

class TopicStorageInterface(abc.ABC):

    @abc.abstractmethod
    def get_topics_by_course_id(self, course_id: str) -> List[TopicDTO]:
        """Get all topics for a course"""
        pass

    @abc.abstractmethod
    def get_modules_with_topics(self, course_id: str) -> List[ModuleDTO]:
        """Get modules with their topics grouped"""
        pass


# ============================================================================
# EXCEPTIONS
# ============================================================================

class InvalidCourseId(Exception):
    def __init__(self, course_id: str):
        super().__init__()
        self.course_id = course_id

    def __str__(self):
        return f"Invalid course id: {self.course_id}"


class TopicsNotFound(Exception):
    def __init__(self, course_id: str):
        super().__init__()
        self.course_id = course_id

    def __str__(self):
        return f"No topics found for course: {self.course_id}"


# ============================================================================
# MIXIN - Validation
# ============================================================================

class ValidationMixin:

    def validate_course_id(self, course_id: str) -> None:
        if not course_id or course_id.strip() == "":
            raise InvalidCourseId(course_id=course_id)


# ============================================================================
# INTERACTOR - GET TOPICS FOR COURSE
# ============================================================================

class GetTopicsForCourseInteractor(ValidationMixin):

    def __init__(self, topic_storage: TopicStorageInterface):
        self.topic_storage = topic_storage

    def get_topics_for_course(self, course_id: str) -> CourseTopicsResponseDTO:
        """
        Get all topics/lessons for a course with business insights

        Provides:
        - All topics organized by modules
        - Total number of topics
        - Total duration
        - Topic details (title, description, duration, type, order)

        Args:
            course_id: Course ID

        Returns:
            CourseTopicsResponseDTO with all topics and metadata

        Raises:
            InvalidCourseId: If course_id invalid
            TopicsNotFound: If no topics found

        Example:
            response = interactor.get_topics_for_course(course_id="course1")
            # Returns all topics organized by modules
        """

        # Step 1: Validate course_id
        self.validate_course_id(course_id=course_id)

        # Step 2: Get modules with their topics
        modules = self.topic_storage.get_modules_with_topics(course_id=course_id)

        # Step 3: Check if topics found
        if not modules:
            raise TopicsNotFound(course_id=course_id)

        # Step 4: Get all topics (flat list)
        all_topics = self.topic_storage.get_topics_by_course_id(course_id=course_id)

        # Step 5: Calculate total topics
        total_topics = len(all_topics)

        # Step 6: Calculate total duration
        total_duration_minutes = self._calculate_total_duration(topics=all_topics)

        # Step 7: Calculate total modules
        total_modules = len(modules)

        # Step 8: Create response
        response = CourseTopicsResponseDTO(
            course_id=course_id,
            total_topics=total_topics,
            total_duration_minutes=total_duration_minutes,
            total_modules=total_modules,
            modules=modules
        )

        # Step 9: Return
        return response

    def _calculate_total_duration(self, topics: List[TopicDTO]) -> int:
        """
        Calculate total duration of all topics

        Formula: Sum of all topic durations
        """
        total = sum(topic.duration_minutes for topic in topics)
        return total


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

"""
EXAMPLE 1: Get all topics for a course

from courses.interactors.get_topics_interactor import GetTopicsForCourseInteractor
from courses.storage import MySQLTopicStorage

storage = MySQLTopicStorage()
interactor = GetTopicsForCourseInteractor(storage)

response = interactor.get_topics_for_course(course_id="python_basics")

print(f"Course: {response.course_id}")
print(f"Total topics: {response.total_topics}")
print(f"Total duration: {response.total_duration_minutes} minutes")
print(f"Total modules: {response.total_modules}")


EXAMPLE 2: Full response structure

response = interactor.get_topics_for_course("python_basics")

Output:
  {
    course_id: "python_basics",
    total_topics: 20,
    total_duration_minutes: 300,  (5 hours)
    total_modules: 4,
    modules: [
      {
        module_id: "mod_1",
        title: "Python Fundamentals",
        description: "Learn basic Python concepts",
        order: 1,
        topics: [
          {
            topic_id: "topic_1",
            title: "Variables",
            description: "Learn what variables are",
            duration_minutes: 15,
            content_type: "Video",
            order: 1
          },
          {
            topic_id: "topic_2",
            title: "Data Types",
            description: "Learn Python data types",
            duration_minutes: 20,
            content_type: "Video",
            order: 2
          },
          {
            topic_id: "topic_3",
            title: "Operators",
            description: "Learn operators",
            duration_minutes: 15,
            content_type: "Video",
            order: 3
          }
        ]
      },
      {
        module_id: "mod_2",
        title: "Control Flow",
        description: "Conditional statements and loops",
        order: 2,
        topics: [
          {
            topic_id: "topic_4",
            title: "If Statements",
            description: "Learn conditional logic",
            duration_minutes: 20,
            content_type: "Video",
            order: 1
          },
          {
            topic_id: "topic_5",
            title: "Loops",
            description: "Learn for and while loops",
            duration_minutes: 25,
            content_type: "Video",
            order: 2
          }
        ]
      }
    ]
  }


EXAMPLE 3: Error handling

from courses.exceptions import InvalidCourseId, TopicsNotFound

try:
    response = interactor.get_topics_for_course(course_id="course1")
    print(f"Topics: {response.total_topics}")
    print(f"Duration: {response.total_duration_minutes} minutes")

except InvalidCourseId as e:
    print(f"Error: {e}")  # Invalid course id: course1

except TopicsNotFound as e:
    print(f"Error: {e}")  # No topics found for course: course1


EXAMPLE 4: Iterate through topics

response = interactor.get_topics_for_course("python_basics")

for module in response.modules:
    print(f"Module: {module.title}")
    for topic in module.topics:
        print(f"  - {topic.order}. {topic.title} ({topic.duration_minutes} min)")


Output:
  Module: Python Fundamentals
    - 1. Variables (15 min)
    - 2. Data Types (20 min)
    - 3. Operators (15 min)
  Module: Control Flow
    - 1. If Statements (20 min)
    - 2. Loops (25 min)


EXAMPLE 5: Display course progress plan

response = interactor.get_topics_for_course("python_basics")

print(f"Course: {response.course_id}")
print(f"Total modules: {response.total_modules}")
print(f"Total topics: {response.total_topics}")
print(f"Total duration: {response.total_duration_minutes} minutes ({response.total_duration_minutes // 60} hours)")
print()
print("Topics to complete:")

for module in response.modules:
    print(f"  {module.title}")
    for topic in module.topics:
        print(f"    □ {topic.title} - {topic.duration_minutes} min ({topic.content_type})")


Output:
  Course: python_basics
  Total modules: 4
  Total topics: 20
  Total duration: 300 minutes (5 hours)

  Topics to complete:
    Python Fundamentals
      □ Variables - 15 min (Video)
      □ Data Types - 20 min (Video)
      □ Operators - 15 min (Video)
    Control Flow
      □ If Statements - 20 min (Video)
      □ Loops - 25 min (Video)


BUSINESS LOGIC:

1. VALIDATE: Check course_id
2. GET MODULES: Fetch modules with topics
3. CHECK: Verify topics exist
4. GET TOPICS: Fetch all topics (flat list)
5. CALCULATE TOTAL: Count all topics
6. CALCULATE DURATION: Sum all topic durations
7. CALCULATE MODULES: Count modules
8. CREATE RESPONSE: Build response object
9. RETURN: Send to user

RETURNS:

- course_id: Which course
- total_topics: Number of lessons
- total_duration_minutes: Total time in minutes
- total_modules: Number of modules
- modules: Organized modules with topics
"""