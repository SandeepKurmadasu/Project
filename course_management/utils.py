from django.db.models import Sum
from course_management.models import Course, Module, Topic


def calculate_module_duration(module_id):
    total_duration=Topic.objects.filter(
        module_id=module_id).aggregate(total=Sum("estimated_duration_in_mins"))["total"]
    return total_duration


def update_module_duration(module_id):
    total_duration=calculate_module_duration(module_id)
    Module.objects.filter(module_id=module_id).update(estimated_duration_in_min=total_duration)
    return total_duration


def calculate_course_duration(course_id):
    total_duration = Module.objects.filter(
        course_id=course_id).aggregate(total=Sum("estimated_duration_in_min"))["total"]
    return total_duration


def update_course_duration(course_id):
    duration = calculate_course_duration(course_id)
    Course.objects.filter(course_id=course_id).update(estimated_duration_in_min=duration)
    return duration


def update_durations_after_topic_change(topic):
    """
    After creating or updating a topic, call this method to update:
     -> Module duration
     -> Course duration
    """
    module_id = topic.module_id
    course_id = topic.module.course_id

    # Update module duration
    update_module_duration(module_id)

    # Update course duration
    update_course_duration(course_id)