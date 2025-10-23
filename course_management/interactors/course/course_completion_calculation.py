from course_management.interactors.dtos import ModuleDTO, TopicDTO, UserTopicCompletionPercentageDTO

class CourseCompletionCalculator:

    @staticmethod
    def calculate_course_percentage(
            modules: list[ModuleDTO],
            topics: list[TopicDTO],
            user_topic_progress: list[UserTopicCompletionPercentageDTO]
    ) -> float:

        topic_completion_map = {utp.topic_id: utp.percentage for utp in user_topic_progress}
        module_ids = [module.module_id for module in modules]

        module_percentages = []
        for module_id in module_ids:
            module_topics = [t for t in topics if t.module_id == module_id]
            if not module_topics:
                module_percentages.append(0)
                continue

            topic_percentages = [topic_completion_map.get(t.topic_id, 0) for t in module_topics]
            module_avg = sum(topic_percentages) / len(topic_percentages)
            module_percentages.append(module_avg)

        if not module_percentages:
            return 0

        return sum(module_percentages) / len(module_percentages)