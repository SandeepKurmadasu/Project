import pytest
import json
from graphene.test import Client

from course_management.models import Course
from hive_edu_verse.schema import schema


@pytest.mark.django_db
def test_get_courses_api(snapshot):
    course_id = "86fa7025-0e26-42cd-842b-5f74cc459755"
    Course.objects.create(
        course_id=course_id,
        title="Test Course",
        description="Course description",
        category="Test Category",
        level="Beginner",
        average_rating=4.5,
        estimated_duration_in_min=120,
    )
    client = Client(schema)

    query = '''
    query GetCourses($params: GetCoursesParams!) {
      getCourses(params: $params) {
        ... on CoursesType {
          __typename
          courses {
            averageRating
            category
            courseId
            description
            estimatedDuration
            level
            title
          }
        }
        ... on DuplicateCourseIdsInRequest {
          __typename
          courseIds
        }
        ... on CourseIdsNotFound {
          __typename
          courseIds
        }
      }
    }
    '''

    variables = {
        "params": {
            "courseIds": ["86fa7025-0e26-42cd-842b-5f74cc459755"]
        }
    }

    result = client.execute(query, variables=variables)
    json_result = json.dumps(result, indent=2)

    snapshot.assert_match(json_result, "test_get_courses_api.txt")
