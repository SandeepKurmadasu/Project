class GetCourseCompletionPercentageInteractor(ValidationMixin):

    def __init__(self,progress_storage: ProgressStorageInterface,course_storage: CourseStorageInterface):
        self.progress_storage = progress_storage
        self.course_storage = course_storage

    def get_course_completion_percentage(self,user_id: str,course_id: str) -> CourseCompletionResponseDTO:
        self.validate_user_id(user_id=user_id)
        self.validate_course_id(course_id=course_id)

        course_progress = self.progress_storage.get_course_progress(
            user_id=user_id,
            course_id=course_id
        )

        topics_progress = self.progress_storage.get_all_topics_progress(
            user_id=user_id,
            course_id=course_id
        )

        next_topic = self.progress_storage.get_next_incomplete_topic(
            user_id=user_id,
            course_id=course_id
        )

        status = self._calculate_status(completion_percentage=course_progress.completion_percentage)

        total_hours = self.course_storage.get_total_course_hours(course_id=course_id)
        estimated_hours_remaining = self._calculate_hours_remaining(
            total_hours=total_hours,
            completion_percentage=course_progress.completion_percentage
        )

        response = CourseCompletionResponseDTO(
            course_id=course_progress.course_id,
            user_id=course_progress.user_id,
            completion_percentage=course_progress.completion_percentage,
            total_topics=course_progress.total_topics,
            completed_topics=course_progress.completed_topics,
            status=status,
            topics_progress=topics_progress,
            next_topic=next_topic,
            estimated_hours_remaining=estimated_hours_remaining
        )

        return response

    def _calculate_status(self, completion_percentage: float) -> str:
        if completion_percentage == 0:
            return "not_started"
        elif completion_percentage < 50:
            return "in_progress"
        elif completion_percentage < 100:
            return "nearly_done"
        else:
            return "completed"

    def _calculate_hours_remaining(self, total_hours: float, completion_percentage: float) -> float:
        remaining_percentage = 100 - completion_percentage
        hours_remaining = (remaining_percentage / 100) * total_hours
        return round(hours_remaining, 1)

