"""Core module for grammar correction and tone rewriting using Google Gemini API.
"""

import os
from typing import List, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()


class RewriteResult(BaseModel):
    """Structured response schema for the rewritten text."""
    rewritten_text: str = Field(
        description="The rewritten text matching the requested tone and standard grammar rules."
    )
    tone_applied: str = Field(
        description="The tone applied to the text."
    )
    improvements: List[str] = Field(
        description="Bullet points of specific grammar, vocabulary, or phrasing improvements made."
    )
    readability_note: str = Field(
        description="Brief comment on readability, clarity, or impact."
    )


TONE_DESCRIPTIONS = {
    "Professional": "Clear, polite, authoritative, suitable for work emails and business communication.",
    "Casual & Friendly": "Warm, conversational, approachable, ideal for peers and casual chats.",
    "Concise & Direct": "Trim fluff, get straight to the point, highly readable with active voice.",
    "Academic / Formal": "Sophisticated vocabulary, well-structured complex sentences, objective tone.",
    "Persuasive": "Compelling, action-oriented, engaging, designed to convince or inspire."
}


def rewrite_text(
    text: str,
    tone: str = "Professional",
    api_key: Optional[str] = None,
    model_name: str = "gemini-3.8-flash"
) -> RewriteResult:
    """Rewrites text according to selected tone and standard grammar rules.
    
    Args:
        text: The original user input text.
        tone: Target tone (e.g., Professional, Casual, Concise).
        api_key: Gemini API key. Defaults to GEMINI_API_KEY environment variable.
        model_name: Gemini model name.
        
    Returns:
        RewriteResult object containing rewritten text and explanations.
    """
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError(
            "Missing Gemini API Key. Set GEMINI_API_KEY in your .env file or pass it to rewrite_text()."
        )

    # Import google.genai inside function to allow graceful handling if not yet installed
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        raise ImportError(
            "The 'google-genai' library is required. Install it using: pip install google-genai"
        )

    client = genai.Client(api_key=key)

    tone_description = TONE_DESCRIPTIONS.get(tone, f"Custom tone: {tone}")

    system_instruction = (
        "You are an expert editor, linguist, and communication specialist. "
        "Your goal is to correct grammar, spelling, punctuation, and rewrite text into the specified tone. "
        "Always preserve the original intent and core facts while elevating readability."
    )

    prompt = f"""
Target Tone: {tone} ({tone_description})

Original Text:
\"\"\"{text.strip()}\"\"\"

Please rewrite the original text in the target tone, fix any grammatical/syntactical errors,
and detail the improvements made according to the required schema.
"""

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            response_schema=RewriteResult,
            temperature=0.3,
        ),
    )

    # In google-genai with response_schema, the response.parsed attribute contains the Pydantic instance
    if hasattr(response, "parsed") and response.parsed:
        return response.parsed

    # Fallback parsing in case SDK returns JSON string
    return RewriteResult.model_validate_json(response.text)


if __name__ == "__main__":
    import sys

    sample_text = (
        "hey there im writing this to tell you that we cant make it to the meeting "
        "because of some stuff that happened yesterday so sorry about that"
    )

    print("--- Original Text ---")
    print(sample_text)
    print("\n--- Testing Rewrite ('Professional') ---")

    try:
        result = rewrite_text(sample_text, tone="Professional")
        print("\nRewritten:")
        print(result.rewritten_text)
        print("\nKey Improvements:")
        for imp in result.improvements:
            print(f"- {imp}")
        print(f"\nReadability Note: {result.readability_note}")
    except Exception as e:
        print(f"Error: {e}")
        print("\nTip: Make sure GEMINI_API_KEY is set in your .env file!")
