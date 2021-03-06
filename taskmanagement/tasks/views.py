from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from projects.models import ProjectModel
from user_auth.models import *
from drf_yasg.utils import swagger_auto_schema
from user_auth.authentication import Authentication

# Create your views here.


@swagger_auto_schema(method='POST', request_body=AddTaskSerializer)
@api_view(["POST"])
def addnewtask(request):
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = AddTaskSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            project_id = serializer.data["project_id"]
            name = serializer.data["name"]
            comment = serializer.data["comment"]
            description = serializer.data["description"]
            is_private = serializer.data["is_private"]
            priority = serializer.data["priority"]
            reviewer_id = serializer.data["reviewer_id"]
            assignee_id = serializer.data["assignee_id"]
            tag_id = serializer.data["tag_id"]
            start_date = serializer.data["start_date"]
            end_date = serializer.data["end_date"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response({"successs" : False,"message":"User does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if project_id != "":
                 project = ProjectModel.objects.filter(id=project_id).first()
                 if not project:
                    return Response({"successs" : False,"message":"Project does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            taskdata = TaskModel.objects.filter(project_id=project_id,name=name).first()
            if taskdata:
                    return Response({"successs" : False,"message":"Task with same name exists in this project"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if(assignee_id != ""):
                assignee = UserModel.objects.filter(id=assignee_id).first()
                if not assignee:
                   return Response({"successs" : False,"message":"Assignee Id does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)    
            if(reviewer_id != ""):
                reviewer = UserModel.objects.filter(id=reviewer_id).first()
                if not reviewer:
                   return Response({"successs" : False,"message":"Reviewer Id does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if reviewer_id == assignee_id is not "":
                return Response({"successs" : False,"message":"Reviewer and assignee cannot be assigned to same project"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            taskStatusData = TaskStatusModel.objects.filter(task_status="Pending").first()
            task_status_id = ""
            if taskStatusData:
                task_status_id = taskStatusData.id
            new_task = TaskModel.objects.create(user_id=user_id,project_id=project_id,
            name=name,comment=comment,task_status=task_status_id,description=description,is_private=is_private,priority=priority,reviewer_id=reviewer_id,assignee_id=assignee_id,
            tag_id=tag_id,start_date=start_date,end_date=end_date)
            new_task.save()
            taskdata = list(TaskModel.objects.values().filter(id=new_task.id))
            taskdata[0].pop("is_active")
            taskdata[0].pop("is_delete")
            return Response({"successs" : True,"data" : taskdata[0],"message":"Task added successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=UpdateTaskSerializer)
@api_view(["POST"])
def updatetask(request):
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = UpdateTaskSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            task_id = serializer.data["id"]
            project_id = serializer.data["project_id"]
            name = serializer.data["name"]
            comment = serializer.data["comment"]
            task_status = serializer.data["task_status"]
            description = serializer.data["description"]
            is_private = serializer.data["is_private"]
            priority = serializer.data["priority"]
            reviewer_id = serializer.data["reviewer_id"]
            assignee_id = serializer.data["assignee_id"]
            tag_id = serializer.data["tag_id"]
            start_date = serializer.data["start_date"]
            end_date = serializer.data["end_date"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response({"successs" : False,"message":"User does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if(project_id != ""):
               projectdata = ProjectModel.objects.filter(id=project_id).first()
               if not projectdata:
                return Response({"successs" : False,"message":"Project id does not exists or is invalid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            taskdata = TaskModel.objects.filter(id=task_id).first()
            if not taskdata:
                return Response({"successs" : False,"message":"Task id does not exists or is invalid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if(assignee_id != ""):
                assignee = UserModel.objects.filter(id=assignee_id).first()
                if not assignee:
                   return Response({"successs" : False,"message":"Assignee Id does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)    
            if(reviewer_id != ""):
                reviewer = UserModel.objects.filter(id=reviewer_id).first()
                if not reviewer:
                   return Response({"successs" : False,"message":"Reviewer Id does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if reviewer_id == assignee_id != "":
                return Response({"successs" : False,"message":"Reviewer and assignee cannot be assigned to same project"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            task = TaskModel.objects.filter(id=task_id).first()
            task.name = name
            task.comment = comment
            task.task_status = task_status
            task.description = description
            task.is_private = is_private
            task.priority = priority
            task.tag_id = tag_id
            task.reviewer_id = reviewer_id
            task.assignee_id = assignee_id
            task.start_date = start_date
            task.end_date = end_date
            task.save()
            taskdata=list(TaskModel.objects.values().filter(id=task.id))
            taskdata[0].pop("is_active")
            taskdata[0].pop("is_delete")
            return Response({"successs" : True,"data" : taskdata[0],"message":"Task details updated successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=DeleteTaskSerializer)
@api_view(["POST"])
def deletetask(request):
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = DeleteTaskSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            task_id = serializer.data["id"]
            task = TaskModel.objects.filter(id=task_id).first()
            if not UserModel.objects.filter(id=user_id).first():
                return Response({"successs" : False,"message":"Account does not exists"}, status=status.HTTP_201_CREATED)
            if not task:
                return Response({"successs" : False,"message":"Task does not exists"}, status=status.HTTP_201_CREATED)
            TaskModel.objects.filter(id=task_id).delete()
            return Response({"success" : True,"message":"Task deleted successfully"}, status=status.HTTP_200_OK)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=GetTaskSerializer)
@api_view(["POST"])
def gettask(request):
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = GetTaskSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            project_id = serializer.data["project_id"]
            task_id = serializer.data["id"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response({"successs" : False,"message":"User does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if(project_id != ""):
                project = ProjectModel.objects.filter(id=project_id).first()
                if not project:
                 return Response({"successs" : False,"message":"Project id is invalid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    taskdata = TaskModel.objects.filter(id=task_id,project_id=project_id).first()
                    if not taskdata:
                      return Response({"successs" : False,"message":"Task does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    else:
                      taskdata=list(TaskModel.objects.values().filter(id=task_id,project_id=project_id))
                      taskdata[0].pop("is_active")
                      taskdata[0].pop("is_delete")
                      return Response({"successs" : True,"data" : taskdata,"message":"Task details fetched successfully"}, status=status.HTTP_201_CREATED)
            elif(task_id!=None):
                taskdata = TaskModel.objects.filter(id=task_id).first()
                if not taskdata:
                      return Response({"successs" : False,"message":"Task does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                      taskdata=list(TaskModel.objects.values().filter(id=task_id))
                      if(taskdata[0]["project_id"]!=""):
                          return Response({"successs" : True,"message":"This task is binded with project id"}, status=status.HTTP_201_CREATED)
                      taskdata[0].pop("is_active")
                      taskdata[0].pop("is_delete")
                      return Response({"successs" : True,"data" : taskdata[0],"message":"Task details fetched successfully"}, status=status.HTTP_201_CREATED)
            else:
                 taskdata=list(TaskModel.objects.values().filter(user_id=user_id))
                 if(len(taskdata)==0):
                     return Response({"successs" : True,"data" : taskdata,"message":"No task found"}, status=status.HTTP_201_CREATED)
                 if(len(taskdata)==1):
                    taskdata[0].pop("is_active")
                    taskdata[0].pop("is_delete")
                    return Response({"successs" : True,"data" : taskdata[0],"message":"Task details fetched successfully"}, status=status.HTTP_201_CREATED)
                 for i in range(0,len(taskdata)):
                    taskdata[i].pop("is_active")
                    taskdata[i].pop("is_delete")
                 return Response({"successs" : True,"data" : taskdata,"message":"Task details fetched successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=AddTaskStatusSerializer)
@api_view(["POST"])
def addtaskstatus(request):
    try:
        data = request.data
        serializer = AddTaskStatusSerializer(data=data)
        if serializer.is_valid():
            task_status = serializer.data["task_status"]
            statusdata = TaskStatusModel.objects.filter(task_status=task_status).first()
            if statusdata:
                return Response({"successs" : False,"message":"Task status already exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            new_task_status = TaskStatusModel.objects.create(task_status=task_status)
            new_task_status.save()
            taskstatusdata = list(TaskStatusModel.objects.values().filter(id=new_task_status.id))
            taskstatusdata[0].pop("is_active")
            taskstatusdata[0].pop("is_delete")
            return Response({"successs" : True,"data" : taskstatusdata[0],"message":"Task status added successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=GetTaskStatusSerializer)
@api_view(["POST"])
def gettaskstatus(request):
    try:
        data = request.data
        serializer = GetTaskStatusSerializer(data=data)
        if serializer.is_valid():
            task_status_id = serializer.data["id"]
            if(task_status_id==None):
                taskstatusdata=list(TaskStatusModel.objects.values())
                if(len(taskstatusdata)==0):
                     return Response({"successs" : True,"data" : taskstatusdata,"message":"No task status found"}, status=status.HTTP_201_CREATED)
                if(len(taskstatusdata)==1):
                    taskstatusdata[0].pop("is_active")
                    taskstatusdata[0].pop("is_delete")
                    return Response({"successs" : True,"data" : taskstatusdata[0],"message":"Task status details fetched successfully"}, status=status.HTTP_201_CREATED)
                for i in range(0,len(taskstatusdata)):
                    taskstatusdata[i].pop("is_active")
                    taskstatusdata[i].pop("is_delete")
                return Response({"successs" : True,"data" : taskstatusdata,"message":"Task status details fetched successfully"}, status=status.HTTP_201_CREATED)
            taskstatusdata = TaskStatusModel.objects.filter(id=task_status_id).first()
            if not taskstatusdata:
                return Response({"successs" : False,"message":"Task status id does not exists or is invalid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                taskstatusdata=list(TaskStatusModel.objects.values().filter(id=task_status_id))
                taskstatusdata[0].pop("is_active")
                taskstatusdata[0].pop("is_delete")
                return Response({"successs" : True,"data" : taskstatusdata[0],"message":"Task status details fetched successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=UpdateTaskStatusSerializer)
@api_view(["POST"])
def updatetaskstatus(request):
    try:
        data = request.data
        serializer = UpdateTaskStatusSerializer(data=data)
        if serializer.is_valid():
            task_status_id = serializer.data["id"]
            task_status = serializer.data["task_status"]
            if(task_status_id != ""):
               taskstatusdata = TaskStatusModel.objects.filter(id=task_status_id).first()
               if not taskstatusdata:
                return Response({"successs" : False,"message":"Task status id does not exists or is invalid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
               if(taskstatusdata.task_status == task_status):
                       return Response({"successs" : False,"message":f"The task name {task_status} already exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
               taskstatusdata.task_status = task_status
               taskstatusdata.save()
               taskstatusdata=list(TaskStatusModel.objects.values().filter(id=taskstatusdata.id))
               taskstatusdata[0].pop("is_active")
               taskstatusdata[0].pop("is_delete")
               return Response({"successs" : True,"data" : taskstatusdata[0],"message":"Task status updated successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"successs" : False,"message":"Task status id param cannot be empty"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=DeleteTaskStatusSerializer)
@api_view(["POST"])
def deletetaskstatus(request):
    try:
        data = request.data
        serializer = DeleteTaskStatusSerializer(data=data)
        if serializer.is_valid():
            task_status_id = serializer.data["id"]
            if not TaskStatusModel.objects.filter(id=task_status_id).first():
                return Response({"successs" : False,"message":"Task status id does not exists"}, status=status.HTTP_201_CREATED)
            TaskStatusModel.objects.filter(id=task_status_id).delete()
            return Response({"success" : True,"message":"Task status deleted successfully"}, status=status.HTTP_200_OK)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)