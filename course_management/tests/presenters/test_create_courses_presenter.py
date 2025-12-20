import pytest
from course_management.presenters.create_courses_presenter import \
    CreateCoursesPresenter
from course_management.tests.factories.interactor_factories import \
    CourseDTOFactory
from course_management.view_graphql.types.types import CoursesType


@pytest.fixture
def presenter():
    return CreateCoursesPresenter()


class TestCreateCoursesPresenter:

    def test_present_courses_returns_courses_type(self, presenter):
        # Arrange
        from course_management.interactors.dtos import CourseCategoryEnum, LevelEnum
        courses_dtos = CourseDTOFactory.build_batch(
            2,
            category=CourseCategoryEnum.DEVELOPMENT,
            level=LevelEnum.BEGINNER
        )
        
        # Act
        response = presenter.present_courses(courses=courses_dtos)

        # Assert
        assert isinstance(response, CoursesType)
        assert len(response.courses) == 2
        
        for i, course_obj in enumerate(response.courses):
            dto = courses_dtos[i]
            assert course_obj.course_id == dto.course_id
            assert course_obj.title == dto.title
            assert course_obj.description == dto.description
            assert course_obj.category == dto.category.value
            assert course_obj.level == dto.level.value
            assert course_obj.average_rating == dto.average_rating
            assert course_obj.estimated_duration == dto.estimated_duration
