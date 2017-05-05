'''
Created on Apr 23, 2017

@author: Akila
'''
from Reports.models import Student, Subject, ClassRoom, Exam, Mark, Performance, ROwner
from django.contrib.auth import get_user_model

from rest_framework import serializers

class StudentSerializer(serializers.Serializer):
    index = serializers.IntegerField()
    name = serializers.CharField()
        
    def create(self, validated_data): #POST Request action
        try:
            student = Student.objects.get_or_create(index=validated_data["index"], name=validated_data["name"])[0]
            student.save() 
        except:
            student = Student.objects.get_or_create(index=validated_data["index"])[0]
            student.name = validated_data["name"]
            student.save() 
        return student
    
class SubjectSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
        
    def create(self, validated_data):
        subject = Subject.objects.get_or_create(name = validated_data["name"])[0]
        subject.save() 
        return subject

class ClassRoomSerializer (serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    
    def create(self, validated_data):
        classRoom = ClassRoom.objects.get_or_create(name = validated_data["name"])[0]
        classRoom.save() 
        return classRoom

class ExamSerializer (serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    year = serializers.IntegerField()
    term = serializers.IntegerField()
    grade = serializers.IntegerField()
    
    def create(self, validated_data):
        exam = Exam.objects.get_or_create(year = validated_data["year"], term = validated_data["term"], grade = validated_data["grade"])[0]
        exam.save() 
        return exam

class MarkSerializer (serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    exam_id = serializers.IntegerField()
    student_id = serializers.IntegerField()
    subject_id = serializers.IntegerField()
    mark = serializers.FloatField()
    
    def create(self, validated_data):
        qs = Mark.objects.filter(exam_id=validated_data["exam_id"], student_id=validated_data["student_id"], subject_id=validated_data["subject_id"])
        if (qs.count()==0):
            #create new object
            try:
                mark = Mark.objects.get_or_create(exam_id=validated_data["exam_id"], student_id=validated_data["student_id"], subject_id=validated_data["subject_id"], mark=validated_data["mark"])[0]
                mark.save()
                return mark
            except:
                mark = Mark()
                mark.id = -1
                mark.exam_id = -1
                mark.student_id = -1
                mark.subject_id = -1
                mark.mark = -1
                return mark
        else:
            #update the existing
            mark = Mark.objects.get_or_create(exam_id=validated_data["exam_id"], student_id=validated_data["student_id"], subject_id=validated_data["subject_id"])[0]
            mark.mark = validated_data["mark"]
            mark.save()
            return mark


class PerformanceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    exam_id = serializers.IntegerField()
    student_id = serializers.IntegerField()
    classRoom_id = serializers.IntegerField()
    
    total = serializers.FloatField()
    average = serializers.FloatField()
    zscore = serializers.FloatField()
    attendence = serializers.FloatField()
    rank = serializers.IntegerField()

    def create(self, validated_data):
        qs = Performance.objects.filter(exam_id=validated_data["exam_id"], classRoom_id=validated_data["classRoom_id"], student_id=validated_data["student_id"])
        if (qs.count()==0):
            #create new object
            try:
                perf = Performance.objects.get_or_create(exam_id=validated_data["exam_id"], classRoom_id=validated_data["classRoom_id"], student_id=validated_data["student_id"],
                                                         total = validated_data["total"],
                                                         average = validated_data["average"],
                                                         zscore = validated_data["zscore"],
                                                         attendence = validated_data["attendence"],
                                                         rank = validated_data["rank"])[0]                          
                perf.save()
                return perf
            except:
                perf = Performance()
                perf.id = -1
                perf.exam_id = -1
                perf.student_id = -1
                perf.classRoom_id = -1
                perf.total = -1
                perf.average = -1
                perf.zscore = -1
                perf.attendence = -1
                perf.rank = -1
                return perf
        else:
            #update the existing
            perf = Performance.objects.get_or_create(exam_id=validated_data["exam_id"], classRoom_id=validated_data["classRoom_id"], student_id=validated_data["student_id"])[0]
            perf.total = validated_data["total"]
            perf.average = validated_data["average"]
            perf.zscore = validated_data["zscore"]
            perf.attendence = validated_data["attendence"]
            perf.rank = validated_data["rank"]
            perf.save()
            return perf
            
class UserSerializer(serializers.ModelSerializer):
    UserModel = get_user_model()
    
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        
        
    def create(self, validated_data):

        user = self.UserModel.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        
        user.set_password(validated_data['password'])
        user.save()

        return user

class ROwnerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    exam_id = serializers.IntegerField()
    classRoom_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    date = serializers.DateField(read_only=True)
    
    def create(self, validated_data):
        qs = ROwner.objects.filter(exam_id=validated_data["exam_id"], classRoom_id=validated_data["classRoom_id"])
        if (qs.count()==0):
            #create new object
            try:
                rowner = ROwner.objects.get_or_create(exam_id=validated_data["exam_id"], classRoom_id=validated_data["classRoom_id"], user_id = validated_data["user_id"])[0]
                rowner.save()
                return rowner
            except:
                rowner = ROwner()
                rowner.id = -1
                rowner.exam_id = -1
                rowner.classRoom_id = -1
                rowner.user_id = -1
                return rowner
        else:
            #update the existing
            rowner = ROwner.objects.get_or_create(exam_id=validated_data["exam_id"], classRoom_id=validated_data["classRoom_id"])[0]
            rowner.user_id = validated_data["user_id"]
            rowner.save()
            return rowner
    
class MessageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    student_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    parentName = serializers.CharField()
    email = serializers.EmailField()
    msg = serializers.CharField()
    count = serializers.IntegerField()
    datetime = serializers.DateTimeField(read_only=True)
    
    
    
    
    
