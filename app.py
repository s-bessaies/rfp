import os
import chainlit as cl
from typing_extensions import TypedDict
from typing import List, Dict
from langchain_core.runnables import Runnable

import graph
welcome_message = """To get started:
1. Upload a Request for proposal (PDF)
"""
from langgraph.graph import StateGraph

class State(TypedDict):
    pdf_name: str
    workflow_steps: int
    chunks: List[str]
    pdf_data: Dict[str, List[str]]
    pdf_json: Dict[str, str]

@cl.on_chat_start
async def main():
    workflow = StateGraph(State)

    workflow.add_node("init", graph.function_init)
    workflow.add_edge('init', 'extract_text_from_pdf')

    workflow.add_node("extract_text_from_pdf", graph.extract_text_from_pdf)
    workflow.add_edge('extract_text_from_pdf', 'group chunks')

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
            content="Please upload a PDF file to begin!", 
            accept=["application/pdf"]
        ).send()
    
    if files is not None:
        file = files[0]
        initstate = State(pdf_name=file.path, workflow_steps=0, chunks=[], pdf_data={}, pdf_json={})
        g: Runnable = cl.user_session.get("graph")
        
        try:
            pdf_json={}
            async for output in g.astream(initstate):
                for key, value in output.items():
                    print(f"========== {key} output: ========")
                    print(value)
                    pdf_json=value['pdf_json']
                print(">>>\n\n")
            print(pdf_json)

            '''if pdf_json:
                for key, value in pdf_json.items():
                    await cl.Message(content=value).send()
            else:
                await cl.Message(content="No content was extracted from the PDF. Please check the file and try again.").send()'''
        except Exception as e:
            await cl.Message(content=f"An error occurred while processing the PDF: {e}").send()
