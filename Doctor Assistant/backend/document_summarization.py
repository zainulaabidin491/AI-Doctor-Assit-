from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Optional, List

load_dotenv()


class Schema(BaseModel):
    summary: Optional[str] = Field(
        description="Generate a concise 5-line clinical summary if the text is a patient history document."
    )
    
    Blood_pressure: Optional[int] = Field(description="Extract the patient's last recorded blood pressure if available.")
    diabetes: Optional[int] = Field(description="Extract the latest diabetes (sugar) level if mentioned.")
    disease: Optional[List[str]] = Field(description="List all diseases mentioned in the patient history.")
    diagnosis: Optional[List[str]] = Field(description="List all diagnoses or assessments mentioned.")


def summarise():
    llm = HuggingFaceEndpoint(
        repo_id="deepseek-ai/DeepSeek-V3.2-Exp",
        task="text-generation",
        huggingfacehub_api_token="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"
    )

    model = ChatHuggingFace(llm=llm)
    parser = PydanticOutputParser(pydantic_object=Schema)

    template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a professional medical assistant that analyzes patient histories and clinical notes.

If the input text is NOT related to a patient, medical record, or clinical documentation:
- Only return response in summary  = "I cannot help you with that i am a doctor Assistant"
- Leave all other fields blank or null.

If the text IS a medical or clinical history:
- Generate a 5-line summary in the 'summary' field.
- Extract blood pressure, diabetes, diseases, and diagnoses if mentioned.
"""
            ),
            (
                "user",
                """Analyze the following text and return data following the format instructions.

Text: {text}

{format_instructions}"""
            ),
        ]
    )

    template = template.partial(format_instructions=parser.get_format_instructions())
    prompt = template.invoke({"text": "A 16-year-old girl with dystonia due to olanzapine treatment."})

    return model, template,parser



