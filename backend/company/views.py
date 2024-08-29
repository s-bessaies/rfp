from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from PdfAnalysis.models import PDFAnalysis
import uuid
from .models import Company
import json
from django.contrib.auth import authenticate
from django.http import JsonResponse
from .serializers import CompanySerializer
from django.views.decorators.csrf import csrf_exempt
import math
from numpy import dot
from numpy import dot
from numpy.linalg import norm
import numpy as np
import chromadb
import requests
from openai import OpenAI
import os
from dotenv import load_dotenv
from chromadb.config import Settings

load_dotenv()

# chroma_client = chromadb.PersistentClient(path="chroma")
chroma_client = chromadb.HttpClient(host="chromadb",port=8000)



client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
def cosine_similarity(embedding1, embedding2):
    return dot(embedding1, embedding2) / (norm(embedding1) * norm(embedding2))

def euclidean_distance(embedding1, embedding2):
    embedding1 = np.array(embedding1)
    embedding2 = np.array(embedding2)
    return np.linalg.norm(embedding1 - embedding2)

def calculate_combined_similarity(rfp_embedding, company_embedding):
    if rfp_embedding == [0.0] * 1536:
        return 1.0
    
    cosine_sim = cosine_similarity(rfp_embedding, company_embedding)
    euclidean_dist = euclidean_distance(rfp_embedding, company_embedding)
    combined_score = 0.8 * cosine_sim + 0.2 * euclidean_dist
    return combined_score
def get_lat_lon(location_name):
    api_url = f"https://geocode.maps.co/search?q={location_name.replace(' ', '%20')}&api_key=66be1188efc82199460301hxf887009"
    response = requests.get(api_url)
    data = response.json()
    if data:
        return float(data[0]["lat"]), float(data[0]["lon"])
    return None, None
