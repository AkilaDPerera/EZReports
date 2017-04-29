from django.shortcuts import render, redirect
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import get_user_model
from django.utils.timezone import localtime 
from rest_framework import viewsets

from Reports.models import Student, Subject, ClassRoom, Exam, Mark, Performance, ROwner, Message
from Reports.serializers import StudentSerializer, SubjectSerializer, ClassRoomSerializer, ExamSerializer, MarkSerializer, PerformanceSerializer, UserSerializer, ROwnerSerializer, MessageSerializer
from Reports import emailClient

import datetime
import json

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    
class ClassRoomViewSet(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer
    
class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

class MarkViewSet(viewsets.ModelViewSet):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer

class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    
    def get_queryset(self):
        exam_id = self.request.query_params.get('exam_id', None)
        class_id = self.request.query_params.get('classRoom_id', None)
        
        if (exam_id!=None and class_id!=None):
            #get the user
            perfs = Performance.objects.filter(exam_id=exam_id, classRoom_id=class_id)
            
            #password check
            if (perfs.exists()):
                perfs.delete()
                return None
        else:
            #no query
            return Performance.objects.all()

class ROwnerViewSet(viewsets.ModelViewSet):
    queryset = ROwner.objects.all()
    serializer_class = ROwnerSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    
    def get_queryset(self):
        #username & password query
        name = self.request.query_params.get('username', None)
        passw = self.request.query_params.get('password', None)
        
        if (name!=None and passw!=None):
            #get the user
            user = get_user_model().objects.filter(username=name)
            
            #password check
            if not(user.exists()):
                return None
            
            if (user[0].check_password(passw)):
                return user
            else:
                return None
        else:
            #no query
            return get_user_model().objects.all()

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

# Create your views here.
def home(request):
    return render(request, "Home/home.html")


def score(request):
    try:
        index = request.POST["index"]
    except:
        #redirect to the home page
        return redirect("home");
    else:
        #Whether the index exists in the DB
        try:
            student = Student.objects.get(index=index)
        except:
            #Student does not exist on the DB
            return render(request, 'Home/homeMSG.html', {"MSG":"Index number does not exist in the system."})
        else:
            #Student does exist
            #Gather the all information
            
            #Check whether there is any information requrding the student
            qs = Performance.objects.filter(student_id=index)
            if not(qs.exists()):
                return render(request, 'Home/homeMSG.html', {"MSG":"RESULT ARE NOT UPLAODED YET."}) 
            
            #There are valid info
            data_set = []
            for performance in qs:
                #try to create a large dict which contains all the data regarding single exam
                exam_dict = dict()

                #finding related subjects
                subjects = dict()
                marks = Mark.objects.filter(exam_id=performance.exam_id, student_id=index)
                s = [0, 1, 2, 3]
                #Get enlish value first
                subjects["subject1"] = ["English", 100]
                for i in [0, 1, 2, 3]:
                    print(marks[i].student_id==1)
                    
                    if (marks[i].student_id==1):
                        subjects["subject1"] = [Subject.objects.get(id=marks[0].subject_id).name, marks[i].mark]
                
                subjects["subject2"] = [Subject.objects.get(id=marks[s[0]].subject_id).name, marks[s[0]].mark]
                subjects["subject3"] = [Subject.objects.get(id=marks[s[1]].subject_id).name, marks[s[1]].mark]
                subjects["subject4"] = [Subject.objects.get(id=marks[s[2]].subject_id).name, marks[s[2]].mark]
                
                
                #Getting exam details
                exam = Exam.objects.get(id=performance.exam_id) #year, term, grade
                
                #Getting class
                classroom = ClassRoom.objects.get(id=performance.classRoom_id) #class
                
                #producer details
                producer = ROwner.objects.filter(exam_id=performance.exam_id, classRoom_id=performance.classRoom_id)[0] #user_id, date
                produce_by = get_user_model().objects.get(id=producer.user_id)
                
                #get messages
                msgs = []
                for mess in Message.objects.filter(student_id=index, user_id=producer.user_id):
                    time = mess.datetime
                    locTime = str(localtime(time).time())
                    locDate = str(localtime(time).date())
                    msgs.append({"date":time, "datetime": "%s  |  %s"%(locDate, locTime), "msg":mess.msg})
                sorted_msgs = sorted(msgs, key=lambda t:t["date"], reverse=True)   
                
                exam_dict["date"] = producer.date
                exam_dict["exam"] = exam
                exam_dict["class"] = classroom.name
                exam_dict["produced_by"] = "%s %s"%(produce_by.first_name, produce_by.last_name) 
                exam_dict["producer_id"] = producer.user_id
                exam_dict["student"] = student
                exam_dict["performance"] = performance
                exam_dict["subjects"] = subjects
                exam_dict["msgs"] = sorted_msgs
                
                data_set.append(exam_dict)
            
            #sort the list by date
            sorted_list = sorted(data_set, key=lambda t:t["date"], reverse=True)
            return render(request, "Home/score.html", {"data": sorted_list})
        
        
def send(request):
    data = request.POST
    
    #Check whether the max reached
    msgs = Message.objects.filter(student_id=data["student_id"], datetime__contains=datetime.date.today())

    if (msgs.count()>=3):
        return HttpResponseBadRequest()
    
    
    #update the db with message
    message = Message.objects.get_or_create(student_id=data["student_id"], user_id=data["user_id"], parentName=data["name"], email=data["email"], msg=data["msg"], count=1)[0];
    message.save()
    
    student = Student.objects.get(index=int(message.student_id))
    teacher = get_user_model().objects.get(id=message.user_id)
    
    #send the email to the teacher
    sub = "Inquiring about student(%s-%s) results"%(student.name, student.index)
    
    mail = """
    Hello %s,
    
    %s
    
    Thanks.
    Best regards,
    %s.
    %s
    
    PLEASE DO REPLY TO THE ABOVE EMAIL ADDRESS. PLEASE DO NOT REPLY TO THE EMAIL THAT YOU HAVE RECEIVED THIS MAIL.
    """%(teacher.first_name, message.msg, message.parentName, message.email)
    
    emailClient.send(teacher.email, sub, mail)
    
    time = message.datetime
    locTime = str(localtime(time).time())
    locDate = str(localtime(time).date())
    
    response = json.dumps([{"datetime": "%s  |  %s"%(locDate, locTime), "msg": message.msg}])
    
    return HttpResponse(response, content_type='application/json')

    
        
        
        
        
        
        
        
        
        
        
        
        
