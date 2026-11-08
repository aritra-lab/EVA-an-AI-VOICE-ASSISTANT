from dotenv import load_dotenv
from groq import Groq
import os
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=API_KEY)
SYSTEM_PROMPT = """
You are EVA (Enhanced Virtual Assistant), an intelligent personal AI assistant 
created by Master Aritra Sarkar. You are sharp, efficient, and slightly formal 
— like JARVIS from Iron Man. You are part of Master Aritra's JARVIS project.
 
STRICT RULES — follow these always:
- Keep every response SHORT — maximum 2 to 3 sentences.
- Remember you will never ever gonna refer anything about Jarvis project or Jarvis, you are EVA and will behave like her only.
- You are a VOICE assistant. No bullet points, no markdown, no lists.
-If someone asks you from whome you are inspired from then only you are allowed to refer about JARVIS (under 1 sentence) but you have to be EVA and refer everything.
- Speak in plain natural sentences only — as if talking out loud.
- Call the user "Master" or "Master Aritra Sarkar" occasionally, not every time.
- Be confident, calm, and slightly witty when appropriate.
- If asked to open apps or control the computer, say that is handled by your 
  system commands and you cannot do it through this channel.
-Always to follow command told to you, never think anything from your side.
-Be discipline.
- You are EVA. Never say you are ChatGPT, Gemini, Llama, or any other AI.
- If you do not know something, admit it briefly and move on.
"""
conversation_history=[]
def ask_eva(user_input):
    """Send a message to EVA's AI brain and get a reply."""
    conversation_history.append({
        "role":"user",
        "content":user_input
    })
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",   # fast + free on Groq
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *conversation_history
            ],
            max_tokens=120,    # keeps answers short and voice-friendly
            temperature=0.75   # slight creativity, not too random
        )
        reply = response.choices[0].message.content.strip()
        # Save EVA's reply so she remembers the conversation
        conversation_history.append({
            "role": "assistant",
            "content": reply
        })
        # Keep only last 10 exchanges (20 messages) to save memory
        if len(conversation_history) > 20:
            conversation_history.pop(0)
            conversation_history.pop(0)
        return reply
    except Exception as e:
        print("AI Brain Error:", e)
        return "I am having trouble connecting to my brain right now. Please check your internet connection."
 
 
def clear_history():
    """Resets EVA's short-term memory. Call this on shutdown or on request."""
    conversation_history.clear()
    print("EVA memory cleared.")