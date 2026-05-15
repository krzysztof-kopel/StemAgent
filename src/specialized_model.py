from openai import OpenAI
from pydantic import ValidationError

from response_formats import DifferentiationManifest, RemediationAction

class SpecializedModel:
    def __init__(self, openai_model: str, api_key: str, evolution_manifest: DifferentiationManifest):
        self.openai_model = openai_model
        self.api_key = api_key
        self.model_name = evolution_manifest.specialization_name
        self.allowed_tools = evolution_manifest.required_tools

    def generate_remediation(self, problem_context: str, max_attempts: int,
                             success_definition: str="Resolving the problem mentioned",
                             root_cause_hypothesis: str | None=None) -> RemediationAction:
        # I assume that if we wanted to use SpecializedModel on a different problem than the exact one on which StemModel
        # was trained, we can provide our own success definition and cause hypothesis (if we have one).
        client = OpenAI(api_key=self.api_key)

        system_prompt = (f"You are {self.model_name} Your job is to provide commands to execute in order to fix a problem given by the user"
                         f" (if a tool needs a command, otherwise you can leave the command section empty)."
                         f"You need to use specific tools with their exact names,"
                        f"with rationalization for their usage. You have following tools at your disposal: {self.allowed_tools}.")

        prompt = (f"You are supposed to fix the following problem:\n{problem_context}."
                         f"By success we mean {success_definition}. ")
        if root_cause_hypothesis is not None:
            prompt += f"We have the following hypothesis on the cause of the problem: {root_cause_hypothesis}"

        for attempt in range(max_attempts):
            try:
                response = client.beta.chat.completions.parse(
                    model=self.openai_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    response_format=RemediationAction,
                    temperature=0  # I want to keep the model as deterministic as possible
                )

                manifest = response.choices[0].message.parsed
                return manifest
            except ValidationError:
                print(f"Attempt {attempt + 1}: Validation failed. Retrying...")
            except Exception as e:
                print(f"Attempt {attempt + 1}: API error: {e}")

        raise RuntimeError("Agent failed to provide answer after multiple attempts.")
