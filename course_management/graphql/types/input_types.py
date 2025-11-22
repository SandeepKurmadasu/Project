
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