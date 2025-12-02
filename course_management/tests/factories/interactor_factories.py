import random

import factory
from course_management.interactors.dtos import LevelEnum, \
    CourseDTO, \
    CreateCourseDTO, UpdateCourseDTO, \
    EnrollmentDTO, ModuleDTO, TopicDTO, CreateTopicDTO, UserDTO, CreateUserDTO, \
    TopicTypeEnum, CreateModuleDTO, \
    UpdateModuleDTO, LearningPathForCourseDTO, LearningUnitDTO, \
    UserLearningPathDTO, \
    StatusEnum, CourseCategoryEnum


class CreateCourseDTOFactory(factory.Factory):
    class Meta:
        model = CreateCourseDTO

    title = factory.Sequence(lambda n: f"Course-{n + 1}")
    description = factory.Faker("paragraph", nb_sentences=3)
    category = factory.Iterator(list(CourseCategoryEnum))
    level = factory.Iterator([lvl.value for lvl in LevelEnum])


class UpdateCourseDTOFactory(factory.Factory):
    class Meta:
        model = UpdateCourseDTO

    course_id = factory.Sequence(lambda n: f"C{n + 1:04d}")
    title = factory.Sequence(lambda n: f"Course-{n + 1}")
    description = factory.Faker("paragraph", nb_sentences=3)
    category = factory.Iterator(
        ["programming", "design", "business", "science"])
    level = factory.Iterator([lvl.value for lvl in LevelEnum])


class EnrollmentDTOFactory(factory.Factory):
    class Meta:
        model = EnrollmentDTO

    id = factory.Sequence(lambda n: n + 1)
    user_id = factory.Faker("uuid4")
    course_id = factory.Sequence(lambda n: f"C{n + 1:04d}")
    course_title = factory.Faker('word')
    user_learning_path_id = factory.Sequence(lambda n: f"ULP{n + 1:04d}")
    course_status = factory.Iterator(["PASS", "FAIL", "IN_PROGRESS"])
    course_percentage = factory.Faker("random_int", min=0, max=100)


class ModuleDTOFactory(factory.Factory):
    class Meta:
        model = ModuleDTO

    module_id = factory.Sequence(lambda n: f"M{n + 1:04d}")
    course_id = factory.LazyAttribute(lambda obj: f"C0001")
    module_title = factory.Sequence(lambda n: f"Module-{n + 1}")
    description = factory.Faker("paragraph", nb_sentences=2)
    order = factory.sequence(lambda n: n + 1)
    estimated_duration = factory.Faker("random_int", min=30, max=120)


class TopicDTOFactory(factory.Factory):
    class Meta:
        model = TopicDTO

    topic_id = factory.Sequence(lambda n: f"T{n + 1:04d}")
    module_id = factory.LazyAttribute(lambda obj: f"M0001")
    title = factory.Sequence(lambda n: f"Topic-{n + 1}")
    description = factory.Faker("paragraph", nb_sentences=2)
    topic_type = TopicTypeEnum.LEARNING
    content = factory.Faker("text")
    order = factory.sequence(lambda n: n + 1)
    estimate_duration_in_mins = factory.Faker("random_int", min=10, max=60)


class CreateTopicDTOFactory(factory.Factory):
    class Meta:
        model = CreateTopicDTO

    title = factory.Sequence(lambda n: f"Topic-{n + 1}")
    description = factory.Faker("paragraph", nb_sentences=2)
    module_id = factory.Sequence(lambda n: f"M{n + 1:04d}")
    order=factory.Faker("random_int", min=1, max=20)
    topic_type = factory.LazyFunction(
        lambda: random.choice(list(TopicTypeEnum)))
    content = factory.Faker("text")
    estimate_duration_in_mins = factory.Faker("random_int", min=10, max=60)


class CourseDTOFactory(factory.Factory):
    class Meta:
        model = CourseDTO

    course_id = factory.Sequence(lambda n: f"C{n + 1:04d}")
    title = factory.Sequence(lambda n: f"Course-{n + 1}")
    description = factory.Faker("paragraph", nb_sentences=3)
    category = factory.Iterator(
        ["programming", "design", "business", "science"])
    level = factory.Iterator([lvl.value for lvl in LevelEnum])
    average_rating = 0
    estimated_duration = factory.Faker("random_element",
                                       elements=[60, 90, 120, 150, 180, 240,
                                                 300])


class CreateUserDTOFactory(factory.Factory):
    class Meta:
        model = CreateUserDTO

    name = factory.Faker("name")
    gender = factory.Iterator(["MALE", "FEMALE", "OTHERS"])
    username = factory.Faker("user_name")
    password = factory.Faker("password")
    email = factory.Faker("email")
    phone_number = factory.Faker("random_number", digits=10)


class UserDTOFactory(factory.Factory):
    class Meta:
        model = UserDTO

    user_id = factory.Sequence(lambda n: f"U{n + 1:04d}")
    name = factory.Faker("name")
    gender = factory.Iterator(["MALE", "FEMALE", "OTHERS"])
    username = factory.Faker("user_name")
    password = factory.Faker("password")
    email = factory.Faker("email")
    phone_number = factory.Faker("random_number", digits=10)
    is_active = factory.Faker("boolean")
    otp_count = factory.Faker("random_int", min=0, max=10)


class CreateModuleDTOFactory(factory.Factory):
    class Meta:
        model = CreateModuleDTO

    module_title = factory.Faker("Word")
    description = factory.Faker("sentence")
    order = factory.Faker("random_int", min=0, max=10)


class UpdateModuleDTOFactory(factory.Factory):
    class Meta:
        model = UpdateModuleDTO

    module_id = factory.sequence(lambda n: f"MOD{n + 1}")
    course_id = factory.Sequence(lambda n: f"Course-{n + 1}")
    order = factory.Faker("random_int", min=0, max=10)
    module_title = factory.Faker("word")
    description = factory.Faker("sentence")


class LearningUnitDTOFactory(factory.Factory):
    class Meta:
        model = LearningUnitDTO

    learning_unit_id = factory.Sequence(lambda n: f"lu-{n}")
    learning_path_id = "lp-123"
    unit_type = factory.Iterator(["LEARNING", "ASSESSMENT"])
    topic_id = factory.Sequence(lambda n: f"topic-{n}")
    unit_title = factory.Sequence(lambda n: f"Unit {n}")
    order = factory.Sequence(lambda n: n + 1)
    estimated_duration_in_minutes = 10


class LearningPathForCourseDTOFactory(factory.Factory):
    class Meta:
        model = LearningPathForCourseDTO

    learning_path_id = "lp-123"
    course_id = "course-123"
    course_title = "Test Course"
    total_units = 3
    estimated_total_duration_in_minutes = 60
    learning_units = factory.List([
        LearningUnitDTOFactory(),
        LearningUnitDTOFactory(),
        LearningUnitDTOFactory()
    ])


class UserLearningPathDTOFactory(factory.Factory):
    class Meta:
        model = UserLearningPathDTO

    user_learning_path_id = factory.Sequence(lambda n: f"ulp-{n + 1}")
    user_id = factory.Sequence(lambda n: f"user-{n + 1}")
    learning_path_id = factory.Sequence(lambda n: f"lp-{n + 1}")
    current_learning_unit_id = factory.Sequence(lambda n: f"lu-{n + 1}")
    overall_percentage = factory.Faker("random_int", min=0, max=100)
    status = factory.Iterator([
        StatusEnum.START,
        StatusEnum.IN_PROGRESS,
        StatusEnum.COMPLETE,
    ])
