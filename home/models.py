from django.db import models


# Create your models here.

class Student(models.Model):
    GRADE_CHOICES = (
        ('first', 'first'),
        ('second', 'second'),
        ('third', 'third'),
    )

    CLASS_NUMBER_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    )

    student_fullname = models.CharField(max_length=255)
    family_order = models.CharField(max_length=50)
    grade = models.CharField(max_length=50, choices=GRADE_CHOICES)
    class_number = models.CharField(max_length=50, choices=CLASS_NUMBER_CHOICES)
    health_status = models.TextField()
    father_fullname = models.CharField(max_length=50)
    mother_fullname = models.CharField(max_length=50)
    father_job = models.CharField(max_length=50)
    mother_job = models.CharField(max_length=50)
    father_phone_number = models.CharField(max_length=50)
    mother_phone_number = models.CharField(max_length=50)
    Insurance_type = models.CharField(max_length=50)

    def __str__(self):
        return self.student_fullname


class InfoPulse(models.Model):
    CATEGORY_CHOICES = (
        ("events", 'events'),
        ("celebrations", 'celebrations'),
        ("notices", 'notices'),
        ("ideas", 'ideas'),
    )

    title = models.CharField(max_length=255)
    # image = models.ImageField(upload_to='infopulse_images/')
    image = models.ImageField()
    date = models.DateField()
    body = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)

    def __str__(self):
        return self.title


class TeacherInfo(models.Model):
    name = models.CharField(max_length=255)
    # image = models.ImageField(upload_to='teacher_images/')
    image = models.ImageField(upload_to='media/')
    grade = models.CharField(max_length=50)
    classroom = models.CharField(max_length=50)
    position = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class TopStudent(models.Model):
    fullname = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    # image = models.ImageField(upload_to='student_images/')
    image = models.ImageField()
    grade = models.CharField(max_length=50)
    classroom = models.CharField(max_length=50)

    def __str__(self):
        return self.grade


class SchoolService(models.Model):
    fullname = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=15)
    neighbourhood = models.CharField(max_length=50)
    alley = models.CharField(max_length=50)
    street = models.CharField(max_length=50)

    def __str__(self):
        return self.neighbourhood


class CollaborationRequest(models.Model):
    parent_fullname = models.CharField(max_length=255)
    student_fullname = models.CharField(max_length=255)
    collaboration_type = models.CharField(max_length=100)
    field = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.collaboration_type
