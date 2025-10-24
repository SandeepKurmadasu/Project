import factory
from course_management.interactors.dtos import CreateCourseDTO, CourseDTO, UpdateCourseDTO, EnrollmentDTO, ModuleDTO, TopicDTO, CreateTopicDTO, LevelEnum

class CreateCourseDTOFactory(factory.Factory):
    class Meta:
        model = CreateCourseDTO

    title = factory.Sequence(lambda n: f"Course-{n+1}")
    description = factory.Faker("paragraph", nb_sentences=3)
    category = factory.Iterator(["programming", "design", "business", "science"])
    level = factory.Iterator([lvl.value for lvl in LevelEnum])

class UpdateCourseDTOFactory(factory.Factory):
    class Meta:
        model = UpdateCourseDTO

    course_id = factory.Sequence(lambda n: f"C{n+1:04d}")
    title = factory.Sequence(lambda n: f"Course-{n+1}")
    description = factory.Faker("paragraph", nb_sentences=3)
    category = factory.Iterator(["programming", "design", "business", "science"])
    level = factory.Iterator([lvl.value for lvl in LevelEnum])

class EnrollmentDTOFactory(factory.Factory):
    class Meta:
        model = EnrollmentDTO

    id = factory.Sequence(lambda n: n + 1)
    user_id = factory.Faker("uuid4")
    course_id = factory.Sequence(lambda n: f"C{n+1:04d}")
    course_percentage = factory.Faker("random_int", min=0, max=100)

class ModuleDTOFactory(factory.Factory):
    class Meta:
        model = ModuleDTO

    module_id = factory.Sequence(lambda n: f"M{n+1:04d}")
    course_id = factory.LazyAttribute(lambda obj: f"C0001")
    module_title = factory.Sequence(lambda n: f"Module-{n+1}")
    description = factory.Faker("paragraph", nb_sentences=2)
    estimated_duration = factory.Faker("random_int", min=30, max=120)

class TopicDTOFactory(factory.Factory):
    class Meta:
        model = TopicDTO

    topic_id = factory.Sequence(lambda n: f"T{n+1:04d}")
    module_id = factory.LazyAttribute(lambda obj: f"M0001")
    title = factory.Sequence(lambda n: f"Topic-{n+1}")
    description = factory.Faker("paragraph", nb_sentences=2)
    topic_type = factory.Iterator(["video", "quiz", "article"])
    content = factory.Faker("text")
    estimated_duration = factory.Faker("random_int", min=10, max=60)

class CreateTopicDTOFactory(factory.Factory):
    class Meta:
        model = CreateTopicDTO

    title = factory.Sequence(lambda n: f"Topic-{n+1}")
    description = factory.Faker("paragraph", nb_sentences=2)
    topic_type = factory.Iterator(["video", "quiz", "article"])
    content = factory.Faker("text")
    estimate_duration = factory.Faker("random_int", min=10, max=60)

class CourseDTOFactory(factory.Factory):
    class Meta:
        model = CourseDTO

    course_id = factory.Sequence(lambda n: f"C{n+1:04d}")
    title = factory.Sequence(lambda n: f"Course-{n+1}")
    description = factory.Faker("paragraph", nb_sentences=3)
    category = factory.Iterator(["programming", "design", "business", "science"])
    level = factory.Iterator([lvl.value for lvl in LevelEnum])
    average_rating = 0
    estimated_duration = factory.Faker("random_element", elements=[60, 90, 120, 150, 180, 240, 300])