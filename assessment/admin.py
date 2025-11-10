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



@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "assessment",
        "total_points",
        "status",
        "started_at",
        "completed_at",
    )

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

