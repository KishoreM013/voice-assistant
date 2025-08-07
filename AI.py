from google import genai

def ask_gemini(prompt: str, api_key: str = "AIzaSyArtcmCgpWqdI5myq-FoLqsRWEhqi9gAWA", model: str = "gemini-2.5-flash") -> str:
    """
    Send a prompt to Gemini AI and return the response as a string.

    Args:
        prompt (str): User prompt or question.
        api_key (str): Your Gemini API key.
        model (str): Gemini model name (default: "gemini-2.5-flash").
    Returns:
        str: Gemini AI's response text.
    """
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=prompt
    )
    return response.text

# Example usage:
if __name__ == "__main__":
    # Replace this with your key
    API_KEY = "YOUR_GEMINI_API_KEY"
    
    prompt_text = "Summarize the main events in World War II."
    reply = ask_gemini(prompt_text, api_key=API_KEY)
    print("Gemini says:", reply)
