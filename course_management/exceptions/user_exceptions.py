class InvalidUserId(Exception):
    def __init__(self, user_id: str):
        super().__init__()
        self.user_id = user_id

    def __str__(self):
        return f"Invalid user id: {self.user_id}"


class UserNotFound(Exception):
    def __init__(self, user_id: str):
        super().__init__()
        self.user_id = user_id

    def __str__(self):
        return f"User not found: {self.user_id}"


class InvalidCourseId(Exception):
    def __init__(self, course_id: str):
        super().__init__()
        self.course_id = course_id

    def __str__(self):
        return f"Invalid course id: {self.course_id}"


class ProgressNotFound(Exception):
    def __init__(self, user_id: str, course_id: str):
        super().__init__()
        self.user_id = user_id
        self.course_id = course_id

    def __str__(self):
        return f"Progress not found for user {self.user_id} in course {self.course_id}"