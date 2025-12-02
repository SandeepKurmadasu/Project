import json
from django.core.management.base import BaseCommand
from assessment.models import (
    Assessment,
    QuestionBank,
    Question,
    QuestionBankQuestion
)


class Command(BaseCommand):
    help = "Load assessment, question bank & questions from custom JSON"

    def handle(self, *args, **kwargs):
        with open("assessments.json", "r") as f:
            data = json.load(f)

        for block in data:

            # -------------------------
            # 1. Create Assessment
            # -------------------------
            a = block["assessment"]

            assessment = Assessment.objects.create(
                assessment_id=a["assessment_id"],
                topic_id=a["topic_id"],
                title=a["title"],
                icon=a["icon"],
                assessment_type=a["assessment_type"],
                description=a["description"],
                no_of_questions=a["no_of_questions"],
                pass_marks=a["pass_marks"],
                marks=a["marks"],
                pass_percentage=a["pass_percentage"],
                easy_count=a["easy_count"],
                medium_count=a["medium_count"],
                hard_count=a["hard_count"],
                attempts_limit=a["attempts_limit"],
                estimated_duration_in_minutes=a["estimated_duration_in_minutes"]
            )

            # -------------------------
            # 2. Create Question Bank
            # -------------------------
            qb = block["question_bank"]

            question_bank = QuestionBank.objects.create(
                bank_id=qb["bank_id"],
                assessment=assessment,
                title=qb["title"]
            )

            # -------------------------
            # 3. Create Questions
            # -------------------------
            for q in block["questions"]:
                Question.objects.create(
                    question_id=q["question_id"],
                    question_text=q["question_text"],
                    question_type=q["question_type"],
                    difficulty=q["difficulty"],
                    options=q["options"],
                    correct_answer=q["correct_answer"]
                )

            # -------------------------
            # 4. Create Bank → Question Mappings
            # -------------------------
            for m in block["question_bank_mappings"]:
                QuestionBankQuestion.objects.create(
                    question_bank=question_bank,
                    question_id=m["question_id"],
                    order=m["order"]
                )

        self.stdout.write(self.style.SUCCESS("SUCCESS: All assessment data loaded!"))