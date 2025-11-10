from django.contrib import admin
from .models import Assessment, Attempt, AssessmentAttemptQuestionSubmission


class AssessmentAttemptQuestionSubmissionInline(admin.TabularInline):
    model = AssessmentAttemptQuestionSubmission
    extra = 0
    readonly_fields = ("created_at",)
    autocomplete_fields = ("question",)
    list_select_related = ("question",)
    can_delete = True
    show_change_link = True


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "assessment_type",
        "marks",
        "pass_marks",
        "estimated_duration_in_minutes",
        "attempts_limit",
        "created_at",
    )
    search_fields = ("title", "description")
    list_filter = ("assessment_type",)
    ordering = ("-created_at",)
    list_per_page = 20
    readonly_fields = ("created_at", "updated_at")


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "assessment",
        "total_points",
        "status",
        "created_at",
        "completed_at",
    )
    search_fields = ("user__username", "assessment__title")
    list_filter = ("status", "assessment__assessment_type")
    autocomplete_fields = ("user", "assessment")
    list_select_related = ("user", "assessment")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "completed_at")

    inlines = [AssessmentAttemptQuestionSubmissionInline]


@admin.register(AssessmentAttemptQuestionSubmission)
class AssessmentAttemptQuestionSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "attempt",
        "question",
        "selected_option",
        "is_response_correct",
        "created_at",
    )
    search_fields = ("attempt__user__username", "question__question_text")
    list_filter = ("is_response_correct",)
    autocomplete_fields = ("attempt", "question")
    list_select_related = ("attempt", "question")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
