import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from typing import List, Dict
from typing_extensions import TypedDict
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.prompts import FewShotChatMessagePromptTemplate
from langchain.chains import LLMChain
from langchain_mistralai.chat_models import ChatMistralAI


load_dotenv()
class State(TypedDict):
    workflow_steps: int
    chunks: List[str]
    pdf_data: Dict[str, List[str]]
    pdf_json: Dict[str, str]
def log_state(state: State):
    """Print the state"""
    print(f"---< Current State >---")
    print(f"- workflow_steps: {state['workflow_steps']}")
    print(f"- chunks: {state['chunks']}")
    print(f"- pdf_data: {state['pdf_data']}")
    print(f"- pdf_json: {state['pdf_json']}")
def function_init(state:State) ->State:
    state["workflow_steps"]  = 1
    
    return state

def group_chunk_by_category(state: State) -> State:

    chat_gpt_35 = ChatOpenAI(model="gpt-4o", max_tokens=3000,temperature=0.5)
    mistrallarge=ChatMistralAI(model='open-mixtral-8x22b',temperature=0.4)
    #chain_gpt_4o = ChatOpenAI(model="gpt-4o", max_tokens=3000)
    state["pdf_data"]= {
        "Sector":[],
        "Description":[],
        "Dates": [],
        "Location": [],
        "Skills and References": {
            "Minimum Experience": [],
            "Required Certifications": [],
            "Similar Project References": []
        },
        "Infrastructure": {
            "IT Infrastructure": [],
            "Network Infrastructure": [],
            "Virtualization": []
        },
       
        "Technical Skills": {
            "Programming Languages": [],
            "Cloud Computing, Data Management, AI Skills": [],
            "Cybersecurity, DevOps, Big Data Skills": [],
            "IoT, Network, Telecommunications, Blockchain Skills": [],
            "Automation, Orchestration, Data Analysis Skills": [],
            "Others": []
        },
        "Requested Solution Quality": {
            "Technical Support and Maintenance": [],
            "Reliability": [],
            "Flexibility": [],
            "Integrity": [],
            "Availability": [],
            "Solution Scalability": [],
            "Others": []
        },
        "Project Management and Resources": {
            "Project Management Approaches": [],
            "Project Management Tools": [],
            "Development Methods": [],
            "Project Resources": [],
            "Training": []
        },
        "Deployment": [],
        "Legal Compliance": [],
        "Regulations": []
    }

    examples = [
         {'input': 'The City of Duluth is soliciting proposals for the purchase of Case Management system for the City Attorney’s Office.', 'answer': 'Sector, Description'},
    {'input': 'Proposals must be received in the Purchasing Office by 4:30 PM on this date1. October 1, 2020', 'answer': 'Dates, Description'},
    {'input': 'The system should offer a scalable architecture that can grow with the State’s needs, accommodating new users, increased transaction volumes, and additional modules or functionalities seamlessly.', 'answer': 'Solution Scalability, Description'},
    {'input': 'The term of the contract will begin once the contract is fully executed and is anticipated to end by December 31, 2022.', 'answer': 'Dates, Description'},
    {'input': 'Ability for any on premise solutions to utilize VMWare’s virtual server platform.', 'answer': 'Virtualization, Description'},
    {'input': 'The solution must be highly reliable, ensuring continuous operation with minimal downtime. It should include built-in redundancy and failover mechanisms to handle hardware or software failures without affecting the user experience.', 'answer': 'Reliability, Availability, Description'},
    {'input': 'Ability to interface with Microsoft Office products including integration with Microsoft Outlook calendar where appropriate.', 'answer': 'IT Infrastructure, Description'},
    {'input': 'The Vendor shall provide for Administrative/Technical Support, Supervisor and End User training.', 'answer': 'Training, Description'},
    {'input': 'Consultant shall obtain and maintain for the Term of this Agreement the following minimum amounts of insurance from insurance companies authorized to do business in the State of Minnesota.', 'answer': 'Legal Compliance, Description'},
    {'input': 'The City reserves the right, in its sole and complete discretion, to reject any and all proposals or cancel the request for proposals, at any time prior to the time a contract is fully executed, when it is in its best interests.', 'answer': 'Irrelevant'},
    {'input': 'The software must allow for extensive customization options to tailor the system to the specific needs of different departments within the State. This customization should be possible through configuration settings rather than code changes', 'answer': 'Flexibility, Description'},
    {'input': "The State has anticipated an 18-month implementation schedule with a currently estimated completion date of April 2019. Bidders must provide a proposed implementation strategy and plan that demonstrates and promotes incremental phases, outcomes and deliverables. Each step detailing the cost and tactical benefits to the State. As discussed at the beginning of Section 6.3, the State recommends an Agile deployment methodology.", 'answer': "Dates, Deployment, Project Management Approaches, Description"},
    {'input': "The Contractor must plan for a Project Initiation phase of the project that allows for project planning, assessment and preparation activities prior to implementation of the Solution. This work will include, but not be limited to: Comprehensive review of overall project scope, Contract requirements and the responsibilities of both the State and the Contractor.", 'answer': "Project Management Approaches, Project Resources, Deployment, Description"},
    {'input': "The eProcurement Solution must be scalable to accommodate up to 10,000 users across the State of Vermont. It must provide a flexible and reliable platform that integrates with existing State systems, ensures data integrity and availability, and supports future growth.", 'answer': "Infrastructure, Solution Scalability, Availability, Integrity, Description"},
    {'input': "Bidders must submit a detailed resume for the Project Manager proposed for this engagement. The resume must include a comprehensive list of similar projects managed, highlighting relevant experience and certifications.", 'answer': "Minimum Experience, Required Certifications, Similar Project References, Description"},
    {'input': "The Contractor shall provide ongoing technical support and maintenance services post-implementation, ensuring the eProcurement Solution remains operational, secure, and up-to-date. This includes regular software updates, security patches, and user support.", 'answer': "Technical Support and Maintenance, Cybersecurity, DevOps, Big Data Skills, Description"},
    {'input': "All bids must be sealed and must be addressed to the State of Vermont, Office of Purchasing & Contracting, 109 State street – 3rd floor, Montpelier, VT 05609-3001.", 'answer': "Location, Description"},
    {'input': "ISSUE DATE September 20, 2017\nQUESTIONS DUE October 16, 2017 at 4:00 PM\nRFP RESPONSES DUE BY November 28, 2017 at 2:00 PM\nFINALIST DEMONSTRATIONS Anticipate month of January 2018\nPROJECT STARTS April 2018", 'answer': "Dates, Description"},
    {'input': "The Office of Purchasing & Contracting (OPC) on behalf of the State of Vermont, its departments, offices, institutions, and other agencies of the State of Vermont and counties, schools, institutions of higher education and municipalities, is soliciting competitive sealed, fixed price proposals (Proposals) from qualified firms/bidders to provide and implement a web-based software solution for Electronic Procurement (eProcurement) to increase efficiencies in the statewide procurement process.", 'answer': "Sector, Location, Description"},
    {'input': "The desired eProcurement solution must be innovative, fully integrated, and well-coordinated to empower the State of Vermont to achieve the following objectives and business outcomes that are organized around four Business Values:\n1. Cost Savings\n2. Customer Service Improvement\n3. Risk Reduction\n4. Compliance", 'answer': "Availability, Integrity, Description"},
    {'input': "The Solution must provide a user experience that is simple, direct and effective. Characteristics of this experience must include, at a minimum:\n• User entry into the Solution that can be configured such that the user is automatically navigated to the component most-relevant to the user (e.g. A Shopping User’s initial screen would be by default the Open Marketplace).\n• Intuitive navigation that guides users to the appropriate Solution component with as few clicks as possible.\n• Capability that allows user personalization of their initial screen based on their needs or use of the Solution.\n• Wizard-driven capabilities that can direct the user to the appropriate process or functionality of the Solution.\n• Dashboard functionality that informs users and supports user work management.\n• Functionality optimized for mobile access and use.", 'answer': "Flexibility, Cybersecurity, DevOps, Big Data Skills, Description"},
    {'input': "The State financial management system (VISION) is currently based on Oracle PeopleSoft Financials version 8.8. The State awarded a contract in late June 2017 to upgrade to PeopleSoft version 9.2. The upgrade timeline has a Go-Live date of December 2018 and the scope includes:\n• General Ledger (including Commitment Control)\n• Accounts Payable\n• Purchasing\n• Asset Management\n• Inventory\n• Billing\n• Accounts Receivable\n• Travel & Expenses\n• Grants Tracking (VT customized, bolt-on)\n• Upgrade the Disaster Recovery site", 'answer': "IT Infrastructure, Description"},
    {'input': "The implementation of the Solution is expected to be a predominantly 'center-led' strategy for procurement that balances Enterprise procurement needs with the decentralized procurement needs of individual Agencies and Departments while also providing centralized oversight/control when appropriate.", 'answer': "Project Resources, Project Management Approaches, Description"},
    {'input': "The Solution must also comply with all State and enterprise policies, standards including technology standards, State accessibility standards and data security standards, and procedures.", 'answer': "Legal Compliance, Description"},
    {'input': "The functionality the State envisions in a Solution would comprise full purchasing, sourcing, contracting and related processes with real-time integration to VISION at designated strategic points necessary to meet all State budget and financial management needs.", 'answer': "Integration, Description"},
    {'input': "The State of Vermont is interested in obtaining proposals to provide a managed Software-as-a-Service (SaaS) eProcurement solution that supports and complies with all State statutes, regulations, policies and guidelines relevant to procurement including soliciting, awarding, processing, executing and overseeing contracts, including contract compliance.", 'answer': "Sector, Legal Compliance, Description"},
    {'input': "The State’s functional requirements for the Solution are organized and presented below by the following procurement Workstreams:\n• Need to Pay\n• Catalog Capability\n• Vendor Enablement/Management\n• Sourcing/Bid Management\n• Contract Management\n• Spend/Data Analytics & Reporting", 'answer': "Cloud Computing, Data Management, AI Skills, Project Resources, Description"},
    {'input': 'The Contractor shall ensure that the solution adheres to the American Disabilities Act (ADA) requirements, ensuring accessibility for all users, including those with disabilities. This includes providing necessary accommodations and ensuring the software is usable with assistive technologies.', 'answer': 'Legal Compliance, Maintainability, Description'},
    {'input': 'The desired eProcurement solution must be innovative, fully integrated, and well-coordinated to empower the State of Vermont to achieve the following objectives and business outcomes that are organized around four Business Values: 1. Cost Savings: Over the lifecycle of the new Solution, it will: i. Streamline and standardize current manual, paper-based procurement, contracting, and purchasing processes and practices to shorten/compress cycle times. ii. Increase use of Statewide contracts to gain greater economies of scale, including accessibility to other eligible entities, authorities, municipalities, and K-12 Schools. iii. Provide visibility into all State spend to enable Spend Analytics, Strategic Sourcing and more effective Contracting. Thereby transforming procurement from tactical activities to a strategic focus. iv. Increase Vendor participation and competitiveness that drive finding the best possible product at the best value.', 'answer': 'Cost Savings, Description'},
    {'input': 'The contractor must comply with all applicable Federal, State, and local laws, regulations, and standards including but not limited to OSHA regulations, environmental regulations, and applicable labor laws.', 'answer': 'Legal Compliance, Description'},
        {
            'input':'The desired eProcurement solution must be innovative, fully integrated, and well-coordinated to empower the State of Vermont to achieve the following objectives and business outcomes that are organized around four Business Values: 1. Cost Savings: Over the lifecycle of the new Solution, it will: i. Streamline and standardize current manual, paper-based procurement, contracting, and purchasing processes and practices to shorten/compress cycle times. ii. Increase use of Statewide contracts to gain greater economies of scale, including accessibility to other eligible entities, authorities, municipalities, and K-12 Schools. iii. Provide visibility into all State spend to enable Spend Analytics, Strategic Sourcing and more effective Contracting. Thereby transforming procurement from tactical activities to a strategic focus. iv. Increase Vendor participation and competitiveness that drive finding the best possible product at the best value-point. v. Track and evaluate Vendor performance and aggregate State demand to negotiate and drive down contract pricing. vi. Lower barriers to compete.',
            'answer':'Solution Scalability,Integration'
        },
        {
            'input':'The State of Vermont is seeking an eProcurement Software Solution (“Solution”) that will drive greater process efficiencies throughout the State’s procurement, contracting, and purchasing process by: eliminating redundant software applications in use; integrating and interfacing with the current State financial management system (VISION), related websites and other systems/applications (e.g. VTRANS’ STARS financial management system); reducing manual, paper-based processes and process cycle times; improve Agency and Department/Vendor interactions with use of the Solution',
            'answer':'IT Infrastructure,Integration'
        },
        {
            'input':'The State of Vermont is seeking an eProcurement Software Solution (“Solution”) that will drive greater process efficiencies throughout the State’s procurement, contracting, and purchasing process by: eliminating redundant software applications in use; integrating and interfacing with the current State financial management system (VISION), related websites and other systems/applications (e.g. VTRANS’ STARS financial management system); reducing manual, paper-based processes and process cycle times; improve Agency and Department/Vendor interactions with use of the Solution',
            'answer':'IT Infrastructure,Integration'
        }
    ]
    
    for semantic_chunk in state["chunks"]:
            

            example_prompt = ChatPromptTemplate.from_messages(
                [
                    ("human", "{input}"),
                    ("ai", "{answer}"),
                ]
            )
            few_shot_prompt = FewShotChatMessagePromptTemplate(
                example_prompt=example_prompt,
                examples=examples,
                input_variables=["input"]
            )

            
            final_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", """You are given chunks from a Request for Proposal (RFP) document. Your task is to identify the topics mentioned in each chunk. Some chunks may contain specific criteria for the RFP, while others may be irrelevant and do not contain any criteria or important information. For each chunk, assign one or many of the following topics:
            Description:General description for the request for proposal.
            Sector: The industry or area of activity the RFP pertains to.
            Dates: Important dates for the request for proposal.
            Location: The geographical area where the project or service is to be executed.
            Skills and References: Specific skills and references required for the project.
                Minimum Experience: The minimum experience required from the applicants.
                Required Certifications: The required certifications for the applicants.
                Similar Project References: References of similar projects completed by the applicants.
            Infrastructure: Requirements related to infrastructure for the project.
                IT Infrastructure: Requirements related to IT infrastructure.
                Network Infrastructure: Requirements related to network infrastructure.
                Virtualization: Requirements related to virtualization.
            Technical Skills: Specific technical skills required for the project.
                Programming Languages: The programming languages required for the project.
                Cloud Computing, Data Management, AI Skills: Skills in cloud computing, data management, and AI.
                Cybersecurity, DevOps, Big Data Skills: Skills in cybersecurity, DevOps, and big data.
                IoT, Network, Telecommunications, Blockchain Skills: Skills in IoT, networks, telecommunications, and blockchain.
                Automation, Orchestration, Data Analysis Skills: Skills in automation, orchestration, and data analysis.
                Others: Any other technical skills not specified above.
            Requested Solution Quality: Quality attributes required for the solution.
                Technical Support and Maintenance: Requirements related to technical support and maintenance.
                Reliability: Requirements related to reliability.
                Flexibility: Requirements related to flexibility.
                Integrity: Requirements related to integrity.
                Availability: Requirements related to availability.
                Solution Scalability: Requirements related to scalability.
                Others: Any other quality attributes not specified above.
            Project Management and Resources: Requirements related to project management and resources.
                Project Management Approaches: The project management approaches to be followed.
                Project Management Tools: The use of specific project management tools.
                Development Methods: The development methodologies to be followed.
                Project Resources: Resources required for the project.
                Training: Training requirements.
            Deployment: Requirements related to deployment.
            
            Legal Compliance: The need to comply with specific legal requirements.
            Regulations: Requirements related to compliance with governmental laws and regulations.
            If the chunk does not contain any relevant RFP criteria, return "Irrelevant."

            Instructions:

           1. Analyze each chunk of text provided.
            2. Assign the appropriate topics from the list above or "Irrelevant" if the chunk does not contain any relevant RFP criteria.
            4. Format your answer exactly as shown in the examples provided, strictly listing the topics without producing paragraphs in this way :topic1,topic2...
            5. Even if the chunk contains some keywords about a topic or even one keyword, assign that topic to that chunk."""),
                    few_shot_prompt,
                    ("human", "{input}"),
                ]
            )

           
            chain =LLMChain(llm=mistrallarge,prompt=final_prompt)

            response = chain.invoke({"input":semantic_chunk})
            print(response)
            """print(f"chunk:{semantic_chunk}")
            print(f"answer:{response.content}")"""
            if "Description" in response['text']:
                state["pdf_data"]["Description"].append(semantic_chunk)
            if "Sector" in response['text']:
                state["pdf_data"]["Sector"].append(semantic_chunk)
            if "Dates" in response['text']:
                state["pdf_data"]["Dates"].append(semantic_chunk)
            if "Location" in response['text']:
                state["pdf_data"]["Location"].append(semantic_chunk)
            if "Required Certifications" in response['text']:
                state["pdf_data"]["Skills and References"]["Required Certifications"].append(semantic_chunk)
            if "Minimum Experience" in response['text']:
                state["pdf_data"]["Skills and References"]["Minimum Experience"].append(semantic_chunk)
            if "Similar Project References" in response['text']:
                state["pdf_data"]["Skills and References"]["Similar Project References"].append(semantic_chunk)
            if "Programming Languages" in response['text']:
                state["pdf_data"]["Technical Skills"]["Programming Languages"].append(semantic_chunk)
            if "Cloud Computing, Data Management, AI Skills" in response['text']:
                state["pdf_data"]["Technical Skills"]["Cloud Computing, Data Management, AI Skills"].append(semantic_chunk)
            if "Cybersecurity, DevOps, Big Data Skills" in response['text']:
                state["pdf_data"]["Technical Skills"]["Cybersecurity, DevOps, Big Data Skills"].append(semantic_chunk)
            if "IoT, Network, Telecommunications, Blockchain Skills" in response['text']:
                state["pdf_data"]["Technical Skills"]["IoT, Network, Telecommunications, Blockchain Skills"].append(semantic_chunk)
            if "Automation, Orchestration, Data Analysis Skills" in response['text']:
                state["pdf_data"]["Technical Skills"]["Automation, Orchestration, Data Analysis Skills"].append(semantic_chunk)
            if "IT Infrastructure" in response['text']:
                state["pdf_data"]["Infrastructure"]["IT Infrastructure"].append(semantic_chunk)
            if "Network Infrastructure" in response['text']:
                state["pdf_data"]["Infrastructure"]["Network Infrastructure"].append(semantic_chunk)
            if "Virtualization" in response['text']:
                state["pdf_data"]["Infrastructure"]["Virtualization"].append(semantic_chunk)
            if "Deployment" in response['text']:
                state["pdf_data"]["Deployment"].append(semantic_chunk)
            if "Technical Support and Maintenance" in response['text']:
                state["pdf_data"]["Requested Solution Quality"]["Technical Support and Maintenance"].append(semantic_chunk)
            if "Reliability" in response['text']:
                state["pdf_data"]["Requested Solution Quality"]["Reliability"].append(semantic_chunk)
            if "Flexibility" in response['text']:
                state["pdf_data"]["Requested Solution Quality"]["Flexibility"].append(semantic_chunk)
            if "Integrity" in response['text']:
                state["pdf_data"]["Requested Solution Quality"]["Integrity"].append(semantic_chunk)
            if "Availability" in response['text']:
                state["pdf_data"]["Requested Solution Quality"]["Availability"].append(semantic_chunk)
            if "Solution Scalability" in response['text']:
                state["pdf_data"]["Requested Solution Quality"]["Solution Scalability"].append(semantic_chunk)
            if "Training" in response['text']:
                state["pdf_data"]["Project Management and Resources"]["Training"].append(semantic_chunk)
            if "Project Resources" in response['text']:
                state["pdf_data"]["Project Management and Resources"]["Project Resources"].append(semantic_chunk)
            if "Project Management Approaches" in response['text']:
                state["pdf_data"]["Project Management and Resources"]["Project Management Approaches"].append(semantic_chunk)
            if "Use of Project Management Tools" in response['text']:
                state["pdf_data"]["Project Management and Resources"]["Project Management Tools"].append(semantic_chunk)
            if "Development Methodologies" in response['text']:
                state["pdf_data"]["Project Management and Resources"]["Development Methods"].append(semantic_chunk)
            if "Legal Compliance" in response['text']:
                state["pdf_data"]["Legal Compliance"].append(semantic_chunk)
            if "Regulations" in response['text']:
                state["pdf_data"]["Regulations"].append(semantic_chunk)
            


    return state


def process_key(key, data, pdf_json,examples,model,parent_key=None):
    if isinstance(data, dict):
        for sub_key in data:
            process_key(sub_key, data[sub_key],pdf_json, examples[key][sub_key],model,parent_key=key)
    else:
        
        context_chunks = "\n\n".join(data)
        example_prompt = ChatPromptTemplate.from_messages(
            [
                ("human", "{input}"),
                ("ai", "{output}"),
            ]
        )

        exampleskey = examples if isinstance(examples, list) else []

        few_shot_prompt = FewShotChatMessagePromptTemplate(
            example_prompt=example_prompt,
            examples=exampleskey,
            input_variables=["input"]
        )

        if key!= 'Location' and key!="Description":
            final_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", f"""Given multiple chunks from a request for proposal (RFP) mentioning the {key}, extract all relevant mentions of the {key} clearly and output a summary paragraph where you simplify and explain them clearly like an expert.

                    Instructions:
                    - Identify and extract relevant information related to the {key} from the provided chunks.
                    - Formulate a summary incorporating the extracted information.
                    - The summary should be a paragraph that contains all relevant information in detail, presented in a comprehensive way.
                    - Format the output like this: summary paragraph.
                    - If there are no available information about the {key} return 'null'not([])
                    
                    """),
                    few_shot_prompt,
                    ("human", "{input}"),
                ]
            )
        else:
            if key=="Location":
                final_prompt = ChatPromptTemplate.from_messages(
                    [
                        ("system", f"""Given multiple chunks from a request for proposal (RFP) mentioning the {key}, extract the location.

                        Instructions:
                        - Extract the location (city and state) and format it as 'City, State'.
                        - Format the output like this: 'City, State'
                        - If location is not mentioned return 'null' 
                        """),
                        few_shot_prompt,
                        ("human", "{input}"),
                    ]
                )
            elif key=="Description":
                final_prompt = ChatPromptTemplate.from_messages(
                    [
                        ("system", f"""You are provided with multiple chunks from a request for proposal (RFP) that reference the {key}. Your task is to extract the critical information and deliver it in a single, concise sentence.

                        Instructions:
                        - Identify and extract the essential details related to the {key}.
                        - Format your response as a clear, informative sentence that encapsulates the key information.
                        - Ensure the sentence is comprehensive yet succinct, conveying all necessary details in one sentence."""),
                        few_shot_prompt,
                        ("human", "{input}"),
                    ]
                )

        chain = LLMChain(llm=model, prompt=final_prompt)
        
        if len(data) > 0:
            response =  chain.invoke({"input": context_chunks, 'key': key})
            if(parent_key!=None):
                pdf_json[parent_key][key] = response['text']
            else:
                pdf_json[key]=response['text']
            #print(response)
def generate_pdf_json(state: State) -> State:
    chain_gpt_4o_mini = ChatOpenAI(model="gpt-4o-mini", max_tokens=1500,temperature=0.4)
    mistrallarge =ChatMistralAI(model='open-mixtral-8x22b')

    #chain_gpt_4o = ChatOpenAI(model="gpt-4o", max_tokens=3000)
    state["pdf_json"] = {
        "Description":"",
        "Sector":"",
        "Dates": "",
        "Location": "",
        "Skills and References": {
            "Minimum Experience": "",
            "Required Certifications": "",
            "Similar Project References": ""
        },
        "Infrastructure": {
            "IT Infrastructure": "",
            "Network Infrastructure": "",
            "Virtualization": ""
        },
        "Technical Skills": {
            "Programming Languages": "",
            "Cloud Computing, Data Management, AI Skills": "",
            "Cybersecurity, DevOps, Big Data Skills": "",
            "IoT, Network, Telecommunications, Blockchain Skills": "",
            "Automation, Orchestration, Data Analysis Skills": "",
            "Others": ""
        },
        "Requested Solution Quality": {
            "Technical Support and Maintenance": "",
            "Reliability": "",
            "Flexibility": "",
            "Integrity": "",
            "Availability": "",
            "Solution Scalability": "",
            "Others": ""
        },
        "Project Management and Resources": {
            "Project Management Approaches": "",
            "Project Management Tools": "",
            "Development Methods": "",
            "Project Resources": "",
            "Training": ""
        },
        "Deployment": "",
        "Regulations": "",
        "Legal Compliance": ""
    }
    examples = {
    "Description": [{
        "input": [
            "The contractor must deliver a complete solution that encompasses software, hardware, and ongoing support services.",
            "The project phases include initial development, staged deployment, and continuous maintenance.",
            "The solution should adhere to industry standards and regulatory requirements, emphasizing high reliability, scalability, and robust technical support."
        ],
        "output": "The RFP is for a complete solution covering software, hardware, and support services. It includes development, staged deployment, and ongoing maintenance phases. The solution must meet industry standards and regulatory requirements, focusing on reliability, scalability, and strong technical support."
    }],
    "Dates": [{
        "input": [
            "All proposals must be submitted by September 30, 2024.",
            "Late submissions will not be considered.",
            "The deadline for questions is September 15, 2024."
        ],
        "output": "The proposals must be submitted by September 30, 2024. Late submissions will not be accepted, and the deadline for questions is September 15, 2024."
    }],
    "Location": [{
    "input": [
        "The project will be conducted at our New York office.",
        "Remote work is permitted, but occasional on-site visits are required.",
        "International firms are welcome to apply, but must have a local presence."
    ],
    "output": "New York, New York"
    }],
    "Skills and References": {
        "Minimum Experience": [{
            "input": [
                "The vendor must have at least 5 years of experience in the field.",
                "Experience with large-scale healthcare projects is required.",
                "Prior work with government health agencies is a plus."
            ],
            "output": "The vendor must have at least 5 years of experience, with experience in large-scale healthcare projects and prior work with government health agencies preferred."
        }],
        "Required Certifications": [{
            "input": [
                "Vendors must be ISO 9001 certified.",
                "Cybersecurity certification such as CISSP is required.",
                "Healthcare IT certifications like CPHIMS are preferred."
            ],
            "output": "ISO 9001, CISSP, and healthcare IT certifications like CPHIMS are preferred."
        }],
        "Similar Project References": [{
            "input": [
                "Provide references for at least three similar projects completed in the last five years.",
                "References must include contact information for verification.",
                "Projects should be similar in scope and complexity to the proposed project."
            ],
            "output": "Provide references for at least three similar projects completed in the last five years, including contact information for verification."
        }]
    },
    "Infrastructure": {
        "IT Infrastructure": [{
            "input": [
                "The project requires robust IT infrastructure capable of supporting 24/7 operations.",
                "Must include high availability systems with disaster recovery capabilities.",
                "Scalable server architecture to handle increasing loads is necessary."
            ],
            "output": "The project requires robust IT infrastructure with 24/7 operations, high availability systems, disaster recovery capabilities, and scalable server architecture."
        }],
        "Network Infrastructure": [{
            "input": [
                "A secure and redundant network infrastructure is required.",
                "Must support high-speed data transfer and connectivity.",
                "Ensure compliance with industry security standards."
            ],
            "output": "The project requires a secure, redundant network infrastructure supporting high-speed data transfer and connectivity, with compliance to industry security standards."
        }],
        "Virtualization": [{
            "input": [
                "Utilize virtualization technologies to optimize resource usage.",
                "Support for virtual machines and containerization is necessary.",
                "Must be compatible with our existing IT infrastructure."
            ],
            "output": "Utilize virtualization technologies with support for virtual machines and containerization, ensuring compatibility with existing IT infrastructure."
        }]
    },
    "Technical Skills": {
        "Programming Languages": [{
            "input": [
                "Proficiency in Python, Java, and C++ is required.",
                "Experience with modern web development frameworks such as React and Angular.",
                "Ability to develop and maintain robust codebases."
            ],
            "output": "Proficiency in Python, Java, and C++ is required, along with experience in modern web development frameworks like React and Angular."
        }],
        "Cloud Computing, Data Management, AI Skills": [{
            "input": [
                "Experience with AWS, Azure, and Google Cloud platforms is essential.",
                "Knowledge of big data technologies like Hadoop and Spark.",
                "Proficiency in AI and machine learning tools such as TensorFlow and PyTorch."
            ],
            "output": "Experience with AWS, Azure, Google Cloud, big data technologies like Hadoop and Spark, and AI/ML tools like TensorFlow and PyTorch is essential."
        }],
        "Cybersecurity, DevOps, Big Data Skills": [{
            "input": [
                "Strong understanding of cybersecurity principles and practices.",
                "Experience with DevOps tools like Jenkins, Docker, and Kubernetes.",
                "Knowledge of big data analytics and data warehousing solutions."
            ],
            "output": "Strong understanding of cybersecurity, DevOps tools (Jenkins, Docker, Kubernetes), and big data analytics/warehousing solutions."
        }],
        "IoT, Network, Telecommunications, Blockchain Skills": [{
            "input": [
                "Experience with IoT device management and integration.",
                "Proficiency in network design and telecommunications.",
                "Knowledge of blockchain technology and its applications."
            ],
            "output": "Experience with IoT device management, network design, telecommunications, and blockchain technology."
        }],
        "Automation, Orchestration, Data Analysis Skills": [{
            "input": [
                "Proficiency in automation tools like Ansible and Puppet.",
                "Experience with orchestration platforms like Kubernetes.",
                "Strong data analysis skills using tools like R, Python, and SQL."
            ],
            "output": "Proficiency in automation tools (Ansible, Puppet), orchestration platforms (Kubernetes), and strong data analysis skills (R, Python, SQL)."
        }],
        "Others": [{
            "input": [
                "Familiarity with emerging technologies like quantum computing.",
                "Ability to adapt to rapidly changing technological landscapes.",
                "Strong problem-solving and analytical skills."
            ],
            "output": "Familiarity with emerging technologies like quantum computing, adaptability to technological changes, and strong problem-solving skills."
        }]
    },
    "Requested Solution Quality": {
        "Technical Support and Maintenance": [{
        "input": [
            "Provide 24/7 technical support for the deployed solution.",
            "Include maintenance contracts for regular updates and fixes.",
            "Support should cover both software and hardware aspects."
        ],
        "output": "Provide 24/7 technical support, maintenance contracts for regular updates and fixes, covering both software and hardware."
        }],
        "Reliability": [{
            "input": [
                "The solution must ensure 99.99% uptime.",
                "Implement redundancy and failover mechanisms.",
                "Consistent performance under varying loads is essential."
            ],
            "output": "The solution must ensure 99.99% uptime, implement redundancy and failover mechanisms, and maintain consistent performance under varying loads."
        }],
        "Flexibility": [{
            "input": [
                "The solution should be adaptable to changing business needs.",
                "Support for multiple platforms and environments is necessary.",
                "Easily configurable to accommodate future requirements."
            ],
            "output": "The solution should be adaptable to changing business needs, support multiple platforms/environments, and be easily configurable for future requirements."
        }],
        "Integrity": [{
            "input": [
                "Data integrity and security must be ensured at all times.",
                "Implement end-to-end encryption and secure access controls.",
                "Regular audits and compliance checks are required."
            ],
            "output": "Ensure data integrity and security with end-to-end encryption, secure access controls, and regular audits/compliance checks."
        }],
        "Availability": [{
            "input": [
                "The system must be available 24/7 with minimal downtime.",
                "Implement high availability and disaster recovery solutions.",
                "Ensure quick recovery times in case of failures."
            ],
            "output": "The system must be available 24/7 with minimal downtime, high availability, disaster recovery solutions, and quick recovery times."
        }],
        "Solution Scalability": [{
            "input": [
                "The solution must scale to handle increasing user loads.",
                "Support for horizontal and vertical scaling is required.",
                "Seamless integration with existing systems is essential."
            ],
            "output": "The solution must scale to handle increasing user loads, support horizontal and vertical scaling, and integrate seamlessly with existing systems."
        }],
        "Others": [{
            "input": [
                "Ensure user-friendly interfaces and seamless user experience.",
                "Incorporate feedback mechanisms for continuous improvement.",
                "Adherence to industry standards and best practices is required."
            ],
            "output": "Ensure user-friendly interfaces, seamless user experience, feedback mechanisms for continuous improvement, and adherence to industry standards."
        }]
    },
    "Project Management and Resources": {
        "Project Management Approaches": [{
            "input": [
                "Utilize Agile methodologies for project management.",
                "Experience with Scrum and Kanban frameworks is preferred.",
                "Ability to adapt management approach based on project needs."
            ],
            "output": "Utilize Agile methodologies, with preferred experience in Scrum and Kanban frameworks, and adaptability in management approaches."
        }],
        "Project Management Tools": [{
            "input": [
                "Proficiency in project management tools like Jira and Trello.",
                "Experience with MS Project and Asana is also beneficial.",
                "Ability to customize tools to fit project requirements."
            ],
            "output": "Proficiency in Jira and Trello, with experience in MS Project and Asana, and ability to customize tools to fit project needs."
        }],
        "Development Methods": [{
            "input": [
                "Adopt DevOps practices for continuous integration and delivery.",
                "Experience with Test-Driven Development (TDD) is preferred.",
                "Use of version control systems like Git is required."
            ],
            "output": "Adopt DevOps practices, with preferred experience in TDD, and required use of version control systems like Git."
        }],
        "Project Resources": [{
            "input": [
                "Adequate resources must be allocated for project success.",
                "Include skilled personnel, budget, and technological tools.",
                "Resource planning should align with project milestones."
            ],
            "output": "Allocate adequate resources including skilled personnel, budget, and technological tools, with resource planning aligned to project milestones."
        }],
        "Training": [{
            "input": [
                "Provide training sessions for team members on new technologies.",
                "Training materials should be comprehensive and accessible.",
                "Ongoing support and learning opportunities are necessary."
            ],
            "output": "Provide training on new technologies with comprehensive materials, and ensure ongoing support and learning opportunities."
        }]
    },
    "Deployment": [{
        "input": [
            "The deployment process must include testing in a staging environment.",
            "Rollout should be gradual to minimize disruption.",
            "Post-deployment support and monitoring are required."
        ],
        "output": "The deployment process must include staging environment testing, gradual rollout, and post-deployment support and monitoring."
    }],
    "Regulations": [{
        "input": [
            "Ensure compliance with governmental regulations and industry-specific standards.",
            "Adhere to national and international regulatory requirements.",
            "Include clauses in contracts for compliance with regulatory bodies."
        ],
        "output": "Ensure compliance with governmental regulations, national and international regulatory requirements, and include compliance clauses in contracts."
    }],

    "Legal Compliance": [{
        "input": [
            "Ensure adherence to legal requirements related to data protection and privacy.",
            "Include specific clauses in contracts for legal obligations like GDPR and intellectual property rights.",
            "Adhere to legal standards for operational practices and industry norms."
        ],
        "output": "Ensure adherence to legal requirements for data protection, privacy, intellectual property rights, and include appropriate clauses in contracts. Adhere to legal standards for operational practices and industry norms."
    }]

    }

    for key in state["pdf_data"]:
        process_key(key, state["pdf_data"][key],state["pdf_json"], examples,chain_gpt_4o_mini)
        
    return state

