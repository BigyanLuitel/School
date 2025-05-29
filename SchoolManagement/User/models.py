from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Role(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    STUDENT = "STUDENT", "Student"
    TEACHER = "TEACHER", "Teacher"


class User(AbstractUser):
    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)


class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=Role.STUDENT)


class Student(User):
    base_role = Role.STUDENT
    student = StudentManager()  # Note: fixed typo from 'object' to 'objects'

    class Meta:
        proxy = True

    def welcome(self):
        return "only for students"
    
@receiver(post_save, sender=Student)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.role == Role.STUDENT:
        StudentProfile.objects.create(user=instance)
        
    
    
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Student_id= models.IntegerField(null=True, blank=True)
class TeacherManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=Role.TEACHER)


class Teacher(User):
    base_role = Role.TEACHER
    teacher = TeacherManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "only for Teachers"
