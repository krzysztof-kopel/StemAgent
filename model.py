import os

from openai import OpenAI
from pydantic import BaseModel, ValidationError


class DifferentiationManifest(BaseModel):
    specialization_name: str
    reasoning_summary: str
    required_skills: list[str]
    success_definition: str

def generate_context_string() -> str:
    context_string = ""

    for filename in os.listdir("resources"):
        with open(os.path.join("resources", filename)) as file:
            context_string += "Source " + filename[:-4] + ":\n"
            context_string += file.read()
        context_string += "\n\n"
    return context_string

def differentiate(context: str, max_attempts: int) -> DifferentiationManifest:
    client = OpenAI(api_key="key goes here")

    system_prompt = ("You are a digital stem cell. Analyze the environment telemetry and differentiate into a specialized"
                     "agent. Return ONLY the JSON matching the required schema.")

    for attempt in range(max_attempts):
        try:
            response = client.beta.chat.completions.parse(
                model="model_name",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": context}
                ],
                response_format=DifferentiationManifest,
                temperature=0 # I want to keep the model as deterministic as possible
            )

            return response.choices[0].message.parsed
        except ValidationError:
            print(f"Attempt {attempt + 1}: Validation failed. Retrying...")
        except Exception as e:
            print(f"Attempt {attempt + 1}: API error: {e}")

    raise RuntimeError("Agent failed to differentiate after multiple attempts.")

