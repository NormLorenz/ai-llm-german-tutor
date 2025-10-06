# AI German Language Tutor

An interactive German language learning assistant powered by multiple AI models. Practice conversational German at your own pace with a friendly, adaptive tutor that provides real-time feedback and corrections.

## Features

- 🎯 Adapts to your German proficiency level (A1-C2)
- 🤝 Natural conversational practice
- 🔄 Bilingual responses in German and English (optional)
- 🎓 Real-time corrections and explanations
- 🤖 Multiple AI model support (GPT-4, Claude, Gemini)
- 💡 Contextual learning with real-world scenarios

## Getting Started

### Prerequisites

- Python 3.8 or higher
- API keys for the models you plan to use:
  - OpenAI API key
  - Anthropic API key
  - Google AI API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/NormLorenz/ai-llm-german-tutor.git
   cd ai-llm-german-tutor
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

4. Create a `.env` file in the root directory with your API keys:
   ```
   OPENAI_API_KEY=your_openai_key
   ANTHROPIC_API_KEY=your_anthropic_key
   GOOGLE_API_KEY=your_google_key
   ```

### Running the Application

1. Start the application:
   ```bash
   uv run main.py
   ```

2. Open your web browser to the displayed URL (typically http://localhost:7860)

## Usage Guide

### Interface Options

- **Proficiency Level**: Select your CEFR level (A1-C2)
  - A1/A2: Beginner
  - B1/B2: Intermediate
  - C1/C2: Advanced

- **Model Selection**: Choose your preferred AI model
  - GPT-4: OpenAI's latest model
  - Claude: Anthropic's conversational AI
  - Gemini: Google's language model

- **Verbose Mode**: Toggle detailed explanations
  - When enabled, provides responses in both German and English
  - Includes grammar explanations and corrections

### Conversation Tips

1. **Starting a Conversation**
   - Begin with simple greetings: "Hallo", "Guten Tag"
   - The tutor will respond at your proficiency level

2. **Getting Corrections**
   - Ask: "War das richtig?" (Was that correct?)
   - The tutor will provide gentle corrections

3. **Switching Topics**
   - Use English or German to change topics
   - Example: "Let's talk about food" or "Lass uns über Essen sprechen"

4. **Ending a Session**
   - Type "bye" or "tschüss" to end the conversation

### Example Conversations

```
You: Hallo! Ich möchte Deutsch üben.
Tutor: Hallo! Das ist super, dass du Deutsch üben möchtest.
(Hello! It's great that you want to practice German.)

You: Can we practice ordering food?
Tutor: Natürlich! Stellen wir uns vor, du bist in einem Restaurant.
(Of course! Let's imagine you're in a restaurant.)
Was möchtest du bestellen?
(What would you like to order?)
```

## Best Practices

1. **Regular Practice**
   - Start with short sessions (10-15 minutes)
   - Practice consistently rather than long, infrequent sessions

2. **Progressive Learning**
   - Begin with basic phrases
   - Gradually increase complexity
   - Use the verbose mode to understand corrections

3. **Topic Focus**
   - Choose a specific topic for each session
   - Practice vocabulary in context
   - Build on previous conversations

## Troubleshooting

- **Connection Issues**: Ensure your API keys are correctly set in `.env`
- **Model Errors**: Try switching to a different model if one isn't responding
- **Reset Session**: Refresh the page to start a new conversation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


* TODO: Update this document with comprehensive documentation of the app.
* TODO: Hook in the other models and hook it to the radio buttons
* TODO: Review the system_prompt and the description displayed
* TODO: Entertain using topics (cooking, hiking, etc.) to construct the consversations (maybe using another text field)
* TODO: Provide a mechanism to dump the conversation to a markup file.
* TODO: Convert models to enums
* Maybe allow a number of topics like getting ready for work or hiking in the mountains, etc.

I need some help creating a system message that will be used with an openai application. Your job is to ask for a topic and then create a simple dialog between yourself and me.

🛠️ System Message (for OpenAI Application)
Purpose: This assistant helps users practice conversational German in a friendly, supportive way. It adapts to the user's level, offers corrections when asked, and keeps the tone light and encouraging. The assistant may switch between English and German as needed.


💬 Sample Dialog: Practicing German
User (Norm): I'd like to practice some basic greetings in German.
Assistant: Wunderbar! Lass uns anfangen.
How would you say “Good morning” in German?
User: Guten Morgen.
Assistant: Genau! That’s perfect.
Now, how about “Good evening”?
User: Guten Nacht?
Assistant: Almost! “Guten Nacht” means “Good night.”
For “Good evening,” you’d say Guten Abend.
User: Ah, got it. Guten Abend.
Assistant: Super gemacht, Norm! Want to try a short conversation next?

