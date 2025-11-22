from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from course_management.models import Topic, Module

@receiver(post_save, sender=Topic)
def update_durations_on_topic_save(sender, instance, **kwargs):
    module = instance.module

    # 1. Recalculate module duration from topics
    module_duration = Topic.objects.filter(
        module=module
    ).aggregate(
        total=Sum("estimated_duration_in_mins")
    )["total"] or 0

    module.estimated_duration_in_min = module_duration
    module.save(update_fields=["estimated_duration_in_min"])

    # 2. Recalculate course duration from modules
    course = module.course
    if course:
        course_duration = Module.objects.filter(
            course=course
        ).aggregate(
            total=Sum("estimated_duration_in_min")
        )["total"] or 0

        course.estimated_duration_in_min = course_duration
        course.save(update_fields=["estimated_duration_in_min"])
