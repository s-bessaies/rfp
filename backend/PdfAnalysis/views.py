from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Company, PDFAnalysis
from langchain.document_loaders import PyPDFLoader
from langchain_mistralai import MistralAIEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from langgraph.graph import StateGraph
import requests


from .import graph
import logging
import tempfile
import chromadb
import math
from numpy import dot
from numpy import dot
from numpy.linalg import norm
import numpy as np
from openai import OpenAI
from  dotenv import load_dotenv
import os
from chromadb.config import Settings

load_dotenv()
# chroma_client = chromadb.PersistentClient(path="chroma")
chroma_client = chromadb.HttpClient(host="chromadb",port=8000)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
logger = logging.getLogger(__name__)
def cosine_similarity(embedding1, embedding2):
    return dot(embedding1, embedding2) / (norm(embedding1) * norm(embedding2))

def euclidean_distance(embedding1, embedding2):
    embedding1 = np.array(embedding1)
    embedding2 = np.array(embedding2)
    return np.linalg.norm(embedding1 - embedding2)

def calculate_combined_similarity(rfp_embedding, company_embedding):
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
@api_view(['GET'])
def rfp_history(request):
    username = request.GET.get('username')
    try:
        
        company = Company.objects.get(username=username)
        

        

        pdf_analysis_list = PDFAnalysis.objects.filter(company=company)
        
        if not pdf_analysis_list.exists():
            return Response({"message": "No PDF analysis history found for this user."}, status=404)

        history_data = []
        for analysis in pdf_analysis_list:
            history_data.append({
                'description':analysis.description,
                'pdf_name': analysis.pdf_name,
                'creation_date':analysis.creation_date,
                'sector': analysis.sector or '',
                'dates': analysis.dates or '',
                'location': analysis.location or '',
                'minimum_experience': analysis.minimum_experience or '',
                'required_certifications': analysis.required_certifications or '',
                'similar_project_references': analysis.similar_project_references or '',
                'it_infrastructure': analysis.it_infrastructure or '',
                'network_infrastructure': analysis.network_infrastructure or '',
                'virtualization': analysis.virtualization or '',
                'programming_languages': analysis.programming_languages or '',
                'cloud_computing_data_management_ai_skills': analysis.cloud_computing_data_management_ai_skills or '',
                'cybersecurity_devops_big_data_skills': analysis.cybersecurity_devops_big_data_skills or '',
                'iot_network_telecom_blockchain_skills': analysis.iot_network_telecom_blockchain_skills or '',
                'automation_orchestration_data_analysis_skills': analysis.automation_orchestration_data_analysis_skills or '',
                'other_technical_skills': analysis.other_technical_skills or '',
                'reliability': analysis.reliability or '',
                'flexibility': analysis.flexibility or '',
                'integrity': analysis.integrity or '',
                'availability': analysis.availability or '',
                'solution_scalability': analysis.solution_scalability or '',
                'other_requested_solution_quality': analysis.other_requested_solution_quality or '',
                'project_management_approaches': analysis.project_management_approaches or '',
                'project_management_tools': analysis.project_management_tools or '',
                'development_methods': analysis.development_methods or '',
                'project_resources': analysis.project_resources or '',
                'training': analysis.training or '',
                'deployment': analysis.deployment or '',
                'technical_support_and_maintenance': analysis.technical_support_and_maintenance or '',
                'legal_compliance': analysis.legal_compliance or '',
                'regulations': analysis.regulations or '',
                'score':analysis.score
            })
        
        return Response(history_data, status=200)
    except Company.DoesNotExist:
        return Response({"error": "Company not found for the given username."}, status=404)
    except Exception as e:
        logger.error("Error fetching PDF analysis history: %s", str(e))
        return Response({"error": str(e)}, status=500)
