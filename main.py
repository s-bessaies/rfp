import os
import mesop as me
from workflow import States, app
import random
import time
import mesop.labs as mel

# Define the directory to save uploaded files
UPLOAD_DIR = "./uploads"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

@me.stateclass
class State:
    input: str 
    output: str 
    in_progress: bool 
    file: me.UploadedFile 
    file_path: str 

def handle_upload(event: me.UploadEvent):
    """Handle file upload event."""
    state = me.state(State)
    if event.file:
        state.file = event.file
        local_path = save_file_to_local(event.file)
        state.file_path = local_path
    else:
        print("No file uploaded")


def save_file_to_local(file: me.UploadedFile) -> str:
    """Save uploaded file to local directory."""
    file_path = os.path.join(UPLOAD_DIR, file.name)
    with open(file_path, "wb") as f:
        f.write(file.getvalue())
    return file_path

@me.page()
def page():
    """Define the main page structure."""
    try:
        state = me.state(State)
        print(f"Initial State: {state}")
        with me.box(
            style=me.Style(
                background="#fff",
                min_height="calc(100% - 48px)",
                padding=me.Padding(bottom=16),
            )
        ):
            with me.box(
                style=me.Style(
                    width="min(720px, 100%)",
                    margin=me.Margin.symmetric(horizontal="auto"),
                    padding=me.Padding.symmetric(horizontal=16),
                )
            ):
                header_text()
                chat_input()
                output()
        footer()
    except Exception as e:
        print(f"Error in page rendering: {e}")
def header_text():
    """Render the header text."""
    with me.box(
        style=me.Style(
            padding=me.Padding(top=64, bottom=36),
        )
    ):
        me.text(
            "Mesop Starter Kit",
            style=me.Style(
                font_size=36,
                font_weight=700,
                background="linear-gradient(90deg, #4285F4, #AA5CDB, #DB4437) text",
                color="transparent",
            ),
        )

def example_box(example: str, is_mobile: bool):
    """Render an example box."""
    with me.box(
        style=me.Style(
            width="100%" if is_mobile else 200,
            height=140,
            background="#F0F4F9",
            padding=me.Padding.all(16),
            font_weight=500,
            line_height="1.5",
            border_radius=16,
            cursor="pointer",
        ),
        key=example,
        on_click=click_example_box,
    ):
        me.text(example)

def click_example_box(e: me.ClickEvent):
    """Handle click on example box."""
    state = me.state(State)
    state.input = e.key

def chat_input():
    """Render the chat input area."""
    state = me.state(State)
    with me.box(
        style=me.Style(
            border_radius=16,
            padding=me.Padding.all(8),
            background="#e2e8f0",
            display="flex",
            width="100%",
        )
    ):
        with me.box(
            style=me.Style(
                flex_grow=1,
            )
        ):
            me.native_textarea(
                autosize=True,
                min_rows=4,
                placeholder="Enter your text here...",
                on_blur=textarea_on_blur,
                style=me.Style(
                    padding=me.Padding(top=16, left=16),
                    background="#e2e8f0",
                    outline="none",
                    width="100%",
                    overflow_y="auto",
                    border=me.Border.all(me.BorderSide(style="none")),
                ),
            )
        me.uploader(
            label="Upload PDF",
            accepted_file_types=["application/pdf"],
            on_upload=handle_upload,
            type="flat",
            color="primary",
            style=me.Style(font_weight="bold"),
        )

        if state.file and state.file.size:
            with me.box(style=me.Style(margin=me.Margin.all(10))):
                me.text(f"File name: {state.file.name}")
                me.text(f"File size: {state.file.size}")
                me.text(f"File type: {state.file.mime_type}")

            with me.box(style=me.Style(margin=me.Margin.all(10))):
                me.text(f"PDF file uploaded and saved to: {state.file_path}")

        with me.content_button(type="icon", on_click=click_send):
            me.icon("send")

def textarea_on_blur(e: me.InputBlurEvent):
    """Handle textarea blur event."""
    state = me.state(State)
    state.input = e.value

def click_send(e: me.ClickEvent):
    """Handle send button click."""
    state = me.state(State)
    if not state.input:
        return
    state.in_progress = True
    input_text = state.input
    state.input = ""
    state.output = ""

    # Call the API with the input text
    state.output = call_api(input_text)

    state.in_progress = False

def call_api(input_text):
    """Simulate API call with the input text."""
    state = me.state(State)
    initstate = States(pdf_name=state.file_path, workflow_steps=0)
    for output in app.stream(initstate):
        for key, value in output.items():
            print(f"========== {key} output: ========")
            print("aaakfjslfdjqsfdlk", value)
            final_state = value
    return final_state["response"]

def output():
    """Render the output area."""
    state = me.state(State)
    if state.output or state.in_progress:
        with me.box(
            style=me.Style(
                background="#F0F4F9",
                padding=me.Padding.all(16),
                border_radius=16,
                margin=me.Margin(top=36),
            )
        ):
            if state.output:
                me.markdown(state.output)

def footer():
    """Render the footer."""
    with me.box(
        style=me.Style(
            position="sticky",
            bottom=0,
            padding=me.Padding.symmetric(vertical=16, horizontal=16),
            width="100%",
            background="#F0F4F9",
            font_size=14,
        )
    ):
        me.html(
            "Made with <a href='https://google.github.io/mesop/'>Mesop</a>",
        )





def on_load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  path="/chat",
  title="Mesop Demo Chat",
  on_load=on_load,
)
def page():
  mel.chat(transform, title="Mesop Demo Chat", bot_user="Mesop Bot")


def transform(input: str, history: list[mel.ChatMessage]):
  for line in random.sample(LINES, random.randint(3, len(LINES) - 1)):
    time.sleep(0.3)
    yield line + " "


LINES = [
  "Mesop is a Python-based UI framework designed to simplify web UI development for engineers without frontend experience.",
  "It leverages the power of the Angular web framework and Angular Material components, allowing rapid construction of web demos and internal tools.",
  "With Mesop, developers can enjoy a fast build-edit-refresh loop thanks to its hot reload feature, making UI tweaks and component integration seamless.",
  "Deployment is straightforward, utilizing standard HTTP technologies.",
  "Mesop's component library aims for comprehensive Angular Material component coverage, enhancing UI flexibility and composability.",
  "It supports custom components for specific use cases, ensuring developers can extend its capabilities to fit their unique requirements.",
  "Mesop's roadmap includes expanding its component library and simplifying the onboarding processs.",
]