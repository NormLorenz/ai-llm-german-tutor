import enum
import os
from typing import Generator
from dotenv import load_dotenv
from openai import OpenAI
import anthropic
import google.generativeai
import gradio as gr


# Load environment variables in a file called .env
load_dotenv(override=True)

# Get API keys from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')


# Connect to OpenAI, Anthropic and Google
openai = OpenAI()
claude = anthropic.Anthropic()
google.generativeai.configure()

# Define the CEFR levels and descriptions
level_options = ["A1 (Beginner)", "A2 (Elementary)",
                 "B1 (Intermediate)", "B2 (Upper Intermediate)", "C1 (Advanced)", "C2 (Proficient)"]

# Descriptions for each CEFR level
level_descriptions = {
    "A1 (Beginner)": "Basic phrases and everyday expressions. Simple personal details.",
    "A2 (Elementary)": "Familiar expressions for basic routines. Simple communication about immediate needs.",
    "B1 (Intermediate)": "Main points on familiar matters. Simple connected text on familiar topics.",
    "B2 (Upper Intermediate)": "Understanding complex text. Spontaneous interaction with native speakers.",
    "C1 (Advanced)": "Understanding demanding, longer texts. Expressing ideas fluently and spontaneously.",
    "C2 (Proficient})": "Understand almost everything heard or read. Can speak in complex situations."
}

# A generic system message
system_message = "This assistant helps users practice conversational German in a friendly, supportive way. \
It adapts to the user's level, offers corrections when asked, and keeps the tone light and encouraging. \
The assistant may switch between English and German as needed. Please start the conversation by asking the \
user a question in German. If the user says 'bye' or 'tschüss', end the conversation and say goodbye to the \
user in German. Also correct any mistakes the user makes."


# Defaults
MODEL_DEFAULT: str = "gpt-4o-mini"
PROFICIENCY_DEFAULT: str = "A1"
VERBOSE_DEFAULT: bool = True


def main() -> None:

    ### High level entry point ###
    verbose_option = gr.Checkbox(
        label="Check if you wish to have English added to the response:", value=VERBOSE_DEFAULT)

    proficiency_option = gr.Radio(
        ["A1", "A2", "B1", "B2", "C1", "C2"],
        label="Choose a language proficiency CERF level:", value=PROFICIENCY_DEFAULT
    )

    model_option = gr.Radio(

        ["gpt-4o-mini", "claude-3-5-haiku-latest",
            "gemini-1.5-flash", "gemini-2.5-flash-lite"],
        label="Choose an AI model:", value=MODEL_DEFAULT
    )

    description = "> This assistant helps users practice conversational German in a friendly, \
    supportive way. It adapts to the user's level, offers corrections when asked, and keeps \
    the tone light and encouraging."

    examples = [
        "What is the meaning of life?",
        "Fun things to do in Sandpoint, Idaho?",
        "Interpret 'The Road Not Taken' by Robert Frost"
    ]

    gr.ChatInterface(fn=chat, additional_inputs=[verbose_option, proficiency_option, model_option], type="messages",
                     title="My German Tutor", description=description).launch(inbrowser=True, share=False)


def chat(user: str, history: list[tuple[str, str]], verbose_option: bool, proficiency_option: str, model_option: str) -> Generator[str, None, None]:

    # Initial yield to avoid Gradio timeout
    yield ""

    # Check if the user wants to exit
    if user.lower().strip() == 'bye' or user.lower().strip() == 'tschüss':

        # Close the browser window and stop the application - BROKEN
        gr.close_all()
        exit()

    system: str = system_message

    # Add specific instructions based upon the verbose checkbox
    if verbose_option:
        system += " Also please show responses in both German and English."

    # Add specific instructions based upon the CEFR level
    system += f" Please use the CEFR level {proficiency_option} for vocabulary and grammar."

    # Call the appropriate model
    if model_option == "gpt-4o-mini":
        result = call_openai(system, history, user, model_option)
        yield from result
    elif model_option == "claude-3-5-haiku-latest":
        result = call_anthropic(system, history, user, model_option)
        yield from result


def call_openai(system: str, history, user: str, model: str):

    # Initial yield to avoid Gradio timeout
    yield ""

    # Prepare messages for OpenAI
    messages = [{"role": "system", "content": system}] + \
        history + [{"role": "user", "content": user}]

    # Call the OpenAI API with streaming
    stream = openai.chat.completions.create(
        model=model,
        messages=messages,
        stream=True
    )

    # Stream the response back to the user
    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ""
        yield response


def call_anthropic(system: str, history: list[tuple[str, str]], user: str, model: str) -> Generator[str, None, None]:

    # Initial yield to avoid Gradio timeout
    yield ""

    # Prepare messages for Anthropic
    keys_to_keep = ["role", "content"]
    history = [{k: d[k] for k in keys_to_keep if k in d} for d in history]
    history.append({"role": "user", "content": user})
    if len(history) > 20:
        history.append({"role": "user", "content": "DONE"})

    # Call the Anthropic API with streaming
    response = ""
    with claude.messages.stream(
        model=model,
        max_tokens=1024,
        messages=history,
        system=system
    ) as stream:
        for text in stream.text_stream:
            response += text
            yield response


def call_google(prompt: str, model: str):

    # Initial yield to avoid Gradio timeout
    yield ""

    # Call the Gemini API with streaming
    gemini = google.generativeai.GenerativeModel(
        model_name=model,
        system_instruction=system_message
    )

    # Stream the response back to the user
    response = ""
    for response in gemini.generate_content(prompt, stream=True):
        response += response.text or ""
        yield response


if __name__ == "__main__":
    main()