@api_view(['GET'])
def rfp_history_top(request):
    username = request.GET.get('username')
    try:
        
        company = Company.objects.get(username=username)
        

        

        pdf_analysis_list = PDFAnalysis.objects.filter(company=company).order_by('-score')[:5]

        if not pdf_analysis_list.exists():
            return Response({"message": "No PDF analysis history found for this user."}, status=404)

        history_data = []
        for analysis in pdf_analysis_list:
            history_data.append({
                'description':analysis.description,
                'pdf_name': analysis.pdf_name,
                'creation_date':analysis.creation_date,
                'sector': analysis.sector or '',
                'dates': analysis.dates or '',
                'location': analysis.location or '',
                'minimum_experience': analysis.minimum_experience or '',
                'required_certifications': analysis.required_certifications or '',
                'similar_project_references': analysis.similar_project_references or '',
                'it_infrastructure': analysis.it_infrastructure or '',
                'network_infrastructure': analysis.network_infrastructure or '',
                'virtualization': analysis.virtualization or '',
                'programming_languages': analysis.programming_languages or '',
                'cloud_computing_data_management_ai_skills': analysis.cloud_computing_data_management_ai_skills or '',
                'cybersecurity_devops_big_data_skills': analysis.cybersecurity_devops_big_data_skills or '',
                'iot_network_telecom_blockchain_skills': analysis.iot_network_telecom_blockchain_skills or '',
                'automation_orchestration_data_analysis_skills': analysis.automation_orchestration_data_analysis_skills or '',
                'other_technical_skills': analysis.other_technical_skills or '',
                'reliability': analysis.reliability or '',
                'flexibility': analysis.flexibility or '',
                'integrity': analysis.integrity or '',
                'availability': analysis.availability or '',
                'solution_scalability': analysis.solution_scalability or '',
                'other_requested_solution_quality': analysis.other_requested_solution_quality or '',
                'project_management_approaches': analysis.project_management_approaches or '',
                'project_management_tools': analysis.project_management_tools or '',
                'development_methods': analysis.development_methods or '',
                'project_resources': analysis.project_resources or '',
                'training': analysis.training or '',
                'deployment': analysis.deployment or '',
                'technical_support_and_maintenance': analysis.technical_support_and_maintenance or '',
                'legal_compliance': analysis.legal_compliance or '',
                'regulations': analysis.regulations or '',
                'score':analysis.score
            })
        
        return Response(history_data, status=200)
    except Company.DoesNotExist:
        return Response({"error": "Company not found for the given username."}, status=404)
    except Exception as e:
        logger.error("Error fetching PDF analysis history: %s", str(e))
        return Response({"error": str(e)}, status=500)

from django.db import transaction

