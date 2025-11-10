import graphene
class CourseType(graphene.ObjectType):
    course_id = graphene.String(required=True)
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    category = graphene.String(required=True)
    level = graphene.String(required=True)
    average_rating = graphene.Int(required=True)
    estimated_duration = graphene.Int(required=True)

