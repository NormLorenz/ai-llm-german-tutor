import os
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
                 "B1 (Intermediate)", "B2 (Upper Intermediate)", "C1 (Advanced)"]

# Descriptions for each CEFR level
level_descriptions = {
    "A1 (Beginner)": "Basic phrases and everyday expressions. Simple personal details.",
    "A2 (Elementary)": "Familiar expressions for basic routines. Simple communication about immediate needs.",
    "B1 (Intermediate)": "Main points on familiar matters. Simple connected text on familiar topics.",
    "B2 (Upper Intermediate)": "Understanding complex text. Spontaneous interaction with native speakers.",
    "C1 (Advanced)": "Understanding demanding, longer texts. Expressing ideas fluently and spontaneously."
}

# A generic system message
system_message = "This assistant helps users practice conversational German in a friendly, supportive way. \
It adapts to the user's level, offers corrections when asked, and keeps the tone light and encouraging. \
The assistant may switch between English and German as needed. Please start the conversation by asking the \
user a question in German. If the user says 'bye' or 'tschüss', end the conversation and say goodbye to the \
user in German."

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

    description = "This assistant helps users practice conversational German in a friendly, \
    supportive way. It adapts to the user's level, offers corrections when asked, and keeps \
    the tone light and encouraging."

    gr.ChatInterface(fn=chat, additional_inputs=[verbose_option, proficiency_option, model_option], type="messages",
                     title="My German Tutor", description=description).launch(inbrowser=True, share=False)


def chat(message, history, verbose_option: bool, proficiency_option: str,  model_option: str):

    # Check if the user wants to exit
    if message.lower().strip() == 'bye' or message.lower().strip() == 'tschüss':

        # Close the browser window and stop the application - BROKEN
        gr.close_all()
        exit()

    _system_message: str = system_message

    # Add specific instructions based upon the verbose checkbox
    if verbose_option:
        _system_message += " Also please show responses in both German and English."

    # Add specific instructions based upon the CEFR level
    _system_message += f" Please use the CEFR level {proficiency_option} for vocabulary and grammar."

    # Prepare messages for OpenAI
    messages = [{"role": "system", "content": _system_message}] + \
        history + [{"role": "user", "content": message}]

    # Call the OpenAI API with streaming
    stream = openai.chat.completions.create(
        model=model_option, messages=messages, stream=True)

    # Stream the response back to the user
    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        yield response


def select_model(company_name: str, url: str, model: str):
    yield ""
    prompt = f"Please generate a company brochure for {company_name}. Here is their landing page:\n"
    # prompt += Website(url).get_contents()
    if model == "gpt-4o-mini":
        result = call_gpt(prompt, model)
    elif model == "claude-3-5-haiku-latest":
        result = call_claude(prompt, model)
    elif model == "gemini-1.5-flash":
        result = call_gemini(prompt, model)
    elif model == "gemini-2.5-flash-lite":
        result = call_gemini(prompt, model)
    else:
        raise ValueError("Unknown model")
    yield from result


def call_gpt(prompt: str, model: str):
    # Prepare messages for OpenAI
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]

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


def call_claude(prompt: str, model: str):
    # Prepare messages for Claude
    messages = [{"role": "user", "content": prompt}]

    # Call the Claude API with streaming
    result = claude.messages.stream(
        model=model,
        system=system_message,
        messages=messages,
        temperature=0.7,
        max_tokens=1000
    )

    # Stream the response back to the user
    response = ""
    with result as stream:
        for text in stream.text_stream:
            response += text or ""
            yield response


def call_gemini(prompt: str, model: str):
    # Call the Gemini API with streaming
    gemini = google.generativeai.GenerativeModel(
        model_name=model,
        system_instruction=system_message
    )

    # Stream the response back to the user
    result = ""
    for response in gemini.generate_content(prompt, stream=True):
        result += response.text or ""
        yield result


if __name__ == "__main__":
    main()
