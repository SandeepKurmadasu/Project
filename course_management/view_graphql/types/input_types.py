
import graphene


# Input
class CreateCourseInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    category = graphene.String(required=True)
    level = graphene.String(required=True)



class CreateCoursesInput(graphene.InputObjectType):
    courses=graphene.List(CreateCourseInput, required=True)



class GetCoursesParams(graphene.InputObjectType):
    course_ids = graphene.List(graphene.String, required=True)


class UpdateCourseInput(graphene.InputObjectType):
    course_id = graphene.String(required=True)
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    category = graphene.String(required=True)
    level = graphene.String(required=True)

class UpdateCoursesParams(graphene.InputObjectType):
    courses=graphene.List(UpdateCourseInput, required=True)


class CreateUserInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    gender = graphene.String(required=True)
    email = graphene.String(required=True)
    phone_number = graphene.String(required=True)


class CreateTopicInput(graphene.InputObjectType):
    module_id=graphene.String(required=True)
    title=graphene.String(required=True)
    description= graphene.String(required=True)
    topic_type= graphene.String(required=True)
    content= graphene.String(required=True)
    order=graphene.String(required=True)
    estimate_duration_in_mins= graphene.Int(required=True)


class CreateTopicsInput(graphene.InputObjectType):
    topics = graphene.List(CreateTopicInput,required=True)


class GetTopicsParams(graphene.InputObjectType):
    topic_ids = graphene.List(graphene.String, required=True)


class CreateCourseFeedbackInput(graphene.InputObjectType):
    course_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    rating = graphene.Int(required=True)
    message = graphene.String(required=False)


class CreateCourseReqParams(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    category = graphene.String(required=True)
    level = graphene.String(required=True)


class CreateCoursesReqParams(graphene.InputObjectType):
    courses = graphene.List(CreateCourseReqParams, required=True)


class GetCoursesReqParams(graphene.InputObjectType):
    course_ids = graphene.List(graphene.String, required=True)


class GetUserCourseCompletionReqParams(graphene.InputObjectType):
    course_id = graphene.String(required=True)
    user_id = graphene.String(required=True)


class GetRecommendedCoursesReqParams(graphene.InputObjectType):
    user_id = graphene.String(required=True)


class GetTopicsForCourseReqParams(graphene.InputObjectType):
    course_id = graphene.String(required=True)


class CreateModuleReqParams(graphene.InputObjectType):
    module_title = graphene.String(required=True)
    description = graphene.String(required=True)
    order = graphene.Int(required=True)


class CreateModulesReqParams(graphene.InputObjectType):
    modules = graphene.List(CreateModuleReqParams)


class UpdateModuleReqParams(graphene.InputObjectType):
    module_title = graphene.String(required=True)
    description = graphene.String(required=True)
    course_id = graphene.String(required=True)
    order = graphene.Int(required=True)
    module_id = graphene.String(required=True)


class UpdateModulesListReqParams(graphene.InputObjectType):
    update_modules = graphene.List(UpdateModuleReqParams, required=True)


class GetModulesForCourse(graphene.InputObjectType):
    course_ids = graphene.List(graphene.String, required=True)


class UpdateUserReqParams(graphene.InputObjectType):
    user_id = graphene.String(required=True)
    name = graphene.String(required=True)
    gender = graphene.String(required=True)
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    email = graphene.String(required=True)
    phone_number = graphene.Int(required=True)

class GetUserReqParms(graphene.InputObjectType):
    user_id = graphene.String(required=True)

class GetUserModulePercentageReqParams(graphene.InputObjectType):
    module_id = graphene.String(required=True)
    user_id = graphene.String(required=True)


class AddModulesToCourseReqParams(graphene.InputObjectType):
    course_id = graphene.String(required=True)
    module_ids = graphene.List(graphene.String, required=True)


class CreateTopicsReqParams(graphene.InputObjectType):
    title = graphene.String(required=True)
    module_id = graphene.String(required=True)
    description = graphene.String(required=True)
    topic_type = graphene.String(required=True)
    content = graphene.String(required=True)
    estimate_duration = graphene.String(required=True)

class UpdateTopicReqParams(graphene.InputObjectType):
    topic_id = graphene.String(required=True)
    topic_title = graphene.String(required=True)
    module_id = graphene.String(required=True)
    description = graphene.String(required=True)
    topic_type = graphene.String(required=True)
    content = graphene.String(required=True)
    order = graphene.Int(required=True)
    estimated_duration_in_mins = graphene.Int(required=True)

class UpdateTopicsReqParams(graphene.InputObjectType):
    topics = graphene.List(UpdateTopicReqParams,required=True)


class GetTopicsReqParams(graphene.InputObjectType):
    topic_ids = graphene.List(graphene.String, required=True)


class GetUserTopicCompletionPercentageReqParams(graphene.InputObjectType):
    user_id = graphene.String(required=True)
    topic_id = graphene.String(required=True)


class CreateEnrollmentReqParams(graphene.InputObjectType):
    user_id = graphene.String(required=True)
    course_id = graphene.String(required=True)


class GetUserEnrolledCourses(graphene.InputObjectType):
    user_id = graphene.String(required=True)


class GenerateCourseLearningPathReqParams(graphene.InputObjectType):
    course_id = graphene.String(required=True)


class GetUserLearningPath(graphene.InputObjectType):
    user_learning_path_id = graphene.String(required=True)


class StartUserLearningPathReqParams(graphene.InputObjectType):
    user_id = graphene.String(required=True)
    course_id = graphene.String(required=True)


class UpdateUserLearningUnit(graphene.InputObjectType):
    user_learning_path_id = graphene.String(required=True)
    learning_unit_id = graphene.String(required=True)
    Status = graphene.String(required=True)
    percentage = graphene.Int(required=True)

class GetUserLearningPathReqParams(graphene.InputObjectType):
    user_learning_path_id = graphene.String(required=True)

class UpdateLearningUnitProgressInput(graphene.InputObjectType):
    user_learning_path_id = graphene.String(required=True)
    user_learning_unit_id = graphene.Int(required=True)
    status = graphene.String(required=True)
    percentage = graphene.Int(required=True)

class FeedbackForCourseReqParams(graphene.InputObjectType):
    course_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    rating = graphene.Int(required=True)
    message = graphene.String(required=True)