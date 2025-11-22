import graphene

from course_management.graphql.mutations.create_courses import CreateCourses
from course_management.graphql.mutations.create_topics import CreateTopics
from course_management.graphql.mutations.create_user import CreateUser
from course_management.graphql.mutations.update_courses import UpdateCourses


class CreateCourse(graphene.ObjectType):
    create_course = CreateCourses.Field(required=True)


class UpdateCourse(graphene.ObjectType):
    update_course = UpdateCourses.Field(required=True)


class CreateUsers(graphene.ObjectType):
    create_user = CreateUser.Field(required=True)


class CreateTopic(graphene.ObjectType):
    create_topics = CreateTopics.Field(required=True)

