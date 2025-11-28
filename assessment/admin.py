from django.contrib import admin
from .models import Assessment, Attempt, AssessmentAttemptQuestionSubmission, \
    Question, QuestionBank, QuestionBankQuestion


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = (
        "assessment_id",
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
        "attempt_id",
        "user",
        "assessment",
        "total_points",
        "status",
        "started_at",
        "completed_at",
        "question_ids"
    )


@admin.register(AssessmentAttemptQuestionSubmission)
class AssessmentAttemptQuestionSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "attempt",
        "question",
        "selected_option",
        "is_response_correct",
        "created_at",
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_id", "question_text", "question_type",
                    "difficulty", "options", "correct_answer")


@admin.register(QuestionBank)
class QuestionBankAdmin(admin.ModelAdmin):
    list_display = (
        "bank_id", "title", "assessment_id", "created_at", "updated_at"
    )


@admin.register(QuestionBankQuestion)
class QuestionBankQuestionAdmin(admin.ModelAdmin):
    list_display = (
        "bank_id", "question_id", "order", "bank_name"
    )

    def bank_id(self, obj):
        return obj.question_bank.bank_id

    def bank_name(self, obj):
        return obj.question_bank.title
