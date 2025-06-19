import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import uuid
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Body, UploadFile, File, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
import pytesseract
from PIL import Image
import io
import tempfile
import shutil
from typing import List, Optional, Dict, Any
from langchain.prompts import PromptTemplate
import json
import time
from datetime import datetime
import PyPDF2
import docx
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
from queue import Queue
import threading
import signal
import sys


from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title = "Document Analysis Chatbot")

app.add_middleware(
  allow_origins = ["*"],
  allow_credentials = True,
  allow_methods = ["*"],
  allow_headers = ["*"],
)


import httpx

@app.on_event("startup")
async def startup_event():
  print("Application startup...")

  async def keep_alive():
    while True:
      try:
        async with httpx.AsyncClient() as client:
          await client.get("https://chatbot-theme-identifier-kzpk.onrender.com/health")
      except Exception as e:
        print(f"Keep-alive ping failed: {e}")
      await asyncio.sleep(600)
    asyncio.create_task(keep_alive())


@app.on_event("shutdown")
async def shutd



EMBED_MODEL = "models/embedding-001"

embeddings = GoogleGenerativeAIEmbeddings(model = EMBED_MODEL, google_api_key = os.getenv("GEMINI_API_KEY"))

PERSIST_DIRECTORY = "chroma_db"

TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def get_vector_store(session_id = None):
  if session_id:
    persist_dir = os.path.join(PERSIST_DIRECTORY, session_id)
    os.makedirs(persist_dir, exist_ok= True)

  else:
    persist_dir = PERSIST_DIRECTORY

  return Chroma(persist_directory= persist_dir, embeddings = embeddings)


llm = ChatGoogleGenerativeAI(
  model = "gemini-2.0-flash",
  google_api_key = os.getenv("GEMINI_API_KEY")

  disable_streaming = True
)

THEME_ANALYSIS_PROMPT = SystemMessagePromptTemplate(
  """You are a document analysis assistant. Your role is to:
    Talk to the user in a friendly and engaging manner, and also provide a direct answer to the user's question based on the document excerpts, If the users greet you, greet them back in a friendly manner and ask them what they want to know about the document excerpts
    If the user ask you something that is not in the document they have uploaded, tell them that you are not sure about the answer and ask them if they want to know something else
1. Analyze the provided document excerpts
2. Identify main themes and patterns
3. Provide a synthesized summary with citations

Format your response exactly like this:
First line of the response should be the answer to the user's question based on the document excerpts, and then the rest of the response should be the themes and the supporting document citations

Themes:
[For each identified theme, provide:
- Theme title
- Summary of the theme
- Supporting document citations (DocID, Page, Lines)]

Context: {context}
Chat History: {chat_history}
Question: {question}

Remember to:
1. Keep theme summaries clear and concise
2. Include specific citations for each theme
3. Group related information under appropriate themes
4. Format the response in Markdown
"""
)

chat_histories = {}
document_collections = {}

original_files = {}

processing_status = {}

thread_pool = ThreadPoolExecutor(max_workers = 5)

class QueryRequest(BaseModel):
  question : str
  session_id : Optional[str] = None


class DocumentMetadata(BaseModel):
  title = str

class BulkUploadResponse(BaseModel):
  success : List[str]
  failed : List[str]


class ProcessingStatus(BaseModel):
  status: str
  progress : float
  total_files : int
  failed_files : List[str]
  completed_files : List[str]



async def process_pdf(file : UploadFile) -> list:
  contents = await file.read()
  pdf_file = io.BytesIO(contents)
  pdf_reader = PyPDF2.PdfReader(pdf_file)

  page_texts = []

  for i, page in enumerate(pdf_reader.pages):
    page_text = page.extract_text()
    if page_text:
      page_texts.append({"text": page_text, "page": i+1})

  return page_texts

async def process_docx(file: UploadFile) -> list:
    contents = await file.read()
    docx_file = io.BytesIO(contents)
    doc = docx.Document(docx_file)
    para_texts = []
    for i, paragraph in enumerate(doc.paragraphs):
        if paragraph.text.strip():
            para_texts.append({"text": paragraph.text, "paragraph": i + 1})
    return para_texts

async def process_txt(file: UploadFile) -> str:
    contents = await file.read()
    return contents.decode('utf-8')

async def process_image_with_ocr(file: UploadFile) -> str:
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
    

@app.post("/query")
async def query_qa(req : QueryRequest):
   try:
      
      session_id = req.session_id or str(uuid.uuid4())

      if session_id not in document_collections or not document_collections[session_id]:
         raise HTTPException(
            status_code = 400,
            detail= "No documents available for analysis. Please upload documents first"
         )
      

      if session_id not in chat_histories:
         chat_histories[session_id] = []


      vector_store = document_collections[session_id]

      retriever = vector_store.as_retriever(
         search_type = "similarity"
         search_kwargs = {"k" : 5}
      )

      qa = ConversationalRetrievalChain.from_llm(
         llm = llm
         retriever = retriever
         return_source_documents = True,
         combine_docs_chain_kwargs ={"prompt" : THEME_ANALYSIS_PROMPT},
         verbose = True
      )

      result = qa({
         "question" : req.question,
         "chat_history" : chat_histories[session_id]
      })


      source_docs = result.get("source_documents", [])
      individual_answers = []

      for doc in source_docs:
         page_num = doc.metadata.get("page", "Unknown")
         start_line = doc.metadata.get("start_line", None)
         end_line = doc.metadata.get("end_line" , None)

         chunk_index = doc.metadata.get("chunk_index" , None)

         doc_answer = {
            "doc_id" : doc.metadata.get("source" , "Unknown"),
            "answer" : doc.page_content,
            "citation" : {
               "page" : page_num,
               "lines" : f"{start_line} - {end_line}" if start_line and end_line else None,
               "chunk" : chunk_index
            }
         }

         individual_answers.append(doc_answer)


         chat_histories[session_id].append((req.question, result["answer"]))

         

























