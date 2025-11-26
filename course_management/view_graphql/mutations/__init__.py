import graphene

from course_management.view_graphql.mutations.Course.create_courses import CreateCourses
from course_management.view_graphql.mutations.Course.update_courses import UpdateCourses
from course_management.view_graphql.mutations.Module.add_modules_for_course import AddModulesToCourse
from course_management.view_graphql.mutations.Module.create_module_mutation import CreateModule
from course_management.view_graphql.mutations.Module.update_modules_mutation import UpdateModule
from course_management.view_graphql.mutations.Topic.create_topics import CreateTopics
from course_management.view_graphql.mutations.Topic.update_topic_mutation import UpdateTopicsMutation
from course_management.view_graphql.mutations.enrollment_mutations.enroll_user_for_course_mutation import \
    EnrollUserForCourse
from course_management.view_graphql.mutations.feedback_mutations.create_course_feedback_mutation import \
    FeedbackForCourseMutation
from course_management.view_graphql.mutations.learning_path.generate_learning_path_mutation import \
    GenerateCourseLearningPathMutation
from course_management.view_graphql.mutations.learning_path.start_user_learning_path_mutation import \
    StartUserLearningPathMutation
from course_management.view_graphql.mutations.learning_path.update_learning_unit_progress_status_mutation import \
    UpdateLearningUnitProgressMutation
from course_management.view_graphql.mutations.user.block_user_mutation import BlockUser
from course_management.view_graphql.mutations.user.create_user import CreateUser
from course_management.view_graphql.mutations.user.login_user_mutation import LoginUser
from course_management.view_graphql.mutations.user.update_user_mutation import UpdateUser
from course_management.view_graphql.mutations.user.user_reset_otp_mutation import UserResetOTPCount


class CreateCourse(graphene.ObjectType):
    create_course = CreateCourses.Field(required=True)


class UpdateCourse(graphene.ObjectType):
    update_course = UpdateCourses.Field(required=True)


class CreateUsers(graphene.ObjectType):
    create_user = CreateUser.Field(required=True)


class CreateTopic(graphene.ObjectType):
    create_topics = CreateTopics.Field(required=True)



class CreateModules(graphene.ObjectType):
    create_modules = CreateModule.Field(required=True)


class UpdateModules(graphene.ObjectType):
    update_modules = UpdateModule.Field(required=True)


class AddModuleToCourse(graphene.ObjectType):
    add_modules = AddModulesToCourse.Field(required=True)


class UserUpdate(graphene.ObjectType):
    update_user = UpdateUser.Field(required=True)


class UserBlock(graphene.ObjectType):
    block_user = BlockUser.Field(required=True)


class UserOtpCountReset(graphene.ObjectType):
    user_reset_otp_count = UserResetOTPCount.Field(required=True)


class UpdateTopics(graphene.ObjectType):
    update_topics = UpdateTopicsMutation.Field(required=True)


class GenerateLearningPath(graphene.ObjectType):
    generate_learning_path = GenerateCourseLearningPathMutation.Field(
        required=True)

class StartUserLearningPath(graphene.ObjectType):
    user_learning_path = StartUserLearningPathMutation.Field(required=True)


class UpdateLearningUnitProgress(graphene.ObjectType):
    update_learning_unit_progress = UpdateLearningUnitProgressMutation.Field(required=True)


class CreateEnrollUserForCourse(graphene.ObjectType):
    enroll_user_for_course = EnrollUserForCourse.Field(required=True)

class CourseFeedback(graphene.ObjectType):
    feedback_for_course = FeedbackForCourseMutation.Field(required=True)

class UserLogin(graphene.ObjectType):
    login_user = LoginUser.Field(required=True)
