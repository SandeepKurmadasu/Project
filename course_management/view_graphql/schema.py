import graphene

from course_management.view_graphql.mutations import CreateCourse, UpdateCourse, \
    CreateUsers, CreateTopic, CreateModules, UpdateModules, AddModuleToCourse, UserUpdate, UserBlock, UserOtpCountReset, \
    UpdateTopics, GenerateLearningPath, StartUserLearningPath, UpdateLearningUnitProgress, CreateEnrollUserForCourse, \
    CourseFeedback
from course_management.view_graphql.mutations.Course.create_courses import CreateCourses
from course_management.view_graphql.queries import GetCourses, GetTopics, GetUserLearningPathPercentage, \
    GetUserRecommendedCourses, GetModulesForCourses, GetTopicCompletionPercentage, GetUserCurrentLearningUnitSatus, \
    GetUserCourseCompletionPercentage, GetModuleCompletionPercentage, GetTopicsForCourse, GetUserEnrollments, \
    GetUserProfile, GetUserLearningPath

QUERY_CLASSES = [GetCourses, GetTopics, GetUserLearningPath, GetModulesForCourses, GetUserProfile,
                 GetUserLearningPathPercentage, GetUserRecommendedCourses,
                 GetUserCurrentLearningUnitSatus, GetTopicCompletionPercentage,
                 GetUserCourseCompletionPercentage, GetUserEnrollments,
                 GetModuleCompletionPercentage, GetTopicsForCourse]

MUTATION_CLASSES = {CreateCourse,UpdateCourse, CreateUsers, CreateTopic, CreateCourses, CreateModules, UpdateModules,
                    AddModuleToCourse, UserUpdate, UserBlock,
                    UserOtpCountReset, UpdateTopics, GenerateLearningPath,
                    StartUserLearningPath, UpdateLearningUnitProgress,
                    CreateEnrollUserForCourse, CourseFeedback}

class Query(*QUERY_CLASSES):
    pass


class Mutation(*MUTATION_CLASSES):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
