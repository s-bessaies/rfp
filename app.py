from dotenv import load_dotenv
import chainlit as cl
from typing_extensions import TypedDict
from typing import List, Dict
from langchain_core.runnables import Runnable
import graph
from langgraph.graph import StateGraph
from langfuse.callback import CallbackHandler
from langchain_experimental.text_splitter import SemanticChunker
from langchain_mistralai import MistralAIEmbeddings
from langchain.document_loaders import PyPDFLoader


load_dotenv()
class State(TypedDict):
    
    workflow_steps: int
    chunks: List[str]
    pdf_data: Dict[str, List[str]]
    pdf_json: Dict[str, str]

@cl.on_chat_start
async def main():
    workflow = StateGraph(State)

    workflow.add_node("init", graph.function_init)
    workflow.add_edge('init', 'group chunks')

    workflow.add_node("group chunks", graph.group_chunk_by_category)
    workflow.add_edge('group chunks', 'generate json')

    workflow.add_node("generate json", graph.generate_pdf_json)
    workflow.add_edge("generate json", "log_state")

    workflow.add_node("log_state", graph.log_state)

    workflow.set_entry_point("init")
    workflow.set_finish_point("log_state")

    cl.user_session.set("graph", workflow.compile())


    files = None
    while files is None:
        files = await cl.AskFileMessage(
            content="Please upload a Request for Proposal to begin!", 
            accept=["application/pdf"],
            
        ).send()
    langfuse_handler=CallbackHandler()
    if files is not None:
        loading_message = await cl.Message(content="Reading the PDF, please wait... ⏳").send()
        file = files[0]
        loader = PyPDFLoader(file.path)
        documents = loader.load()  
        mistral = MistralAIEmbeddings(
            model="mistral-embed",
        )
        text_splitter = SemanticChunker(mistral, breakpoint_threshold_type="standard_deviation")
        semantic_chunks = text_splitter.create_documents([d.page_content for d in documents])
        chunks = [semantic_chunk.page_content for semantic_chunk in semantic_chunks]
        initstate = State(workflow_steps=0, chunks=chunks, pdf_data={}, pdf_json={})
        g: Runnable = cl.user_session.get("graph")
        loading_message = await cl.Message(content="Analyzing the PDF..").send()
        
        pdf_json = {}
        try:
            async for output in g.astream(initstate,config={"callbacks": [langfuse_handler]}):
                for key, value in output.items():
                    print(f"========== {key} output: ========")
                    print(value)
                    pdf_json = value['pdf_json']
                print(">>>\n\n")
            print(pdf_json)
            #await loading_message.update(content="Processing complete! 🎉")

            
            
        except Exception as e:
            await loading_message.update(content=f"An error occurred while processing the PDF: {e}")
        if pdf_json:
                loading_message = await cl.Message(content="Analysis complete.").send()

                try:
                    for key, value in pdf_json.items():
                        if isinstance(value, dict):
                            if value is not None:
                                for sub_key in value:
                                    if value[sub_key] is not None:
                                        await cl.Message(content=value[sub_key]).send()
                        else:
                            if value is not None:
                                await cl.Message(content=value).send()
                except Exception as e:
                    print(f"Error sending message: {e}")

if __name__ == "__main__":
    cl.start(main)
