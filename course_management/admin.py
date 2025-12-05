import csv

from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.http import HttpResponse

from .models import (
    Course, Module, Topic, Enrollment, CourseFeedback,
    CourseLearningPath, LearningUnit, UserLearningPath, UserLearningUnit, Video, RateLimitEntry
)
from .models import User


class CourseFeedbackForm(forms.ModelForm):
    class Meta:
        model = CourseFeedback
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get("user")
        course = cleaned_data.get("course")

        if not self.instance.pk:
            if CourseFeedback.objects.filter(user=user, course=course).exists():
                raise ValidationError(
                    "This user has already given feedback for this course."
                )
        return cleaned_data

def make_active(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    modeladmin.message_user(request, f"{updated} user(s) marked as active.")


make_active.short_description = "Mark selected users as active"


def make_inactive(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    modeladmin.message_user(request, f"{updated} user(s) marked as inactive.")


make_inactive.short_description = "Mark selected users as inactive"


def export_users_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=users.csv'

    writer = csv.writer(response)
    writer.writerow(
        ['User ID', 'Username', 'Email', 'Phone Number', 'Is Active',
         'Created At'])

    for user in queryset:
        writer.writerow(
            [user.user_id, user.username, user.email, user.phone_number,
             user.is_active, user.created_at])

    return response


export_users_to_csv.short_description = "Export Selected Users to CSV"


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("course_id", "title", "category", "level",
                    "average_rating",
                    "estimated_duration_in_min", "created_at")
    search_fields = ("title", "description")
    list_filter = ("category", "level")
    ordering = ("created_at",)
    list_per_page = 20


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("module_title", "module_id", "course", "order",
                    "estimated_duration_in_min", "created_at")
    search_fields = ("module_title", "description")
    list_filter = ("course",)
    autocomplete_fields = ("course",)
    list_select_related = ("course",)
    ordering = ("course", "order")


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("topic_title", "topic_id", "module", "topic_type", "order",
                    "estimated_duration_in_mins", "created_at")
    search_fields = ("topic_title", "description")
    list_filter = ("topic_type", "module__course")
    autocomplete_fields = ("module",)
    list_select_related = ("module",)
    ordering = ("module", "order")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "username", "email", "phone_number",
                    "is_active", "otp_count",
                    "created_at")
    search_fields = ("username", "email", "phone_number")
    list_filter = ("is_active", "gender")
    ordering = ("created_at",)
    actions = [make_active, make_inactive, export_users_to_csv]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "course_status",
                    "user_learning_path__overall_percentage",
                    "created_at")
    search_fields = ("user__username", "course__title")
    list_filter = ("course_status",)
    autocomplete_fields = ("user", "course")
    list_select_related = ("user", "course")


@admin.register(CourseFeedback)
class CourseFeedbackAdmin(admin.ModelAdmin):
    form = CourseFeedbackForm
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
    list_display = ("user_learning_path_id", "user", "learning_path", "status",
                    "overall_percentage",
                    "created_at")
    search_fields = ("user__username", "learning_path__course__title")
    list_filter = ("status",)
    autocomplete_fields = ("user", "learning_path", "current_learning_unit")
    list_select_related = ("user", "learning_path", "current_learning_unit")


@admin.register(UserLearningUnit)
class UserLearningUnitAdmin(admin.ModelAdmin):
    list_display = ("id", "user_learning_path", "learning_unit", "status",
                    "percentage", "is_locked", "created_at")
    search_fields = ("user_learning_path__user__username",
                     "learning_unit__topic__topic_title")
    list_filter = ("status", "is_locked")
    autocomplete_fields = ("user_learning_path", "learning_unit")
    list_select_related = ("user_learning_path", "learning_unit")


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'estimated_duration_in_mins',
                    'created_at')
    list_filter = ('topic', 'created_at')
    search_fields = ('title', 'video_id')
    readonly_fields = ('video_id', 'created_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Video Information', {
            'fields': ('video_id', 'title', 'topic')
        }),
        ('Content', {
            'fields': ('video_url', 'estimated_duration_in_mins')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )

    # Optional: Show video count per topic
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('topic')


@admin.register(RateLimitEntry)
class RateLimitEntryAdmin(admin.ModelAdmin):
    list_display = ("identifier","last_requests","cooldown_until")