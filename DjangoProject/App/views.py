from asyncio import Task
from os import stat_result
from unicodedata import name
from urllib import request, response
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from App.serializers import RegisterUserSerializer,CreateProjectSerializer,TeamSerializer,TaskSerializer
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from rest_framework import status
from App import models
from rest_framework.authtoken.models import Token
from App.models import MyUser,CreateProject,Team,Tasks
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken




@swagger_auto_schema(method='POST', request_body=RegisterUserSerializer,
                     operation_summary="Clients will be created",operation_description="Register Clients")
@api_view(['POST'])
def register_users(request):
    

    if request.method == 'POST':
        seriaizer = RegisterUserSerializer(data=request.data)
        data = {}
        if seriaizer.is_valid():
            user = seriaizer.save(user_type=1)
            refresh = RefreshToken.for_user(user)
            res = {
              'refresh': str(refresh),
              'access': str(refresh.access_token),
    }

            return Response(res)
        else:
            return Response(seriaizer.errors)

@swagger_auto_schema(method='POST', request_body=RegisterUserSerializer,
                     operation_description="user type member",operation_summary="member which will be created by client")
@api_view(['POST'])
def register_member(request):
    if request.method == 'POST':
        seriaizer = RegisterUserSerializer(data=request.data)
        if seriaizer.is_valid():
            user = seriaizer.save(user_type=2)
            refresh = RefreshToken.for_user(user)
            res = {
              'refresh': str(refresh),
              'access': str(refresh.access_token),
    }
            return Response(res)
        else:
            return Response(seriaizer.errors)



@api_view(['POST'])
def logout_user(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)


@swagger_auto_schema(method='PUT', request_body=RegisterUserSerializer
                        ,operation_description="Profile details of logged in user",operation_summary="users profile")
@api_view(['GET','PUT'])
def user_profile(request):
    if request.method == 'GET':
        current_user = MyUser.objects.get(pk=request.user.pk)
        print(current_user)
        serializers = RegisterUserSerializer(current_user)
        return Response(serializers.data)


    if request.method == 'PUT':
        current_user = MyUser.objects.get(pk=request.user.pk)
        serializers = RegisterUserSerializer(current_user,data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)



# @permission_classes(['IsAuthenticated'])
@swagger_auto_schema(method='POST', request_body=CreateProjectSerializer,
                                    operation_summary="All Projects",operation_description="All the projects created by logged in user")
@api_view(['GET','POST'])
  
def client_project(request):
    if request.method == 'GET':
        members = MyUser.objects.filter(user_type=2)
        # current_user = MyUser.objects.get(pk=request.user.pk)
        projects = CreateProject.objects.all().filter(owner=request.user)
        serializers = CreateProjectSerializer(projects,many=True)
        return Response(serializers.data)
 
    

    if request.method == 'POST':
        data = request.data
        new_project = CreateProject.objects.create(name = data["name"],description = data["description"],owner=request.user)
        new_project.save()

        for teams in data["teams"]:
            team_obj = Team.objects.get(name=projects["name"])
            new_project.team_project.add(team_obj)

        # return new_project
        serializers = CreateProjectSerializer(new_project)
        return Response(serializers.data,status=status.HTTP_200_OK)

# @permission_classes(['IsAuthenticated'])
@swagger_auto_schema(method='PUT', request_body=CreateProjectSerializer,
                      operation_description="project details by id",operation_summary="all the details of individual project object")
@api_view(['GET','PUT','DELETE'])
def project_detail(request,pk):
    if request.method == 'GET':
      projects = CreateProject.objects.get(pk=pk)
      serializers = CreateProjectSerializer(projects)
      return Response(serializers.data)
        
    if request.method == 'PUT':
        project_obj = CreateProject.objects.get(pk=pk)
        data = request.data

        for teams in data["teams"]:
            project_obj.teams.clear()
            team_obj = Team.objects.get(name=projects["name"])

            project_obj.teams.add(team_obj)

        project_obj.name = data["name"]
        project_obj.description = data["description"]
        project_obj.owner = request.user

        project_obj.save()

        serializers = TeamSerializer(project_obj)
        return Response(serializers.data)


    if request.method == 'DELETE':
        projects = CreateProject.objects.get(pk=pk)
        projects.delete()
        return Response(status=status.HTTP_200_OK)



