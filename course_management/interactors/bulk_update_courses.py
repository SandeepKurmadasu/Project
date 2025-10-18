from course_management.tests import CourseStorageInterface, UpdateCourseRequestDTO, CourseDTO, InvalidCourseIds

class BulkUpdateInteractor:

    def __init__(self,course_storage:CourseStorageInterface):
        self.course_storage=course_storage

    def bulk_update_courses(self,requests :List[UpdateCourseRequestDTO]) -> List[CourseDTO]:

        course_ids=[]
        for request in requests:
            self.validate_course_data(
                course_id=request.course_id,
                name=request.name,
                description=request.description
            )
            course_ids.append(request.course_id)

        courses=self.course_storage.bulk_update_courses(courses=requests)
        return courses

    @staticmethod
    def _validate_course_data(self,course_id : str,name: str,description:str):
        if not course_id or course_id.strip() == "":
            raise InvalidCourseIds(course_ids=[course_id])
    CourseValidator.validate_course_data(name,description)













    # def check_courses_exist(self,course_ids: List[str]):
    #     courses=self.course_storage.get_courses_by_ids(course_ids)
    #     found_ids=[course.course_id for course in courses]
    #
    #     missing_ids=list(set(course_ids) - set(found_ids))
    #
    #     if missing_ids:
    #         raise InvalidCourseIds(course_ids=missing_ids)