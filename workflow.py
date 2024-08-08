import os
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from PyPDF2 import PdfReader
from langchain_mistralai import ChatMistralAI
from typing_extensions import TypedDict




os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_API_KEY'] = ''
os.environ["OPENAI_API_KEY"] = '' 
os.environ["LANGFUSE_PUBLIC_KEY"] = ""
os.environ["LANGFUSE_SECRET_KEY"] = ""


# Define the States TypedDict for workflow states
class States(TypedDict):
    pdf_name: str
    workflow_steps: int
    pdf_content: str
    response: str

# Initialize workflow steps
def function_init(states: States) -> States:
    states["workflow_steps"] = 1
    return states

def read_pdf(state: States) -> States:
    pdf_content = ""
    print('aaaaaaaa :::::::',state["pdf_name"])
    with open(state["pdf_name"], "rb") as file:
        reader = PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            pdf_content += page.extract_text()
    state["pdf_content"] = pdf_content
    return state
# Initialize models
chain_gpt_4o_mini = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, top_p=1)
open_mistral_7b = ChatMistralAI(model="open-mixtral-8x22b", temperature=0.2, api_key="")


def langfuse(text: str) -> str:
    # Define chat prompt template
    chat_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
    You are an expert in analyzing and extracting information from Request for Proposal (RFP) documents.

    **Objective:**
    1. Extract and format the provided RFP text into a detailed, structured text format for each attribute. Ensure thorough coverage of each section and capture multiple entries where applicable.
    2. Summarize the detailed text while retaining all relevant details.

    **Output Format:**
    First, present the response as a detailed and structured text summary for each attribute, followed by the references extracted from the RFP text. Use the following format for each attribute:

    **Sector:**
    - **Detailed Summary:**
      [Detailed summary of the sector and focus areas mentioned in the RFP. Include specific sectors targeted, the purpose of the RFP, and any relevant programs or initiatives.]
    - **References from RFP text:**
      [List the references extracted from the RFP text that support the detailed summary.]

    **Dates:**
    - **Detailed Summary:**
      - Release RFP date: [Date]
      - Questions due date: [Date]
      - RFP response deadline: [Date]
      - Selection and award of contract date: [Date]
      - Others: [Additional dates or milestones such as follow-up actions or decision dates.]
    - **References from RFP text:**
      [List the references extracted from the RFP text that support the detailed summary.]

    **Location:**
    - **Detailed Summary:**
      [Detailed information about the location requirements mentioned in the RFP, including geographical scope, site specifics, or any regional considerations.]
    - **References from RFP text:**
      [List the references extracted from the RFP text that support the detailed summary.]

    **Skills and References:**
    - **Minimum experience:**
      - **Detailed Summary:**
        [Detailed description of the required experience, including years, specific skills, and types of projects or roles.]
      - **References from RFP text:**
        [List the references extracted from the RFP text that support the detailed summary.]
    - **Required certifications:**
      - **Detailed Summary:**
        [List of required certifications, with explanations of their relevance or importance.]
      - **References from RFP text:**
        [List the references extracted from the RFP text that support the detailed summary.]
    - **Similar project references:**
      - **Detailed Summary:**
        [Detailed requirements for providing references, including the format, information needed, and any evaluation criteria.]
      - **References from RFP text:**
        [List the references extracted from the RFP text that support the detailed summary.]

    **Infrastructure:**
    - **IT infrastructure:**
      - **Detailed Summary:**
        [Detailed specifications for IT infrastructure, including hardware, software, network components, and integration needs.]
      - **References from RFP text:**
        [List the references extracted from the RFP text that support the detailed summary.]
    - **Network infrastructure:**
      - **Detailed Summary:**
        [Details on network requirements, including bandwidth, connectivity, and security measures.]
      - **References from RFP text:**
        [List the references extracted from the RFP text that support the detailed summary.]
    - **Virtualization:**
      - **Detailed Summary:**
        [Information on virtualization needs, if applicable, including types of virtualization technologies and their purposes.]
      - **References from RFP text:**
        [List the references extracted from the RFP text that support the detailed summary.]

    **Technical Skills:**
    - **Programming languages:**
      - **Detailed Summary:**
        [Detailed list of programming languages required, including versions and usage contexts.]
      - **References from RFP text:**
        [List the references extracted from the RFP text that support the detailed summary.]
    - **Cloud computing, data management, AI skills:**
      - **Detailed Summary:**
        [Skills and technologies required for cloud computing, data management, and AI, including specific tools or platforms.]
      - **References from RFP text:**
        [List the references extracted from the RFP text that support the detailed summary.]
    - **Cybersecurity, DevOps, Big Data skills:**
      - **Detailed Summary:**
        [Requirements for cybersecurity, DevOps practices, and big data management, including relevant tools and methodologies.]
      - **References from RFP text:**
        [List the references extracted from the RFP text that support the detailed summary.]
    - **IoT, network, telecommunications, blockchain skills:**
      - **Detailed Summary:**
        [Skills related to IoT, networking, telecommunications, and blockchain, including their relevance to the project.]
      - **References from RFP text:**
        [List the references extracted from the RFP text that support the detailed summary.]
    - **Automation, orchestration, data analysis skills:**
      - **Detailed Summary:**
        [Skills required for automation, orchestration, and data analysis, including specific technologies and methodologies.]
      - **References from RFP text:**
        [List the references extracted from the RFP text that support the detailed summary.]
    - **Others:**
      - **Detailed Summary:**
        [Any additional technical skills required.]
      - **References from RFP text:**
        [List the references extracted from the RFP text that support the detailed summary.]

    **Requested Solution Quality:**
    - **Maintainability:**
      - **Detailed Summary:**
        [Detailed requirements for maintainability, including ease of updates, ongoing management, and support.]
      - **References from RFP text:**
        [List the references extracted from the RFP text that support the detailed summary.]
    - **Reliability:**
      - **Detailed Summary:**
        [Criteria for reliability, including uptime requirements, fault tolerance, and redundancy.]
      - **References from RFP text:**
        [List the references extracted from the RFP text that support the detailed summary.]
    - **Flexibility:**
      - **Detailed Summary:**
        [Requirements for flexibility, including customization options and adaptability to changing needs.]
      - **References from RFP text:**
        [List the references extracted from the RFP text that support the detailed summary.]
    - **Integrity:**
      - **Detailed Summary:**
        [Details on integrity requirements, including data protection, security measures, and compliance standards.]
      - **References from RFP text:**
        [List the references extracted from the RFP text that support the detailed summary.]
    - **Availability:**
      - **Detailed Summary:**
        [Requirements for availability, including uptime guarantees, support, and disaster recovery plans.]
      - **References from RFP text:**
        [List the references extracted from the RFP text that support the detailed summary.]

    Please ensure that your response follows this format and captures the required information.
                """,
            ),
            (
                "user",
                "Please analyze the following RFP text: {text}",
            ),
        ]
    )


    # Create the LLMChain with chat template and models
    llm_chain = chat_template | chain_gpt_4o_mini

    response = llm_chain.invoke({"text": text})

    print("Extracted Information:", response)
    
    print("yessssss we are hereeee 111111111111 ")
    return response.content


def result(state: States) -> States:
    state["response"] = langfuse(state["pdf_content"])
    print("yessssss we are hereeee 222222222222 ")
    return state


# Define a LangChain graph
workflow = StateGraph(States)

# Initial function
workflow.add_node("init", function_init)
workflow.add_edge('init', 'read_pdf')

# Extract text from PDF
workflow.add_node("read_pdf", read_pdf)
workflow.add_edge('read_pdf', 'result')

# Filter by sector
workflow.add_node("result", result)


# Set entry and finish points
workflow.set_entry_point("init")
workflow.set_finish_point("result")

# Compile the workflow
app = workflow.compile()
