import graphene

class CourseType(graphene.ObjectType):
    course_id = graphene.String(required=True)
    title = graphene.String(required=True)
    description = graphene.String()
    category = graphene.String(required=True)
    level = graphene.String(required=True)
    average_rating = graphene.Float()
    estimated_duration = graphene.Int()


class CoursesType(graphene.ObjectType):
    courses=graphene.List(CourseType,required=True)


class TopicType(graphene.ObjectType):
     module_id =  graphene.String(required=True)
     title = graphene.String(required=True)
     description = graphene.String(required=True)
     topic_type = graphene.String(required=True)
     content = graphene.String(required=True)
     estimated_duration_in_mins = graphene.Int(required=True)


class TopicsType(graphene.ObjectType):
    topics=graphene.List(TopicType, required=True)


class UserType(graphene.ObjectType):
    user_id = graphene.String(required=True)
    name = graphene.String(required=True)
    gender = graphene.String(required=True)
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    phone_number = graphene.String(required=True)
    is_active = graphene.Boolean(required=True)
    otp_count = graphene.Int(required=True)


class CourseFeedbackType(graphene.ObjectType):
    course_id = graphene.String()
    user_id = graphene.String()
    rating = graphene.Int()
    message = graphene.String()