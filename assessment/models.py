# import uuid
# from django.db import models
#
#
#
# class QuestionBank(models.Model):
#     id=models.UUIDField(primary_key=True,default=uuid.uuid4)
#     name=models.CharField(max_length=50)
#     questions=models.ManyToManyField(Question,blank=True)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.name
#
# class QuestionSelectionConfig(models.Model):
#     id=models.UUIDField(primary_key=True,default=uuid.uuid4)
#     question_bank=models.ForeignKey(QuestionBank,on_delete=models.CASCADE)
#     number_of_questions=models.IntegerField()
#     algorithm=models.CharField(max_length=10) #DIFFICULTY BASED
#
#
# class QuestionBankQuestion(models.Model):
#     bank = models.ForeignKey('QuestionBank', on_delete=models.CASCADE)
#     question = models.ForeignKey('Question', on_delete=models.CASCADE)
#     position = models.PositiveIntegerField()
