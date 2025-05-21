from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from fastapi import FastAPI ,Request
from fastapi.middleware.cors import CORSMiddleware

import json
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ระบุ origin ที่อนุญาต
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # อนุญาตเฉพาะ GET และ POST เท่านั้น
    allow_headers=["*"],  # อนุญาตทุก header
)
load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)



# Prompt สำหรับปริศนา Escape Room

TemplateRoom3= """
ช่วยสร้างเรื่องราวสำหรับเกมโดยสวมบทบาทโดยผู้เล่นมีบทบาทโดยเป็น{occupation}
ภายใน Office
ให้ผู้เล่นโดยเหตุใดต้องทำ 3 สิ่งนี้ ขอ 500 ตัวอักษร
1.หาโพสอิทสี{colP} 6 ใบที่อยู่ทั่วห้องแล้วนำไปแปะบอร์ด
2. จัดเรียงแฟ้มสี{colF}ที่กระจัดกระจาย 
3.เสียบบัตรเปิดไฟ
โดย 
Pos คือตัวอักษร 6 ตัวที่รวมกันแล้วมีความหมาย 1 อักษร ต่อ 1  โพสอิท
Fam คือตัวอักษร 4 ตัวที่รวมกันแล้วมีความหมาย ติดบนแฟ้มต่อ 1 อักษร
ตอบในรูปแบบ JSON: 
{{
    "roleAndStory": "...",
    "reasonDoing1": {{
        "easy": "...",
        "normal": "...",
        "hard": "..."
    }},
    "reasonDoing2": {{
        "easy": "...",
        "normal": "...",
        "hard": "..."
    }},
    "reasonDoing3": {{
        "easy": "...",
        "normal": "...",
        "hard": "..."
    }},
    "pos": "...",
    "fam": "..."
}}
"""

TemplateRoom2= """
ช่วยสร้างเรื่องราวสำหรับเกมโดยสวมบทบาทโดยผู้เล่นมีบทบาทโดยเป็น{occupation}
ภายในท่ออุโมงลึกลับ
ให้ผู้เล่นโดยเหตุใดต้องทำ 5 สิ่งนี้ 

1.ต่อท่อให้สมบูรณ์
2.ดันกล่องที่ขวางทางอยู่
3.ดันกล่องสองใบเพื่อปีนข้ามกำแพง
4.หากุญแจในเขาวงกต
5 สังเกตเลขบนเสื้อตัวตลกในเขาวงกตและนำมาเปิดทางออก
ตอบในรูปแบบ JSON: 
{{
    "roleAndStory": "...",
    "reasonDoing1": {{
        "easy": "...",
        "normal": "...",
        "hard": "..."
    }},
    "reasonDoing2": {{
        "easy": "...",
        "normal": "...",
        "hard": "..."
    }},
    "reasonDoing3": {{
        "easy": "...",
        "normal": "...",
        "hard": "..."
    }}
    "reasonDoing4": {{
        "easy": "...",
        "normal": "...",
        "hard": "..."
    }}
    "reasonDoing5": {{
        "easy": "...",
        "normal": "...",
        "hard": "..."
    }}
}}
"""

@app.post('/room3')
async def gen_puzzleT(request : Request):
    data = await request.json() # request จาก unity
    pt = ChatPromptTemplate.from_template(TemplateRoom3)
    chain = pt | llm
    res = chain.invoke(data)

    try:
        cleaned_response = res.content.strip("```json")
        super_clean = cleaned_response.strip("```")
        print(super_clean)
        response_data = json.loads(super_clean)  # แปลงข้อความเป็น JSON
        return response_data
    except json.JSONDecodeError: 
        return {"error": "AI response is not valid JSON"}

@app.post('/room2')
async def gen_puzzleT(request : Request):
    data = await request.json() # request จาก unity
    pt = ChatPromptTemplate.from_template(TemplateRoom2)
    chain = pt | llm
    res = chain.invoke(data)

    try:
        cleaned_response = res.content.strip("```json")
        super_clean = cleaned_response.strip("```")
        print(super_clean)
        response_data = json.loads(super_clean)  # แปลงข้อความเป็น JSON
        return response_data
    except json.JSONDecodeError: 
        return {"error": "AI response is not valid JSON"}

