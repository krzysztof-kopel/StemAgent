from pydantic import BaseModel, Field

class DifferentiationManifest(BaseModel):
    specialization_name: str
    reasoning_summary: str
    root_cause_hypothesis: str = Field(description="A precise engineering hypothesis that links distinct anomalies, "
                                                    "focusing on causality rather than vague "
                                                    "correlations.")
    required_tools: list[str]
    success_definition: str

    def __str__(self):
        return ("-" * 40 + "\n").join(f"{k.upper()}:\n{v}\n" for k, v in self.model_dump().items())

class RemediationAction(BaseModel):
    target_device: str
    commands: list[str]
    rationale: str
