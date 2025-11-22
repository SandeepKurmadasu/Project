import graphene

from course_management.graphql.schema import Query as CourseQuery
from course_management.graphql.schema import Mutation as CourseMutation

from assessment.graphql.schema import Query as AssessmentQuery
from assessment.graphql.schema import Mutation as AssessmentMutation


class RootQuery(CourseQuery, AssessmentQuery, graphene.ObjectType):
    pass


class RootMutation(CourseMutation, AssessmentMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=RootQuery, mutation=RootMutation)