def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distance in kilometers
@api_view(['POST'])
def company_create(request):
    if request.method == 'POST':
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@csrf_exempt
@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            username = body.get('username')
            password = body.get('password')

            if not username or not password:
                return JsonResponse({'error': 'Username and password are required'}, status=400)

            try:
                company = Company.objects.get(username=username)
                
                if company.check_password(password):
                    token = str(uuid.uuid4())

                    return JsonResponse({
                        'message': 'Login successful',
                        'username': username,
                        'token': token
                    }, status=200)
                else:
                    return JsonResponse({'error': 'Invalid username or password'}, status=400)
            except Company.DoesNotExist:
                return JsonResponse({'error': 'Invalid username or password'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

@api_view(['GET'])
def get_company_info(request,username):
    try:
        company = Company.objects.get(username=username)
        if company:
            serializer = CompanySerializer(company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_company_info(request,username):
    if hasattr(chroma_client, 'list_collections'):
        collections = chroma_client.list_collections()
        print("Collections:", collections)
    else:
        print("No method to list collections found.")

    try:
        company = Company.objects.get(username=username)
        if company:
            serializer = CompanySerializer(company, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                company=Company.objects.get(username=username)
                company_attributes = {
                    "Company Overview": 
                        f"""{company.company_name}, headquartered in {company.headquarters_location}, 
                        established in {company.year_established}, with {company.company_size} employees, 
                        {company.ownership_structure}. 
                        .""",
                    "Activity Domain":f"""Focused on {', '.join([
                            f'{sector.get("sector", "N/A")} with subsectors: {", ".join(sector.get("subsectors", [])) or "N/A"}'
                            for sector in company.sector_of_activity if isinstance(sector, dict)
                        ])}""",
                    
                    "Location": company.headquarters_location,
                    
                    "Company Experience": 
                        f"""{company.years_of_experience} years of experience in relevant industries. 
                        Notable clients and projects include: 
                        {', '.join([
                            f"{proj.get('scope', 'N/A')} for {proj.get('client', 'N/A')} "
                            f"(with deliverables such as {proj.get('deliverables', 'N/A')})" 
                            for proj in company.projects if isinstance(proj, dict)
                        ])}""",
                    
                    "Certifications and Compliance": 
                        ', '.join(company.certifications) 
                        if isinstance(company.certifications, list) and all(isinstance(cert, str) for cert in company.certifications) 
                        else '',
                    
                    "Technical Capabilities": 
                        f"""{', '.join([
                            f"{it['resource']} ({it['it_category']})" 
                            for it in company.it if isinstance(it, dict)
                        ])}""",
                    
                    "Support and Maintenance": 
                        "24/7 technical support available via phone, email, and chat. Regular maintenance updates and patches are provided.",
                    
                    "Skills and Expertise": 
                        f"""{', '.join([
                            f"{skill['skill']} ({skill['skill_category']})" 
                            for skill in company.skills if isinstance(skill, dict)
                        ])}""",
                    
                    "CSR Policy and Environmental Commitment": 
                        f"{company.csr_policy} {company.environmental_commitment}",
                    
                }
                attributes_to_compare = {
                    "sector": ["Activity Domain"], 
                    
                    "skills_and_references": [
                        "Company Experience",  
                        "Skills and Expertise",  
                        "Certifications and Compliance",  # Mapping "Relevant Certifications and Compliance"
                    ],
                    
                    "infrastructure": ["Technical Capabilities"],  # Mapping "Technological Infrastructure"
                    
                    "technical_skills": [
                        "Skills and Expertise", 
                        "Technical Capabilities"  # Mapping "Technological Infrastructure"
                    ],
                    
                    "requested_solution_quality": [
                        "Technical Capabilities",  # Mapping "Technological Infrastructure"
                        "Support and Maintenance",  # Mapping "Support and Maintenance"
                        "Certifications and Compliance"  # Mapping "Relevant Certifications and Compliance"
                    ],
                    
                    "project_management_and_resources": ["Skills and Expertise","Company Experience"],  # Mapping "Skills"
                    
                    # Mapping "Support and Maintenance"
                    
                    "legal_compliance": [
                        "CSR Policy and Environmental Commitment",  # Mapping "CSR Policy and Environmental Commitment"
                        "Certifications and Compliance",
                    ],
                    "regulations":[
                        "CSR Policy and Environmental Commitment",  # Mapping "CSR Policy and Environmental Commitment"
                        "Certifications and Compliance",
                    ]
                }

                print(company_attributes)
                collection = chroma_client.get_collection(name="rfp_vector_dbb")
                print("collection:",collection)
                collection = chroma_client.get_collection(name="rfp_vector_dbb")

# Log the collection details
                print("Collection details:")
                print("Name:", collection.name)
                print("Metadata:", collection.metadata)
                print("Total Embeddings:", collection.count())

                # Check if the collection is empty
                if collection.count() == 0:
                    print("The collection is empty.")
                else:
                    print("The collection contains embeddings.")

                # If you want to log more specific information about the collection, such as the first few embeddings:
                print(collection.peek())
                company_embeddings={}
                for key in company_attributes:
                    print("attribute:",company_attributes[key])
                    company_embeddings[key]=get_embedding(company_attributes[key])  
                company = Company.objects.get(username=username)
                all_pdf_analyses = PDFAnalysis.objects.filter(company=company)
                for pdf_analysis in all_pdf_analyses:
                    print(pdf_analysis.id)
                print(all_pdf_analyses)
                
                for pdf_analysis in all_pdf_analyses:
                    rfp_embeddings = {
                        "sector": [],
                        "dates": [],
                        "skills_and_references": [],
                        "infrastructure":[],
                        "technical_skills":[],
                        "requested_solution_quality": [],
                        "project_management_and_resources": [],
                        "legal_compliance": [],
                        "regulations":[]
                    }
                    for key in rfp_embeddings:
                        print("key:",key)
                        print(f"{pdf_analysis.id}_{key}")
                        results = collection.get(
                           ids=f"{pdf_analysis.id}_{key}",include=['embeddings']
                        )
                        print(len(results['embeddings'][0]))
                        rfp_embeddings[key]=results['embeddings'][0]
                    for key, value in rfp_embeddings.items():
                        print(f"Key: {key}, Embedding: {value[:5]}... ")
                    rfp_similarity={}
                    location_rfp=pdf_analysis.location
                    company_lat, company_lon = get_lat_lon(company_attributes["Location"])
                    if location_rfp!="null":
                        try:
                            rfp_lat,rfp_lon = get_lat_lon(location_rfp)
                            if company_lat is not None and company_lon is not None:
                                distance = haversine(company_lat, company_lon, rfp_lat, rfp_lon)
                                similarity_score = 1.0 / (1.0 + distance * 0.001)
                                print(f"Location similarity score: {similarity_score:.2f}")
                                rfp_similarity['location']=similarity_score
                            else:
                                print(f"Location similarity score (missing company coordinates): {similarity_score:.2f}")
                        except (IndexError, ValueError):
                            print(f"Invalid location data: {location_rfp}")
                    for rfp_key, rfp_embedding in rfp_embeddings.items():
                        if rfp_key != "location":
                            total_similarity_score = 0
                            num_comparisons = 0
                            if rfp_embedding!=  [0.0] * 1536:
                                for key in attributes_to_compare.get(rfp_key, []):
                                    company_embedding = company_embeddings.get(key)
                                    if company_embedding is not None:
                                        combined_score = calculate_combined_similarity(rfp_embedding, company_embedding)
                                        print(f"Combined similarity score for {rfp_key} against {key}: {combined_score:.2f}")
                                        total_similarity_score += combined_score
                                        num_comparisons += 1
                                    else:
                                        print(f"No matching company embedding for key: {key}")

                                average_similarity = total_similarity_score / num_comparisons if num_comparisons > 0 else 0.0
                                rfp_similarity[rfp_key] = round(average_similarity, 2)
                    print("Similarities:")

                    print(f"RFP ID: {pdf_analysis.id} Similarity Scores: {rfp_similarity}")
                    print(f"Processing score update for RFP ID: {pdf_analysis.id}")

                    total_score = sum(rfp_similarity.values())
                    total_score = round((total_score*100)/len(rfp_similarity),2)
                    print(f"Total score to add for RFP ID {pdf_analysis.id}: {total_score}")
                    pdf_analysis.score = total_score
                    pdf_analysis.save()
                    
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)