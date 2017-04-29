from django.db import models
from django.contrib.auth.models import User

class Student (models.Model):
    index = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return str(self.index)
    

class Subject (models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class ClassRoom (models.Model):
    name = models.CharField(max_length=10)
    def __str__(self):
        return self.name
    
    
    
class Exam (models.Model):
    year = models.PositiveSmallIntegerField()
    term = models.PositiveSmallIntegerField()
    grade = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return "%d, %d, %d"%(self.year, self.term, self.grade)
    
    
class Mark (models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    mark = models.FloatField()
    
    def __str__(self):
        return "%d, %d, %d, %f"%(self.exam_id, self.student_id, self.subject_id, self.mark)


class Performance (models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classRoom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    
    total = models.FloatField()
    average = models.FloatField()
    zscore = models.FloatField()
    attendence = models.FloatField()
    rank = models.IntegerField()
    
    def __str__(self):
        return "%d, %d, %d, %d, %f, %f, %f, %d"%(self.exam_id, self.student_id, self.classRoom_id, self.total, self.average, self.zscore, self.attendence, self.rank)

class ROwner(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    classRoom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    
    def __str__(self):
        return "%d, %d, %d"%(self.exam_id, self.classRoom_id, self.user_id)

class Message(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parentName = models.CharField(max_length=50)
    email = models.EmailField()
    msg = models.TextField()
    count = models.PositiveIntegerField()
    datetime = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "%s - %s"%(self.parentName, self.msg)



    