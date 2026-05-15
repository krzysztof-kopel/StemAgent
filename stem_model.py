import os

from openai import OpenAI
from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from response_formats import DifferentiationManifest
from specialized_model import SpecializedModel
from tools import format_tools

class Settings(BaseSettings):
    openai_api_key: str
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

class StemModel:
    def __init__(self, openai_model: str, api_key: str):
        self.openai_model = openai_model
        self.api_key = api_key
        self.diff_manifest = DifferentiationManifest(required_tools=[""], reasoning_summary="", specialization_name="",
                                                     root_cause_hypothesis="", success_definition="")

    @staticmethod
    def generate_context_string(source_dir: str) -> str:
        context_string = ""

        for filename in os.listdir(source_dir):
            with open(os.path.join(source_dir, filename)) as file:
                context_string += "Source " + filename[:-4] + ":\n"
                context_string += file.read()
            context_string += "\n\n"
        return context_string

    def differentiate(self, context: str, max_attempts: int) -> DifferentiationManifest:
        client = OpenAI(api_key=self.api_key)

        tools_prompt = f"When choosing tools, you can select only the ones from the following list: {format_tools()}."

        system_prompt = ("You are a digital stem cell. Analyze the environment telemetry and differentiate into a specialized"
                         "agent. Return ONLY the JSON matching the required schema.")

        for attempt in range(max_attempts):
            try:
                response = client.beta.chat.completions.parse(
                    model=self.openai_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "system", "content": tools_prompt},
                        {"role": "user", "content": context}
                    ],
                    response_format=DifferentiationManifest,
                    temperature=0 # I want to keep the model as deterministic as possible at this stage
                )

                manifest = response.choices[0].message.parsed
                self.diff_manifest = manifest
                return manifest
            except ValidationError:
                print(f"Attempt {attempt + 1}: Validation failed. Retrying...")
            except Exception as e:
                print(f"Attempt {attempt + 1}: API error: {e}")

        raise RuntimeError("Agent failed to differentiate after multiple attempts.")

    def evolve(self) -> SpecializedModel:
        return SpecializedModel(self.openai_model, self.api_key, self.diff_manifest)

