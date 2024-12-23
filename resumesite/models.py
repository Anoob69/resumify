from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    # Basic User Information
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resumes")
    name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)
    address = models.TextField()

    # Skills
    skills_1 = models.CharField(max_length=100, blank=True, null=True)
    skills_2 = models.CharField(max_length=100, blank=True, null=True)
    skills_3 = models.CharField(max_length=100, blank=True, null=True)
    skills_4 = models.CharField(max_length=100, blank=True, null=True)

    # Work Experience 1
    experience_1_title = models.CharField(max_length=255)
    experience_1_start = models.DateField(null=True, blank=True)  # Start date for Experience 1
    experience_1_end = models.DateField(null=True, blank=True)    # End date for Experience 1
    experience_1_desc = models.TextField()

    # Work Experience 2 (Optional)
    experience_2_title = models.CharField(max_length=255, blank=True, null=True)
    experience_2_start = models.DateField(null=True, blank=True)  # Start date for Experience 2
    experience_2_end = models.DateField(null=True, blank=True)    # End date for Experience 2
    experience_2_desc = models.TextField(blank=True, null=True)

    # Education 1
    education_1 = models.CharField(max_length=255)
    education_1_start = models.DateField(null=True, blank=True)  # Start date for Education 1
    education_1_end = models.DateField(null=True, blank=True)    # End date for Education 1
    education1_score = models.PositiveIntegerField()

    # Education 2 (Optional)
    education_2 = models.CharField(max_length=255, blank=True, null=True)
    education_2_start = models.DateField(null=True, blank=True)  # Start date for Education 2
    education_2_end = models.DateField(null=True, blank=True)    # End date for Education 2
    education2_score = models.PositiveIntegerField(blank=True, null=True)

    # PDF File
    pdf_file = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.name
