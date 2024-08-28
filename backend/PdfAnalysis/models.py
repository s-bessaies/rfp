from django.db import models
from company.models import Company

class PDFAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
    description=models.TextField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    pdf_name = models.CharField(max_length=255)

    sector = models.TextField(blank=True, null=True)
    dates = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)

    minimum_experience = models.TextField(blank=True, null=True)
    required_certifications = models.TextField(blank=True, null=True)
    similar_project_references = models.TextField(blank=True, null=True)

    it_infrastructure = models.TextField(blank=True, null=True)
    network_infrastructure = models.TextField(blank=True, null=True)
    virtualization = models.TextField(blank=True, null=True)

    programming_languages = models.TextField(blank=True, null=True)
    cloud_computing_data_management_ai_skills = models.TextField(blank=True, null=True)
    cybersecurity_devops_big_data_skills = models.TextField(blank=True, null=True)
    iot_network_telecom_blockchain_skills = models.TextField(blank=True, null=True)
    automation_orchestration_data_analysis_skills = models.TextField(blank=True, null=True)
    other_technical_skills = models.TextField(blank=True, null=True)

    technical_support_and_maintenance = models.TextField(blank=True, null=True)
    reliability = models.TextField(blank=True, null=True)
    flexibility = models.TextField(blank=True, null=True)
    integrity = models.TextField(blank=True, null=True)
    availability = models.TextField(blank=True, null=True)
    solution_scalability = models.TextField(blank=True, null=True)
    other_requested_solution_quality = models.TextField(blank=True, null=True)

    project_management_approaches = models.TextField(blank=True, null=True)
    project_management_tools = models.TextField(blank=True, null=True)
    development_methods = models.TextField(blank=True, null=True)
    project_resources = models.TextField(blank=True, null=True)
    training = models.TextField(blank=True, null=True)

    deployment = models.TextField(blank=True, null=True)
    technical_support_and_maintenance = models.TextField(blank=True, null=True)
    legal_compliance = models.TextField(blank=True, null=True)
    regulations = models.TextField(blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company', 'pdf_name'], name='unique_company_pdf')
        ]

    def __str__(self):
        return f"{self.pdf_name} - {self.company.username}"
