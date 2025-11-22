from course_management.exceptions.custom_exceptions import CourseNotFound
from course_management.interactors.course.get_topics_for_course import \
    GetTopicsForCourseInteractor
from course_management.storages.course_storage import CourseStorage
from course_management.storages.module_storage import ModuleStorage
from course_management.storages.topic_storage import TopicStorage
from course_management.view_graphql.types.error_types import CourseNotFoundType
from course_management.view_graphql.types.types import TopicGQLType, \
    TopicsListType


def get_topics_for_course_resolver(root, info, params):
    course_id = params.course_id

    course_storage = CourseStorage()
    module_storage = ModuleStorage()
    topic_storage = TopicStorage()

    interactor = GetTopicsForCourseInteractor(course_storage=course_storage,
                                              module_storage=module_storage,
                                              topic_storage=topic_storage)

    try:
        response_data = interactor.get_topics_for_course(course_id=course_id)

        result = [TopicGQLType(
            topic_id=t.topic_id,
            module_id=t.module_id,
            topic_title=t.title,
            description=t.description,
            topic_type=t.topic_type,
            content=t.content,
            order=t.order,
            estimated_duration_in_mins=t.estimate_duration_in_mins
        ) for t in response_data]

        return TopicsListType(topics=result)

    except CourseNotFound as e:
        return CourseNotFoundType(course_id=course_id)
