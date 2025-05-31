import google.generativeai as genai
import json

def generate_mcq(user_input, api_key):
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-2.0-flash')

    prompt = f"""Generate a multiple choice question.
    MCQ should be about this context:"{user_input}"

    Use this JSON schema:
    {{
      "question": str,
      "options": {{
        "A": str,
        "B": str,
        "C": str,
        "D": str
      }},
      "correct_answer": str,
      "correct_answer_text": str
    }}

    ensure:
    always use the text in the question.
    always generate the mcq with user input language.
    The question is meaningful and relevant to the text.
    The correct answer matches the context of the text.
    The answer choices are plausible but only one is correct.
    Return a single MCQ in JSON format."""

    generation_config = genai.GenerationConfig(
        temperature=0.5,
        top_p=0.7,
        top_k=50,
        max_output_tokens=256,
        response_mime_type="application/json"
    )

    contents = [prompt]
    response = model.generate_content(contents, generation_config=generation_config)
    
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        raise ValueError("Failed to process the API response.")
