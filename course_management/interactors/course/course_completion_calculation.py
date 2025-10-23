from course_management.interactors.dtos import ModuleDTO, TopicDTO, UserTopicCompletionPercentageDTO
from typing import List

class CourseCompletionCalculator:

    @staticmethod
    def calculate_course_percentage(
            modules: List[ModuleDTO],
            topics: List[TopicDTO],
            user_topic_progress: List[UserTopicCompletionPercentageDTO]) -> float:

        if not modules or not topics:
            return 0.0
        topic_completion_map = {utp.topic_id: utp.percentage for utp in user_topic_progress}

        module_percentages = []

        for module in modules:
            # GET TOPICS BELONGS TO THIS MODULE
            module_topics = [t for t in topics if t.module_id == module.module_id]

            if not module_topics:
                module_percentages.append(0.0)
                continue

            total_module_percentage = sum(topic_completion_map.get(t.topic_id, 0.0) for t in module_topics)
            module_avg = total_module_percentage / len(module_topics)
            module_percentages.append(module_avg)

        course_percentage = sum(module_percentages) / len(module_percentages)

        return round(course_percentage, 2)

