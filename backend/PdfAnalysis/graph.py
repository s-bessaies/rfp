from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from PyPDF2 import PdfReader
from io import BytesIO
import os
from langchain_mistralai import ChatMistralAI
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict
from langchain_experimental.text_splitter import SemanticChunker
from langchain_core.prompts import ChatPromptTemplate 
from langchain_mistralai.chat_models import ChatMistralAI
from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langfuse.decorators import observe
from langfuse import Langfuse
load_dotenv()
client =OpenAI(api_key=os.environ.get("OPENAI_API_KEY")) 
class State(TypedDict):
    pdf_name: str 
    workflow_steps: int = 0
    pdf_content: str 
    response: str
    
def function_init(state: State) -> State:
    state["workflow_steps"] = 1
    pdf_content= "" 
    pdf_name= "" 
    response= ""
    
    return state


import tempfile
from PyPDF2 import PdfReader
from io import BytesIO

def read_pdf(state: State) -> State:
    pdf_content = ""

    # Assurez-vous que l'objet pdf_name est un fichier InMemoryUploadedFile
    if hasattr(state["pdf_name"], 'read'):
        # Utilisez un fichier temporaire pour stocker le contenu du fichier PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            temp_pdf.write(state["pdf_name"].read())
            temp_pdf.flush()
            temp_pdf_path = temp_pdf.name

            print("Loaded PDF into temporary file")

            # Utilisez PyPDF2 pour lire le fichier temporaire
            with open(temp_pdf_path, "rb") as file:
                reader = PdfReader(file)
                num_pages = len(reader.pages)
                for page_num in range(num_pages):
                    page = reader.pages[page_num]
                    pdf_content += page.extract_text()

            state["pdf_content"] = pdf_content

            # Nettoyez le fichier temporaire
            os.remove(temp_pdf_path)
    else:
        raise TypeError("Expected an InMemoryUploadedFile or similar object")

    return state



    
# Initialiser les modèles
chain_gpt_4o_mini = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, top_p=1)
open_mistral_7b = ChatMistralAI(model="open-mistral-7b", temperature=0.2, api_key="mistral key")
open_mixtral_8x7b = ChatMistralAI(model=" open-mixtral-8x7b", temperature=0.2, api_key="mistral key")
open_mixtral_8x22b = ChatMistralAI(model="open-mixtral-8x22b", temperature=0.2, api_key="mistral key")




