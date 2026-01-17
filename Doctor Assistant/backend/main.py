from fastapi import FastAPI
from pydantic import  BaseModel,Field
from document_summarization import summarise


model,template,parser=summarise()
class Text(BaseModel):
    text:str=Field("Enter patient history")



app=FastAPI()



@app.post("/summarise")
def summarise(text:Text):
    prompt=template.invoke({'text':text})
    results=model.invoke(prompt)
    result_final=parser.parse(results.content)
    return {'result':result_final}
