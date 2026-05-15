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

class ToolCommandPair(BaseModel):
    tool: str
    command: str

    def __str__(self):
        return f"{self.tool} -> \n{self.command}\n"

class RemediationAction(BaseModel):
    tool_command_pairs: list[ToolCommandPair]
    rationale: str

    def __str__(self):
        result = "What to do:\n"
        for i, pair in enumerate(self.tool_command_pairs):
            result += f"{i + 1}. {pair}\n"
        result += f"Rationale:\n{self.rationale}\n"
        return result
