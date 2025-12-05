from django.db.models.aggregates import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from course_management.models import Topic, Module, CourseFeedback
from course_management.signals.signal_services.generate_learning_path_service import \
    GenerateLearningPathService


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


@receiver(post_save, sender=CourseFeedback)
def update_the_course_average_rating(sender, instance, **kwargs):
    course = instance.course
    if course:
        course_rating = CourseFeedback.objects.filter(
            course_id=course.course_id).aggregate(avg=Avg('rating'))
        course.average_rating = course_rating['avg']
        course.save(update_fields=['average_rating'])


@receiver(post_save, sender=Module)
def update_the_learning_unit_in_a_course(sender, instance, created, **kwargs):
    if created:
        return

    course = instance.course
    if course:
        GenerateLearningPathService.generate_learning_path_for_course(
            course_id=course.course_id)