@permission_classes(['IsAuthenticated'])
@swagger_auto_schema(method='POST', request_body=TeamSerializer
                        ,operation_description="Teams Lists",operation_summary="Team list which is created by logged in user")
@api_view(['GET','POST'])
def general_team(request):
    if request.method == 'GET':
        teams = Team.objects.all().filter(owner=request.user)
        serializers = TeamSerializer(teams,many=True)
        return Response(serializers.data)
 
    if request.method == 'POST':
        data = request.data
        new_team = Team.objects.create(name = data["name"],description = data["description"],owner=request.user)
        new_team.save()

        for projects in data["team_project"]:
            project_obj = CreateProject.objects.get(name=projects["name"])
            new_team.team_project.add(project_obj)


        serializers = TeamSerializer(new_team)
        return Response(serializers.data,status=status.HTTP_200_OK)


@permission_classes(['IsAuthenticated'])
@swagger_auto_schema(method='PUT', request_body=TeamSerializer
                        ,operation_description="Individual team object",operation_summary="Individual team details by id")
@api_view(['GET','PUT','DELETE'])
def team_detail(request,pk):
    if request.method == 'GET':
      teams = Team.objects.get(pk=pk)
      serializers = TeamSerializer(teams)
      return Response(serializers.data)
        
    if request.method == 'PUT':
        teams_obj = Team.objects.get(pk=pk)
        data = request.data

        for projects in data["team_project"]:
            teams_obj.team_project.clear()
            project_obj = CreateProject.objects.get(name=projects["name"])
            teams_obj.team_project.add(project_obj)
            
        teams_obj.name = data["name"]
        teams_obj.description = data["description"]
        teams_obj.owner = request.user

        teams_obj.save()

        serializers = TeamSerializer(teams_obj)
        return Response(serializers.data)
       

    if request.method == 'DELETE':
        projects = Team.objects.get(pk=pk)
        projects.delete()
        return Response(status=status.HTTP_200_OK)



@swagger_auto_schema(method='POST', request_body=TaskSerializer
                        ,operation_description="Tasks Lists",operation_summary="Tasks list which is created by logged in user")
@permission_classes(['IsAuthenticated'])
@api_view(['GET','POST'])
def project_task(request,pk):
    if request.method == 'GET':
        projects = CreateProject.objects.get(pk=pk)
        tasks = Tasks.objects.all().filter(owner=request.user,tasks_project=projects)
        serializers = TaskSerializer(tasks,many=True)
        return Response(serializers.data)
 
    if request.method == 'POST':
        projects = CreateProject.objects.get(pk=pk)
        print(projects)
        serializers = TaskSerializer(data=request.data)
        if serializers.is_valid():
              serializers.save(owner=request.user,tasks_project=projects)
              return Response(serializers.data,status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors)


@swagger_auto_schema(method='PUT', request_body=TaskSerializer
                        ,operation_description="Individual Task detail",operation_summary="Individual task details by id")   
@permission_classes(['IsAuthenticated'])
@api_view(['GET','PUT','DELETE'])
def task_detail(request,pk):
    if request.method == 'GET':
      tasks = Tasks.objects.get(pk=pk)
      serializers = TaskSerializer(tasks)
      return Response(serializers.data)
        
    if request.method == 'PUT':
        tasks = Tasks.objects.get(pk=pk)
        serializers = TaskSerializer(tasks,data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)


    if request.method == 'DELETE':
        projects = Tasks.objects.get(pk=pk)
        projects.delete()
        return Response(status=status.HTTP_200_OK)


