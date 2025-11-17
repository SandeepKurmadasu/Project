import graphene


class CourseType(graphene.ObjectType):
    course_id = graphene.String(required=True)
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    category = graphene.String(required=True)
    level = graphene.String(required=True)
    average_rating = graphene.Int(required=True)
    estimated_duration = graphene.Int(required=True)


class CoursesType(graphene.ObjectType):
    courses = graphene.List(CourseType, Required=True)


class ModuleType(graphene.ObjectType):
    module_id = graphene.String(required=True)
    course_id = graphene.String(required=True)
    module_title = graphene.String(required=True)
    description = graphene.String(required=True)
    order = graphene.Int(required=True)
    estimated_duration_in_mins = graphene.Int(required=True)


class TopicGQLType(graphene.ObjectType):
    topic_id = graphene.String(required=True)
    module_id = graphene.String(required=True)
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    topic_type = graphene.String(required=True)
    content = graphene.String(required=True)
    order = graphene.Int(required=True)
    estimate_duration_in_mins = graphene.Int(required=True)

    # @staticmethod
    # def resolve_module(root, info):
    #     loader = ModuleByIdDataLoader(context=info.context)
    #     return loader.load(root.module_id)


class TopicsList(graphene.ObjectType):
    topics = graphene.List(TopicGQLType)


class EnrollmentType(graphene.ObjectType):
    id = graphene.Int(required=True)
    user_id = graphene.String(required=True)
    course_id = graphene.String(required=True)
    course_status = graphene.String(required=True)
    course_percentage = graphene.Int(required=True)
    user_learning_path_id = graphene.String(required=True)


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