@api_view(['PUT'])
def process_pdf(request):
    try:
        username = request.data.get('username')
        pdf_file = request.FILES.get('pdf')
        documents = None

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            temp_pdf.write(pdf_file.read())
            temp_pdf.flush()

            print("Loaded PDF into temporary file")

            loader = PyPDFLoader(temp_pdf.name)
            documents = loader.load()

        logger.info("Received request with username: %s", username)

        if not pdf_file or not hasattr(pdf_file, 'read'):
            return Response({'message': 'Invalid file'}, status=400)

        if not username:
            return Response({"error": "Username is required"}, status=400)

        try:
            company = Company.objects.get(username=username)
        except Company.DoesNotExist:
            return Response({"error": "Company does not exist"}, status=404)

        logger.info("Company found: %s", company)
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


        mistral = MistralAIEmbeddings(model="mistral-embed")
        text_splitter = SemanticChunker(mistral, breakpoint_threshold_type="standard_deviation")
        semantic_chunks = text_splitter.create_documents([d.page_content for d in documents])

        logger.info("Created semantic chunks: %d chunks", len(semantic_chunks))

        chunks = [semantic_chunk.page_content for semantic_chunk in semantic_chunks]
        pdf_json = {}

        workflow = StateGraph(graph.State)
        workflow.add_node("init", graph.function_init)
        workflow.add_edge('init', 'group chunks')
        workflow.add_node("group chunks", graph.group_chunk_by_category)
        workflow.add_edge('group chunks', 'generate json')
        workflow.add_node("generate json", graph.generate_pdf_json)
        workflow.add_edge("generate json", "log_state")
        workflow.add_node("log_state", graph.log_state)
        workflow.set_entry_point("init")
        workflow.set_finish_point("log_state")

        print("Compiled workflow")

        initstate = graph.State(workflow_steps=0, chunks=chunks, pdf_data={}, pdf_json={})
        g = workflow.compile()
        if g is None:
            raise ValueError("Compiled workflow is None. Please check the compile method.")

        for output in g.stream(initstate):
            for key, value in output.items():
                pdf_json = value['pdf_json']
        
        print("Workflow executed successfully")
        response1={
                    'pdf_name':pdf_file.name,
                    'sector': pdf_json.get("Sector", []),
                    'dates': pdf_json.get("Dates", []),
                    'location': pdf_json.get("Location", []),
                    'minimum_experience': pdf_json["Skills and References"].get("Minimum Experience", []),
                    'required_certifications': pdf_json["Skills and References"].get("Required Certifications", []),
                    'similar_project_references': pdf_json["Skills and References"].get("Similar Project References", []),
                    'it_infrastructure': pdf_json["Infrastructure"].get("IT Infrastructure", []),
                    'network_infrastructure': pdf_json["Infrastructure"].get("Network Infrastructure", []),
                    'virtualization': pdf_json["Infrastructure"].get("Virtualization", []),
                    'programming_languages': pdf_json["Technical Skills"].get("Programming Languages", []),
                    'cloud_computing_data_management_ai_skills': pdf_json["Technical Skills"].get("Cloud Computing, Data Management, AI Skills", []),
                    'cybersecurity_devops_big_data_skills': pdf_json["Technical Skills"].get("Cybersecurity, DevOps, Big Data Skills", []),
                    'iot_network_telecom_blockchain_skills': pdf_json["Technical Skills"].get("IoT, Network, Telecommunications, Blockchain Skills", []),
                    'automation_orchestration_data_analysis_skills': pdf_json["Technical Skills"].get("Automation, Orchestration, Data Analysis Skills", []),
                    'other_technical_skills': pdf_json["Technical Skills"].get("Others", []),
                    'technical_support_and_maintenance': pdf_json["Requested Solution Quality"].get("Technical Support and Maintenance", []),
                    'reliability': pdf_json["Requested Solution Quality"].get("Reliability", []),
                    'flexibility': pdf_json["Requested Solution Quality"].get("Flexibility", []),
                    'integrity': pdf_json["Requested Solution Quality"].get("Integrity", []),
                    'availability': pdf_json["Requested Solution Quality"].get("Availability", []),
                    'solution_scalability': pdf_json["Requested Solution Quality"].get("Solution Scalability", []),
                    'other_requested_solution_quality': pdf_json["Requested Solution Quality"].get("Others", []),
                    'project_management_approaches': pdf_json["Project Management and Resources"].get("Project Management Approaches", []),
                    'project_management_tools': pdf_json["Project Management and Resources"].get("Project Management Tools", []),
                    'development_methods': pdf_json["Project Management and Resources"].get("Development Methods", []),
                    'project_resources': pdf_json["Project Management and Resources"].get("Project Resources", []),
                    'training': pdf_json["Project Management and Resources"].get("Training", []),
                    'deployment': pdf_json.get("Deployment", []),
                   
                    'legal_compliance': pdf_json.get("Legal Compliance", []),
                    'regulations':pdf_json.get("Regulations",[])}
        with transaction.atomic():
            
            pdf_analysis, created = PDFAnalysis.objects.update_or_create(
                company=company,
                pdf_name=pdf_file.name,
                defaults={
                    'description':pdf_json.get("Description", []),
                    'sector': pdf_json.get("Sector", "null"),
                    'dates': pdf_json.get("Dates", "null"),
                    'location': pdf_json.get("Location", "null"),
                    'minimum_experience': pdf_json["Skills and References"].get("Minimum Experience", "null"),
                    'required_certifications': pdf_json["Skills and References"].get("Required Certifications", "null"),
                    'similar_project_references': pdf_json["Skills and References"].get("Similar Project References", "null"),
                    'it_infrastructure': pdf_json["Infrastructure"].get("IT Infrastructure", "null"),
                    'network_infrastructure': pdf_json["Infrastructure"].get("Network Infrastructure", "null"),
                    'virtualization': pdf_json["Infrastructure"].get("Virtualization", "null"),
                    'programming_languages': pdf_json["Technical Skills"].get("Programming Languages", "null"),
                    'cloud_computing_data_management_ai_skills': pdf_json["Technical Skills"].get("Cloud Computing, Data Management, AI Skills", "null"),
                    'cybersecurity_devops_big_data_skills': pdf_json["Technical Skills"].get("Cybersecurity, DevOps, Big Data Skills", "null"),
                    'iot_network_telecom_blockchain_skills': pdf_json["Technical Skills"].get("IoT, Network, Telecommunications, Blockchain Skills", "null"),
                    'automation_orchestration_data_analysis_skills': pdf_json["Technical Skills"].get("Automation, Orchestration, Data Analysis Skills", "null"),
                    'other_technical_skills': pdf_json["Technical Skills"].get("Others", "null"),
                    'technical_support_and_maintenance': pdf_json["Requested Solution Quality"].get("Technical Support and Maintenance", "null"),
                    'reliability': pdf_json["Requested Solution Quality"].get("Reliability", "null"),
                    'flexibility': pdf_json["Requested Solution Quality"].get("Flexibility", "null"),
                    'integrity': pdf_json["Requested Solution Quality"].get("Integrity", "null"),
                    'availability': pdf_json["Requested Solution Quality"].get("Availability", "null"),
                    'solution_scalability': pdf_json["Requested Solution Quality"].get("Solution Scalability", "null"),
                    'other_requested_solution_quality': pdf_json["Requested Solution Quality"].get("Others", "null"),
                    'project_management_approaches': pdf_json["Project Management and Resources"].get("Project Management Approaches", "null"),
                    'project_management_tools': pdf_json["Project Management and Resources"].get("Project Management Tools", "null"),
                    'development_methods': pdf_json["Project Management and Resources"].get("Development Methods", "null"),
                    'project_resources': pdf_json["Project Management and Resources"].get("Project Resources", "null"),
                    'training': pdf_json["Project Management and Resources"].get("Training", "null"),
                    'deployment': pdf_json.get("Deployment", "null"),
                    'legal_compliance': pdf_json.get("Legal Compliance", "null"),
                    'regulations':pdf_json.get("Regulations","null"),
                    'score': 0
                }
            )

            rfp_id = pdf_analysis.id
            def concatenate_if_not_null(*args):
                return " ".join(filter(lambda x: x and x != "null", args)) or "null"

            rfp_attributes = {
                "sector": pdf_analysis.sector if pdf_analysis.sector != "null" else "null",
                "dates": pdf_analysis.dates if pdf_analysis.dates != "null" else "null",
                "location": pdf_analysis.location if pdf_analysis.location != "null" else "null",
                "skills_and_references": concatenate_if_not_null(
                    pdf_analysis.minimum_experience, 
                    pdf_analysis.required_certifications, 
                    pdf_analysis.similar_project_references
                ),
                "infrastructure": concatenate_if_not_null(
                    pdf_analysis.it_infrastructure, 
                    pdf_analysis.network_infrastructure, 
                    pdf_analysis.virtualization
                ),
                "technical_skills": concatenate_if_not_null(
                    pdf_analysis.programming_languages, 
                    pdf_analysis.cloud_computing_data_management_ai_skills, 
                    pdf_analysis.cybersecurity_devops_big_data_skills, 
                    pdf_analysis.iot_network_telecom_blockchain_skills, 
                    pdf_analysis.automation_orchestration_data_analysis_skills, 
                    pdf_analysis.other_technical_skills
                ),
                "requested_solution_quality": concatenate_if_not_null(
                    pdf_analysis.technical_support_and_maintenance, 
                    pdf_analysis.reliability, 
                    pdf_analysis.flexibility, 
                    pdf_analysis.integrity, 
                    pdf_analysis.availability, 
                    pdf_analysis.solution_scalability, 
                    pdf_analysis.other_requested_solution_quality
                ),
                "project_management_and_resources": concatenate_if_not_null(
                    pdf_analysis.project_management_approaches, 
                    pdf_analysis.project_management_tools, 
                    pdf_analysis.development_methods, 
                    pdf_analysis.project_resources, 
                    pdf_analysis.training
                ),
                "legal_compliance": pdf_analysis.legal_compliance if pdf_analysis.legal_compliance != "null" else "null",
                "regulations":pdf_analysis.regulations if pdf_analysis.regulations != "null" else "null"
            }
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

            
            rfp_embeddings = {
                key: [0.0] * 1536 if "null" in value.lower() else get_embedding(value)
                for key, value in rfp_attributes.items()
                if value is not None
            }
            
            eMbeddings = []

            for key in rfp_embeddings:
                if key != 'location':
                    eMbeddings.append(rfp_embeddings[key])

            collection_name = "rfp_vector_dbb"
            collection = chroma_client.get_or_create_collection(name=collection_name)

            if len([key for key in rfp_embeddings if key != 'location']) == len(eMbeddings):
                print("yes")
                collection.upsert(
                    documents=[f"{key}: {value}" for key, value in rfp_attributes.items() if value is not None and key != 'location'],
                    embeddings=eMbeddings,
                    metadatas=[{"rfp_id": rfp_id,"key":key} for key in rfp_attributes.keys() if key != 'location'] ,  # Match length to eMbeddings
                    ids=[f"{rfp_id}_{key}" for key in rfp_embeddings.keys() if key != 'location']
                )
            else:
                print("no")
            company_embeddings={}
            for key in company_attributes:
                print("attribute:",company_attributes[key])
                company_embeddings[key]=get_embedding(company_attributes[key])  
            
            
            company_lat, company_lon = get_lat_lon(company_attributes["Location"])
            location_rfp = rfp_attributes['location']
            similarity_score = 0.0
            rfp_similarity = {}
            if location_rfp!="null":
                try:
                    rfp_lat,rfp_lon = get_lat_lon(location_rfp)
                    if (company_lat is not None and company_lon is not None)and(rfp_lat is not None and rfp_lon is not None):
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

            print(f"RFP ID: {rfp_id} Similarity Scores: {rfp_similarity}")
            print(f"Processing score update for RFP ID: {rfp_id}")

            total_score = sum(rfp_similarity.values())
            total_score = round((total_score*100)/len(rfp_similarity),2)
            print(f"Total score to add for RFP ID {rfp_id}: {total_score}")
            pdf_analysis.score = total_score
            pdf_analysis.save()
            
        if created:
            logger.info("PDF analysis created successfully")
        else:
            logger.info("PDF analysis updated successfully")
        

    except Exception as e:
        logger.error("Error processing PDF: %s", str(e))
        return Response({"error": str(e)}, status=500)

    return Response(response1)