def langfuse(text):

    chat_template = ChatPromptTemplate.from_messages(
        [
(
"system",
    f"""
You are an expert in analyzing and extracting information from Request for Proposal (RFP) documents.

**Objective:**
Extract and format the provided RFP text into a detailed, structured text format for each attribute, focusing on clarity and relevance.

**Output Format:**
Present the response as a structured text summary for each attribute. Use the format below:

**Sector:**

**Detailed Summary:**
[Summary of the sector and focus areas in the RFP. Include specific sectors targeted and the purpose of the RFP.]

---

**Dates:**

**Detailed Summary:**
- Release RFP date: [Date, or return "null"]
- Questions due date: [Date, or return "null"]
- RFP response deadline: [Date, or return "null"]
- Selection and award of contract date: [Date, or return "null"]
- Others: [Additional dates or milestones, or return "null"]

---

Location: 

City, State


Return the city and state in the format: "City, State." or Null
Extract the name of the city without any preceding text such as "City of" and capitalize it properly, Extract the name of the state and capitalize it properly

---

**Minimum experience:**

**Detailed Summary:**
[Description of required experience, including years and specific skills, or return "null" if not applicable.]

---

**Required certifications:**

**Detailed Summary:**
[List of required certifications and their relevance, or return "null" if not applicable.]

---

**Similar project references:**

**Detailed Summary:**
[Requirements for providing references, including evaluation criteria, or return "null" if not applicable.]

---

**Infrastructure:**

**IT infrastructure:**

**Detailed Summary:**
[Specifications for IT infrastructure, including hardware and software, or return "null" if not applicable.]

---

**Network infrastructure:**

**Detailed Summary:**
[Details on network requirements, including security measures, or return "null" if not applicable.]

---

**Virtualization:**

**Detailed Summary:**
[Virtualization needs, including technologies and purposes, or return "null" if not applicable.]

---

**Technical Skills:**

**Programming languages:**

**Detailed Summary:**
[List of required programming languages and versions, or return "null" if not applicable.]

---

**Cloud computing, data management, AI skills:**

**Detailed Summary:**
[Skills required for cloud computing and AI, including specific tools, or return "null" if not applicable.]

---

**Cybersecurity, DevOps, Big Data skills:**

**Detailed Summary:**
[Requirements for cybersecurity and DevOps practices, or return "null" if not applicable.]

---

**IoT, network, telecommunications, blockchain skills:**

**Detailed Summary:**
[Skills related to IoT and blockchain, or return "null" if not applicable.]

---

**Automation, orchestration, data analysis skills:**

**Detailed Summary:**
[Skills required for automation and data analysis, or return "null" if not applicable.]

---

**Other technical skills:**

**Detailed Summary:**
[Other Skills required, or return "null" if not applicable.]

---

**Requested Solution Quality:**

**Technical Support and Maintenance:**

**Detailed Summary:**
[Comprehensive details on technical support and maintenance requirements, or return "null" if not applicable.]

---

**Maintainability:**

**Detailed Summary:**
[Requirements for maintainability, including updates and support, or return "null" if not applicable.]

---

**Reliability:**

**Detailed Summary:**
[Criteria for reliability, including uptime requirements, or return "null" if not applicable.]

---

**Flexibility:**

**Detailed Summary:**
[Requirements for flexibility and customization options, or return "null" if not applicable.]

---

**Integrity:**

**Detailed Summary:**
[Integrity requirements, including data protection and compliance, or return "null" if not applicable.]

---

**Availability:**

**Detailed Summary:**
[Requirements for availability, including support and disaster recovery, or return "null" if not applicable.]

---

**Solution scalability:**

**Detailed Summary:**
[Scalability requirements, including performance under load, or return "null" if not applicable.]

---

**other requested solution quality:**

**Detailed Summary:**
[other requested solution quality, or return "null" if not applicable.]

---

**Project Management and Resources:**

**Project management approaches:**

**Detailed Summary:**
[Description of required project management approaches, or return "null" if not applicable.]

---

**Project management tools:**

**Detailed Summary:**
[Tools required for project management and their functionalities, or return "null" if not applicable.]

---

**Development methods:**

**Detailed Summary:**
[Development methods to be used, with application explanations, or return "null" if not applicable.]

---

**Project resources:**

**Detailed Summary:**
[Details on required project resources and roles, or return "null" if not applicable.]

---

**Legal Compliance:**

**Detailed Summary:**
[Requirements for legal compliance, including laws, or return "null" if not applicable.]

---

**Regulations:**

**Detailed Summary:**
[Requirements for legal compliance, including regulations, or return "null" if not applicable.]

---

**Summary:**
Provide a concise summary of the entire RFP, focusing on the most critical information.

Instructions:

Carefully read the RFP text.
Provide a concise explanation for each attribute.
Ensure comprehensive coverage of each section.
Highlight any relevant discussions related to attributes.
Reread the text for each attribute, treating each question or list in the RFP as a source of details.
"""
),
            ("human", "{input}"),
        ]
    )

    chain = chat_template | chain_gpt_4o_mini

# # Initialize LLMChain with the chain
    # chain = LLMChain(llm=chain_gpt_4o_mini, prompt=chat_template)
    response = chain.invoke({"input": text})

    print("Extracted Information:", response)
    return response.content


def result(state: State) -> State:

    state["response"] = langfuse(state["pdf_content"])
    return state