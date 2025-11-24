import json
import pytest
from faker import Faker

from course_management.storages.module_storage import ModuleStorage
from course_management.interactors.dtos import (
    CreateModuleDTO,
    ModuleDTO,
    UpdateModuleDTO,
)
from course_management.models import Course, Module
from course_management.tests.factories.storage_factories import ModuleFactory

Faker.seed(1)


def module_dto_to_json(dto: ModuleDTO) -> dict:
    d = dto.__dict__.copy()
    d["module_id"] = "STATIC-MODULE-ID"
    d["course_id"] = "STATIC-COURSE-ID" if d.get("course_id") else None
    return d


def dto_list(dtos):
    return [module_dto_to_json(d) for d in dtos]



@pytest.fixture
def course():
    return Course.objects.create(
        title="Python Basics",
        description="Intro",
        category=Course.CourseCategoryEnum.DEVELOPMENT,
        level=Course.LevelEnum.BEGINNER,
        estimated_duration_in_min=60,
    )



@pytest.mark.django_db
def test_get_modules_for_courses(snapshot, course):
    _m1 = Module.objects.create(
        course=course,
        module_title="Mod A",
        description="Desc A",
        order=1,
        estimated_duration_in_min=10,
    )
    _m2 = Module.objects.create(
        course=course,
        module_title="Mod B",
        description="Desc B",
        order=2,
        estimated_duration_in_min=20,
    )

    storage = ModuleStorage()
    result = storage.get_modules_for_courses([str(course.course_id)])

    snapshot.assert_match(
        json.dumps(dto_list(result), indent=2, sort_keys=True),
        "get_modules_for_courses",
    )


@pytest.mark.django_db
def test_create_modules(snapshot):
    storage = ModuleStorage()

    dtos = [
        CreateModuleDTO(
            module_title="New Mod 1",
            description="D1",
            order=1,
        ),
        CreateModuleDTO(
            module_title="New Mod 2",
            description="D2",
            order=2,
        ),
    ]

    result = storage.create_modules(dtos)

    snapshot.assert_match(
        json.dumps(dto_list(result), indent=2, sort_keys=True),
        "create_modules",
    )


@pytest.mark.django_db
def test_update_modules(snapshot, course):
    module = Module.objects.create(
        course=course,
        module_title="Old",
        description="Old desc",
        order=1,
        estimated_duration_in_min=10,
    )

    storage = ModuleStorage()

    updates = [
        UpdateModuleDTO(
            module_id=str(module.module_id),
            course_id=str(course.course_id),
            order=1,
            module_title="New Title",
            description="New Desc",
        )
    ]

    result = storage.update_modules(updates)

    snapshot.assert_match(
        json.dumps(dto_list(result), indent=2, sort_keys=True),
        "update_modules",
    )

    module.refresh_from_db()
    assert module.module_title == "New Title"
    assert module.description == "New Desc"


@pytest.mark.django_db
def test_add_modules_to_course(snapshot, course):
    m1 = Module.objects.create(
        module_title="Unassigned 1",
        description="D1",
        order=1,
        estimated_duration_in_min=5,
    )
    m2 = Module.objects.create(
        module_title="Unassigned 2",
        description="D2",
        order=2,
        estimated_duration_in_min=10,
    )

    storage = ModuleStorage()
    module_ids = [m1.module_id,m2.module_id]

    dtos = [
        ModuleDTO(
            module_id=str(m1.module_id),
            course_id=str(course.course_id),
            module_title=m1.module_title,
            description=m1.description,
            order=m1.order,
            estimated_duration=m1.estimated_duration_in_min,
        ),
        ModuleDTO(
            module_id=str(m2.module_id),
            course_id=str(course.course_id),
            module_title=m2.module_title,
            description=m2.description,
            order=m2.order,
            estimated_duration=m2.estimated_duration_in_min,
        ),
    ]

    result = storage.add_modules_to_course(str(course.course_id), module_ids=module_ids)
    result_dict = dto_list(result)
    result_dict = sorted(result_dict, key=lambda m: m["order"])

    snapshot.assert_match(
        repr(result_dict),
        "add_modules_to_course",
    )


@pytest.mark.django_db
def test_get_module_ids_for_titles(snapshot, course):
    m1 = Module.objects.create(
        course=course,
        module_title="A",
        description="X",
        order=1,
        estimated_duration_in_min=10,
    )
    Module.objects.create(
        course=course,
        module_title="B",
        description="Y",
        order=2,
        estimated_duration_in_min=20,
    )

    storage = ModuleStorage()

    ids = storage.get_module_ids_for_titles(["A"])

    snapshot.assert_match(
        json.dumps(["STATIC-MODULE-ID"], indent=2, sort_keys=True),
        "get_module_ids_for_titles",
    )

    assert str(m1.module_id) in [str(i) for i in ids]


@pytest.mark.django_db
def test_get_course_modules(snapshot, course):
    m1 = Module.objects.create(
        course=course,
        module_title="Course Mod 1",
        description="D1",
        order=1,
        estimated_duration_in_min=10,
    )
    m2 = Module.objects.create(
        course=course,
        module_title="Course Mod 2",
        description="D2",
        order=2,
        estimated_duration_in_min=20,
    )
    other_course = Course.objects.create(
        title="Another",
        description="",
        category=Course.CourseCategoryEnum.DEVELOPMENT,
        level=Course.LevelEnum.BEGINNER,
        estimated_duration_in_min=30,
    )
    Module.objects.create(
        course=other_course,
        module_title="Other",
        description="X",
        order=1,
        estimated_duration_in_min=5,
    )

    storage = ModuleStorage()
    result = storage.get_course_modules(str(course.course_id))

    snapshot.assert_match(
        json.dumps(dto_list(result), indent=2, sort_keys=True),
        "get_course_modules",
    )

    ids = {str(m.module_id) for m in result}
    assert str(m1.module_id) in ids
    assert str(m2.module_id) in ids
    assert len(ids) == 2


@pytest.mark.django_db
def test_get_modules(snapshot, course):
    modules = ModuleFactory.build_batch(2)

    module_ids = [obj.module_id for obj in modules]

    storage = ModuleStorage()
    result = storage.get_modules(module_ids=module_ids)

    snapshot.assert_match(
        repr(result),
        "get_modules",
    )
