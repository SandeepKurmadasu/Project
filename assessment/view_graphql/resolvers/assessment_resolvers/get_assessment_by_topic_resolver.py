from assessment.interactors.assessment_interactor.get_assessment_for_topic import \
    GetAssessmentByTopicInteractor
from assessment.storages.assessment_storage import AssessmentStorage
from assessment.view_graphql.types.types import AssessmentType
from course_management.exceptions.custom_exceptions import NotExistedTopicFound
from course_management.storages.topic_storage import TopicStorage
from course_management.view_graphql.types.error_types import TopicNotFound


def get_assessment_by_topic_resolver(root,info,params):

    topic_id = params.topic_id

    topic_storage = TopicStorage()
    assessment_storage = AssessmentStorage()

    interactor = GetAssessmentByTopicInteractor(topic_storage=topic_storage,assessment_storage=assessment_storage)

    try:

        result = interactor.get_assessment_by_topic(topic_id=topic_id)

        return AssessmentType(
                        assessmentId=result.assessment_id,
                        assessmentTitle=result.assessment_title,
                        assessmentType=result.assessment_type,
                        topic_id=result.topic_id,
                        description=result.description,
                        passMarks=result.pass_marks,
                        icon=result.icon,
                        noOfQuestions=result.no_of_questions,
                        marks=result.marks,
                        passPercentage=result.pass_percentage,
                        easyCount=result.easy_count,
                        mediumCount=result.medium_count,
                        hardCount=result.hard_count,
                        attemptsLimit=result.attempts_limit,
                        estimateDurationInMins=result.estimate_duration_in_mins,
                    )
    except NotExistedTopicFound as e:
        return TopicNotFound(topic_id=e.topic_id)