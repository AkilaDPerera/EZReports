from django.contrib import admin
from Reports.models import ClassRoom, Exam, Mark, Performance, Student, Subject, ROwner, Message

# Register your models here.
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(ClassRoom)
admin.site.register(Exam)
admin.site.register(Mark)
admin.site.register(Performance)
admin.site.register(ROwner)
admin.site.register(Message)

