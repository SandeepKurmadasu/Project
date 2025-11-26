import graphene


class TopicType(graphene.ObjectType):
     module_id =  graphene.String(required=True)
     title = graphene.String(required=True)
     description = graphene.String(required=True)
     topic_type = graphene.String(required=True)
     content = graphene.String(required=True)
     estimated_duration_in_mins = graphene.Int(required=True)


class TopicsType(graphene.ObjectType):
    topics=graphene.List(TopicType, required=True)


class CourseFeedbackType(graphene.ObjectType):
    course_id = graphene.String()
    user_id = graphene.String()
    rating = graphene.Int()
    message = graphene.String()


class CourseType(graphene.ObjectType):
    course_id = graphene.String(required=True)
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    category = graphene.String(required=True)
    level = graphene.String(required=True)
    average_rating = graphene.Float(required=True)
    estimated_duration = graphene.Int(required=True)


class CoursesType(graphene.ObjectType):
    courses = graphene.List(CourseType, required=True)


class ModuleType(graphene.ObjectType):
    module_id = graphene.String(required=True)
    course_id = graphene.String()
    module_title = graphene.String(required=True)
    description = graphene.String(required=True)
    order = graphene.Int(required=True)
    estimated_duration_in_mins = graphene.Int()


class ModuleList(graphene.ObjectType):
    modules = graphene.List(ModuleType, required=True)


class TopicGQLType(graphene.ObjectType):
    topic_id = graphene.String(required=True)
    module_id = graphene.String(required=True)
    topic_title = graphene.String(required=True)
    description = graphene.String(required=True)
    topic_type = graphene.String(required=True)
    content = graphene.String(required=True)
    order = graphene.Int(required=True)
    estimated_duration_in_mins = graphene.Int(required=True)



class TopicsListType(graphene.ObjectType):
    topics = graphene.List(TopicGQLType,required=True)


class UserType(graphene.ObjectType):
    user_id = graphene.String(required=True)
    name = graphene.String(required=True)
    gender = graphene.String(required=True)
    username = graphene.String(required=True)
    password = graphene.String()
    email = graphene.String(required=True)
    phone_number = graphene.String(required=True)
    is_active = graphene.Boolean(required=True)
    otp_count = graphene.Int(required=True)


class EnrollmentType(graphene.ObjectType):
    id = graphene.Int(required=True)
    user_id = graphene.String(required=True)
    course_id = graphene.String(required=True)
    course_status = graphene.String(required=True)
    course_percentage = graphene.Int(required=True)
    user_learning_path_id = graphene.String(required=True)


class EnrollmentListType(graphene.ObjectType):
    enrollments = graphene.List(EnrollmentType,required=True)


class LearningUnitType(graphene.ObjectType):
    learning_unit_id = graphene.String(required=True)
    learning_path_id = graphene.String(required=True)
    unit_type = graphene.String(required=True)
    topic_id = graphene.String(required=True)
    unit_title = graphene.String(required=True)
    order = graphene.Int(required=True)
    estimated_duration_in_minutes = graphene.Int(required=True)


class LearningPathType(graphene.ObjectType):
    learning_path_id = graphene.String(required=True)
    course_id = graphene.String(required=True)
    course_title = graphene.String(required=True)
    total_units = graphene.Int(required=True)
    estimated_total_duration_in_minutes = graphene.Int(required=True)
    learning_units = graphene.List(LearningUnitType)


class UserLearningUnitType(graphene.ObjectType):
    user_learning_path_id = graphene.String(required=True)
    user_learning_unit_id = graphene.String(required=True)
    status = graphene.String(required=True)
    percentage = graphene.String(required=True)


class UserLearningPathType(graphene.ObjectType):
    user_learning_path_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    learning_path_id = graphene.String(required=True)
    current_learning_unit_id = graphene.String(required=True)
    overall_percentage = graphene.Int(required=True)
    status = graphene.String(required=True)

class UserLearningPathPercentageType(graphene.ObjectType):
    user_id = graphene.String(required=True)
    learning_path_id = graphene.String(required=True)
    percentage = graphene.Int(required=True)

class UserCurrentLearningUnitStatusType(graphene.ObjectType):
    user_learning_path_id = graphene.String(required=True)
    user_learning_unit_id = graphene.Int(required=True)
    percentage = graphene.Int(required=True)
    status = graphene.String(required=True)

class UpdateLearningUnitProgressType(graphene.ObjectType):
    user_learning_path_id = graphene.String(required=True)
    user_learning_unit_id = graphene.Int(required=True)
    updated_status = graphene.String(required=True)
    updated_percentage = graphene.Int(required=True)
    next_unit_unlocked = graphene.Boolean(required=True)
    next_unit_id = graphene.Int()
    overall_path_percentage = graphene.Int(required=True)

class GetUserCourseCompletionPercentageType(graphene.ObjectType):
    course_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    percentage = graphene.Int(required=True)

class GetModuleCompletionPercentageType(graphene.ObjectType):
    module_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    percentage = graphene.Int(required=True)

class GetTopicCompletionPercentageType(graphene.ObjectType):
    topic_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    percentage = graphene.Int(required=True)


class FeedbackType(graphene.ObjectType):
    course_id = graphene.String(required=True)
    user_id = graphene.String(required=True)
    rating = graphene.Int(required=True)
    message = graphene.String(required=True)
