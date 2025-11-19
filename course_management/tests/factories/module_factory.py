import uuid

import factory

from course_management.models import Module
from course_management.tests.factories.storage_factories import CourseFactory


class ModuleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Module

    module_id = factory.LazyFunction(uuid.uuid4)
    course = factory.SubFactory(CourseFactory)
    module_title = factory.Faker("sentence", nb_words=2)
    description = factory.Faker("sentence")
    order = factory.Sequence(lambda n: n + 1)
    estimated_duration_in_min = 30