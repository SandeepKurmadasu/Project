import graphene

from course_management.view_graphql.schema import Query as CourseQuery
from course_management.view_graphql.schema import Mutation as CourseMutation

from assessment.view_graphql.schema import Query as AssessmentQuery
from assessment.view_graphql.schema import Mutation as AssessmentMutation


class RootQuery(CourseQuery, AssessmentQuery, graphene.ObjectType):
    pass


class RootMutation(CourseMutation, AssessmentMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=RootQuery, mutation=RootMutation)
