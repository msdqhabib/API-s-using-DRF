from asyncio import Task, tasks
from asyncore import read
from dataclasses import field
import email
from email.policy import default
from pyexpat import model
from rest_framework import serializers
from django.contrib.auth import get_user_model
from App.models import MyUser,CreateProject,Team,Tasks
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken



User = get_user_model()

class RegisterUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type':'password'},write_only=True)
    contactPerson = serializers.CharField()
    phone_number = serializers.CharField()
    contactEmail = serializers.EmailField()
    contactAddress = serializers.CharField()
    projects = serializers.PrimaryKeyRelatedField(read_only=True,source='owner.username')
    team = serializers.PrimaryKeyRelatedField(read_only=True,source='owner.username',allow_null=True)
    tasks = serializers.PrimaryKeyRelatedField(read_only=True,source='owner.username',allow_null=True)

    def create(self, validated_data):
        contactPerson = self.validated_data['contactPerson']
        phone_number = self.validated_data['phone_number']
        contactEmail = self.validated_data['contactEmail']
        contactAddress = self.validated_data['contactAddress']
        
        
        username = User.objects.filter(username=self.validated_data['username'])
        if username.exists():
            raise serializers.ValidationError("username already existed")

        email = self.validated_data['email']
        username = self.validated_data['username']
        
        #set_password will convert plain password into hashes
        validated_data['password'] = make_password(validated_data['password'])        
       
        return User.objects.create(**validated_data) 

    
      

    def update(self, instance, validated_data):
        instance.contactPerson = validated_data.get('contactPerson',instance.contactPerson)
        instance.phone_number = validated_data.get('phone_number',instance.phone_number)
        instance.contactEmail = validated_data.get('contactEmail',instance.contactEmail)
        instance.contactAddress = validated_data.get('contactAddress',instance.contactAddress)

        instance.email = validated_data.get('email',instance.email)
        instance.username = validated_data.get('username',instance.username)
        instance.save()
        return instance


class CreateProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    teams = serializers.StringRelatedField(required=False,many=True)
    tasks = serializers.PrimaryKeyRelatedField(read_only=True,source='tasks_project.name')
    
    class Meta:
        model = CreateProject
        fields = ['id','name','description','owner','project_status','teams','tasks']


class TeamClassField(serializers.StringRelatedField):
    
    def to_internal_value(self, value):
       sector_class = Team.objects.filter(name=value)
       return value


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)    
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Team
        fields = ['id','name','description','owner','team_project']    
        depth = 1



class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)    
    owner = serializers.ReadOnlyField(source='owner.username')
    tasks_project = serializers.ReadOnlyField(source='tasks_project.name')
    class Meta:
        model = Tasks
        fields = ['id','name','description','owner','tasks_project','task_status']    

    def create(self, validated_data):
        name = self.validated_data['name']
        description = self.validated_data['description']
        tasks = Tasks.objects.create(**validated_data) 
        tasks.save()
        return tasks


    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.description = validated_data.get('description',instance.description)
        instance.task_status = validated_data.get('task_status',instance.task_status)
        instance.save()
        return instance
