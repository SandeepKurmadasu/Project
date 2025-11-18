from django.contrib import admin
from .models import (
    Course, Module, Topic, Enrollment, CourseFeedback,
    CourseLearningPath, LearningUnit, UserLearningPath, UserLearningUnit
)
from .models import User


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "level", "average_rating",
                    "estimated_duration_in_min", "created_at")
    search_fields = ("title", "description")
    list_filter = ("category", "level")
    ordering = ("created_at",)
    list_per_page = 20


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("module_title", "course", "order",
                    "estimated_duration_in_min", "created_at")
    search_fields = ("module_title", "description")
    list_filter = ("course",)
    autocomplete_fields = ("course",)
    list_select_related = ("course",)
    ordering = ("course", "order")


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("topic_title", "module", "topic_type", "order",
                    "estimated_duration_in_mins", "created_at")
    search_fields = ("topic_title", "description")
    list_filter = ("topic_type", "module__course")
    autocomplete_fields = ("module",)
    list_select_related = ("module",)
    ordering = ("module", "order")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "phone_number", "is_active",
                    "created_at")
    search_fields = ("username", "email", "phone_number")
    list_filter = ("is_active", "gender")
    ordering = ("created_at",)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "course_status", "created_at")
    search_fields = ("user__username", "course__title")
    list_filter = ("course_status",)
    autocomplete_fields = ("user", "course")
    list_select_related = ("user", "course")


@admin.register(CourseFeedback)
class CourseFeedbackAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "rating", "created_at")
    search_fields = ("user__username", "course__title")
    list_filter = ("rating",)
    autocomplete_fields = ("user", "course")
    list_select_related = ("user", "course")


@admin.register(CourseLearningPath)
class CourseLearningPathAdmin(admin.ModelAdmin):
    list_display = ("learning_path_id", "course", "created_at")
    search_fields = ("course__title",)
    autocomplete_fields = ("course",)
    list_select_related = ("course",)


@admin.register(LearningUnit)
class LearningUnitAdmin(admin.ModelAdmin):
    list_display = ("learning_unit_id", "learning_path", "topic", "order",
                    "created_at")
    search_fields = ("topic__topic_title",)
    list_filter = ("learning_path",)
    autocomplete_fields = ("learning_path", "topic")
    list_select_related = ("learning_path", "topic")
    ordering = ("learning_path", "order")


@admin.register(UserLearningPath)
class UserLearningPathAdmin(admin.ModelAdmin):
    list_display = ("user", "learning_path", "status", "overall_percentage",
                    "created_at")
    search_fields = ("user__username", "learning_path__course__title")
    list_filter = ("status",)
    autocomplete_fields = ("user", "learning_path", "current_learning_unit")
    list_select_related = ("user", "learning_path", "current_learning_unit")


@admin.register(UserLearningUnit)
class UserLearningUnitAdmin(admin.ModelAdmin):
    list_display = ("user_learning_path", "learning_unit", "status",
                    "percentage", "is_locked", "created_at")
    search_fields = ("user_learning_path__user__username",
                     "learning_unit__topic__topic_title")
    list_filter = ("status", "is_locked")
    autocomplete_fields = ("user_learning_path", "learning_unit")
    list_select_related = ("user_learning_path", "learning_unit")
