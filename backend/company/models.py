from django.db import models

class Company(models.Model):
    id = models.AutoField(primary_key=True)
    
    company_name = models.CharField(max_length=255)
    headquarters_location = models.CharField(max_length=255)
    year_established = models.IntegerField()
    company_size = models.IntegerField()
    revenue_last_year = models.CharField(max_length=100, blank=True)
    ownership_structure = models.CharField(max_length=100)
    years_of_experience = models.IntegerField()

    projects = models.JSONField(default=list) 

    certifications = models.JSONField(default=list)  

    skills = models.JSONField(default=list)  

    it = models.JSONField(default=list) 
    
    csr_policy = models.TextField(blank=True)
    environmental_commitment = models.TextField(blank=True)

    sector_of_activity = models.JSONField(default=list)  

    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    def check_password(self, raw_password):
        return self.password == raw_password

    def __str__(self):
        return self.company_name
