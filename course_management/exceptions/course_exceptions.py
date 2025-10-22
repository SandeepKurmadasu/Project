from typing import List

class InvalidCourseIds(Exception):

    def __init__(self,course_ids : List[str]):
        super().__init__()
        self.course_ids=course_ids

    def __str__(self):
        return f"Invalid Course Ids: {self.course_ids}"

class InvalidCourseData(Exception):

    def __init__(self,invalid_fields: List[str]):
        super().__init__()
        self.invalid_fields=invalid_fields

    def __str__(self):
        return f"Invalid course data fields: {self.invalid_fields}"

class InvalidUserId(Exception):
    def __init__(self,user_id:str):
        super().__init__()
        self.user_id=user_id