from asyncore import read
from distutils import core
from email.policy import default
from statistics import mode
from urllib import request
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField
from django.core.validators import RegexValidator



class MyUser(AbstractUser):    
    contactPerson = models.CharField(max_length=150,default='',blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=True,max_length=16)
    contactEmail = models.EmailField(default='')
    contactAddress = models.TextField(default='')
    CLIENT = 1
    ROLE_CHOICES = (
        (1, 'Client'),
        (2, 'Team_Member'),
    )
    
    user_type = models.PositiveSmallIntegerField(choices=ROLE_CHOICES,default='1')

    
    def __str__(self):
        return self.username


class CreateProject(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name='projects')

    STATUS_CHOICE = (
        (1,'Not_Started'),
        (2,'In_Progress'),
        (3,'Completed'),
    )

    project_status = models.PositiveSmallIntegerField(choices=STATUS_CHOICE,default='1')

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name='team')
    team_project = models.ManyToManyField(CreateProject,related_name='teams',blank=True)
    
    def __str__(self):
        return self.name


class Tasks(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name='tasks')
    tasks_project = models.ForeignKey(CreateProject,on_delete=models.CASCADE,related_name='tasks')

    STATUS_CHOICE = (
        (1,'Not_Started'),
        (2,'In_Progress'),
        (3,'Completed'),
    )

    task_status = models.PositiveSmallIntegerField(choices=STATUS_CHOICE,default='1')

    
    def __str__(self):
        return self.name


