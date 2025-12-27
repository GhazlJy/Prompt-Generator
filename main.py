from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
import os
from fastapi.middleware.cors import CORSMiddleware


client = genai.Client(api_key=api_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    idea: str
    audience: str = ""
    example: str = ""

@app.post("/generate")
def generate_prompt(req: PromptRequest):
    system_instruction = "You are a Lead Prompt Architect. Follow the 26 principles to generate a professional prompt. Output must be in English."
    example_value = req.example.strip() if req.example else "Not Provided"

    user_message_content = f"""
Task: Architect a professional, high-precision prompt based on these inputs:

- Idea: {req.idea}
- Target Audience: {req.audience if req.audience else "Not Provided"}
- Example: {example_value}

You MUST:
- Apply the 26 principles described in the system instruction.
- Respect the Auto-Delete Protocol for the # Few-Shot Examples section:
  - If Example is exactly "Not Provided", you MUST COMPLETELY DELETE the line containing the 'Few-Shot Examples' tag.
  - Do NOT replace it with any alternative text.
- Output the final engineered prompt in English inside a Markdown code block.
"""

    model_name = "gemini-2.5-flash"

    response = client.models.generate_content(
        model=model_name,
        contents=user_message_content,
        config={"system_instruction": system_instruction}
    )

    final_prompt = response.text if hasattr(response, "text") else str(response)
    return {"prompt": final_prompt}
