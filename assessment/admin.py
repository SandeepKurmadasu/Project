from django.contrib import admin
from .models import Assessment, Attempt, AssessmentAttemptQuestionSubmission, Question, QuestionBank, \
    QuestionBankQuestion


# class AssessmentAttemptQuestionSubmissionInline(admin.TabularInline):
#     model = AssessmentAttemptQuestionSubmission
#     extra = 0
#     readonly_fields = ("created_at",)
#     autocomplete_fields = ("question",)
#     list_select_related = ("question",)
#     can_delete = True
#     show_change_link = True


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "assessment_id",
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

    # inlines = [AssessmentAttemptQuestionSubmissionInline]


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
    list_display = ("question_id", "question_text", "question_type", "difficulty",)


@admin.register(QuestionBank)
class QuestionBankAdmin(admin.ModelAdmin):
    list_display = (
        "bank_id", "title", "assessment_id", "created_at", "updated_at"
    )

@admin.register(QuestionBankQuestion)
class QuestionBankQuestionAdmin(admin.ModelAdmin):
    list_display = (
        "bank_id", "question_id", "order", "bank_name", "question_text"
    )

    def bank_id(self, obj):
        return obj.question_bank.bank_id

    def bank_name(self, obj):
        return obj.question_bank.title

    def question_text(self, obj):
        return obj.question.question_text

    def delete_model(self, request, obj):
        bank_id = obj.question_bank_id
        super().delete_model(request, obj)
        self.normalize_order(bank_id)

    def delete_queryset(self, request, queryset):
        bank_ids = set(str(q.question_bank_id) for q in queryset)
        super().delete_queryset(request, queryset)
        for bank_id in bank_ids:
            self.normalize_order(bank_id)

    @staticmethod
    def normalize_order(bank_id):
        qs = QuestionBankQuestion.objects.filter(
            question_bank_id=bank_id
        ).order_by("order")

        for i, obj in enumerate(qs, start=1):
            obj.order = i

        QuestionBankQuestion.objects.bulk_update(qs, ["order"])
