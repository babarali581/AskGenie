import os
import requests
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional  # Import List and Optional
import re
from datetime import datetime, timezone
from fastapi.middleware.cors import CORSMiddleware
import shutil
from utils import extract_text_from_pdf, extract_text_from_website, upload_content, write_file_content, get_content_from_firebase, store_prompt, get_prompts, generate_pdf_with_wrapping, generate_ppt, find_prompts
from typings import AskQuestionRequest, GenerateFile
from resources import model, genai

app = FastAPI()
LOCAL_PATH = os.getenv("LOCAL_PATH")

OUTPUTS= 'outputs'

if not os.path.exists(LOCAL_PATH):
    os.makedirs(LOCAL_PATH)

if not os.path.exists(OUTPUTS):
    os.makedirs(OUTPUTS)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], )


@app.post("/upload/")
async def save_urls_and_files_to_firebase(
      urls: Optional[List[str]] = Form(None), files: Optional[List[UploadFile]] = File(None)):
    
    data = {"files":{}, "urls":{}}
    if urls:
        urls= urls[0]
        urls= urls.split(',')
        for url in urls:
            try:
                print("URL", url)
                response = requests.get(url)
                response.raise_for_status()
               
                content=extract_text_from_website(response.text)
                content_id= upload_content(content, "url")
                data["urls"][url]= content_id

            except requests.exceptions.RequestException as e:
                pass

    if files:
       
        for uploaded_file in files:
            try:
                file_path = os.path.join(LOCAL_PATH, uploaded_file.filename)
                await write_file_content(file_path, uploaded_file)
                if uploaded_file.content_type == "application/pdf":
                    file_content = extract_text_from_pdf(file_path)   
                else:
                    await uploaded_file.seek(0)
                    file_content = await uploaded_file.read() 
                    
                    file_content= file_content.decode('utf-8')
                
                content_id= upload_content(file_content, "text", uploaded_file.filename)
                data["files"][uploaded_file.filename]= content_id
            except Exception as e:
                pass

    return data





@app.post("/ask_question/")
async def ask_question_url(request: AskQuestionRequest):
    
        
        
        contents=[]
        for id in request.resource_ids:
            try:
                content= get_content_from_firebase(id)
            except Exception as e:
                continue

            
            
            try:
                if content.get("filename"):
                    contents.append(genai.upload_file(os.path.join(LOCAL_PATH, content["filename"])))
                else:
                    contents.append(content["content"])
            except Exception as e:
                print(e)
                continue
            #try:
            #    text = content["content"]
            #except KeyError:
            #    continue
        
            #contents.append("CONTENT ->: "+text)

        
        
        try:
            #prompt= ["ANSWER THE QUESTION ACCORDING TO THE PROVIDED CONTENT, TRY TO CREATE TABLE ,THERE MAY BE ONE OR MULTIPLE CONTENTS IDENTIFYING AS CONTENT ->: "+request.question]
            
            if request.table:
                prompt = [
        f"ANSWER THE QUESTION ACCORDING TO THE PROVIDED CONTENT. CREATE A TABLE IF RELEVANT. THERE MAY BE ONE OR MULTIPLE TEXT CONTENTS OR FILES, IF PDF FILE IS UNREADABLE , TRY PARSING IT USING OCR.  {request.question}"
    ]
            else:
                prompt = [
        f"ANSWER THE QUESTION ACCORDING TO THE PROVIDED CONTENT. THERE MAY BE ONE OR MULTIPLE TEXT CONTENTS OR FILES, IF PDF FILE IS UNREADABLE , TRY PARSING IT USING OCR. {request.question}"
    ]
            answer=model.generate_content(
                                  prompt  +contents)
            

            store_prompt(request.question, answer.text)

            return JSONResponse(content={"response": answer.text})
        except Exception as e:
            print(e)
            return JSONResponse(content={"response":"SOMETHING WENT WRONG"},status_code=500)
            
   



@app.get("/prompt-history/")
async def get_history():
    try:
        
        return JSONResponse(content={"response": get_prompts()})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error retrieving history.")




@app.get("/prompt-history/{_id}")
async def get_specific_prompt(_id: str):
    try:
        return JSONResponse(content=get_content_from_firebase(_id,"prompts")) 
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving history.")
    



@app.post("/generate")
async def generate(request: GenerateFile):
    ids = request.IDs
    output_format = request.format
    layout = request.layout

    data= find_prompts(ids)
    data2 = data[0]['answer']
    print("ansWER ",data)
    if output_format == "PDF":
        file_path = generate_pdf_with_wrapping(data, layout, request.heading, request.subheading)  # Example function
    elif output_format == "PPT":
        file_path = generate_ppt(data, layout, request.heading,request.subheading)  # Example function
    
    return FileResponse(file_path, media_type="application/octet-stream", filename=file_path.split("/")[-1])