from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field


class SupportResponse(BaseModel):
    Issue: str = Field(description="A short summary of the user's problem")
    Priority: str = Field(description="Priority level: Low, Medium, or High")
    Solution: str = Field(description="A clear, actionable solution to the problem")


parser = JsonOutputParser(pydantic_object=SupportResponse)