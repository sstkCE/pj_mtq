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
TemplateRoom1="""ช่วยคิดเรื่องราวพร้อมบทพูดของ {occupations} ความยาวไม่เกิน 500 ตัวอักษร โดยที่สถานการณ์ตอนนี้คือยานเกิดอุบัติเหตุก่อนหน้า และเมื่อเกิเมีอุกกาบาตกำลังจะพุ่งชนยาน ต้องเปิดระบบป้องกันยาน
ช่วยคิดปริศณาแนว escape room สถานที่ยานอวกาศ โดยห้ามใช้วัตถุที่บอก มีความยากง่าย 3 ระดับคือ ง่าย, กลาง, ยาก และมีคำใบ้(hint) ที่เป็นแนวพูดให้ทำเช่น “เอ๊ะ…ฉันคิดว่าที่ไฟมีกระพริบเป็นแพทเทิร์นนะ”
1.
มีหลอดไฟสีแดงจำนวน 1
มีหลอดไฟสีน้ำเงินจำนวน 1
มีหลอดไฟสีเขียวจำนวน 1 
มีหลอดไฟสีชมพูจำนวน 1
กำหนดจำนวนครั้งที่ไฟกระพริบ ไฟกระพริบด้วยความถี่ที่เท่ากัน ตอบเป็นตัวเลขเช่น lightBulb1 กระพริบ 1, lightBulb2 กระพริบ 2, lightBulb3 กระพริบ 3, lightBulb3 กระพริบ 3 ตอบ “1234” พร้อมบทพูดที่สอดคล้องกับการเปิดประตู

2.
มีแบตเตอรี่สีฟ้าจำนวน 4 ก้อน
มีแบตเตอรี่สีเทาจำนวน 4 ก้อน
มีแบตเตอรี่สีแดงจำนวน 4 ก้อน
มีแบตเตอรี่สีเหลือง จำนวน 4 ก้อน
มีแทนชาร์จจำนวน 4 จุด
กำหนดค่าให้แบตเตอร์รี่ทุกก้อน โดยใช้สีละก้อนในการรวมค่าให้ได้ตามต้องการ ตอบเป็นตัวเลขพร้อมบทพูดที่สอดคล้องกับการเปิดพลังงาน

3.
led 1 ดวง
ช่อง VCC 1 ช่อง
ช่อง GND 1 ช่อง
ปุ่มสำหรับ input 1
ปุ่มสำหรับ input 2
IC7408 1 ชิ้น
IC7432 1 ชิ้น
สายไฟที่ต่อ VCC กับ IC ขาที่ 14
สายไฟที่ต่อ GND กับ IC ขาที่ 7
สายไฟที่ต่อ ปุ่ม input 1 กับ IC ขาที่ 1
สายไฟที่ต่อ ปุ่ม input 2 กับ IC ขาที่ 2
สายไฟที่ต่อ led กับ IC ขาที่ 3
คิด puzzle โดยที่เลือกใช้ IC 1 ชนิด และต้องบอกว่าวัตถุไหนที่ไม่อยู่บนบอร์ดบ้างซื่งสามารถมีวัตถุอยู่(ture)ครบหรือเลือกให้มีอยู่บางชิ้นได้ หากไม่มี(false)วัตถุต้องหาเพื่อให้ครบวงจร การตรวจคำตอบคือ led ติดใช้วัถตุจากที่ให้ไปเท่านั้น พร้อมบทพูดที่สอดคล้องกับ puzzle 1 และ 2

4. 
คิด puzzle จากวัตถุที่อยู่ทั้วยานไม่มีตำแหน่งวัตถุระบุต่อไปนี้
รูปภาพดร.ไสว สุทธิพิทักษ์ ต่ำแหน่ง ผู้ก่อตั้งยาน DPU จำนวน 1 รูป
รูปภาพอาจารย์สนั่น เกตุทัต ต่ำแหน่ง ผู้ก่อตั้งยาน DPU จำนวน 1 รูป
รูปภาพอลัน ทัวริ่ง ต่ำแหน่ง กัปตันยาน DPU รุ่นที่ CITE-CE 28 จำนวน 1 รูป
รูปภาพเอดา เลิฟเลซ ต่ำแหน่ง รองกัปตันยาน DPU รุ่นที่ CITE-CE 28 จำนวน 1 รูป
ตู้ล็อกเกอร์เปล่า 5 ตู้
กล่อง 35 กล่อง
ชั้นวางของ 5 ชิ้น
คิด puzzle ที่สอดคล้องกับสถานที่ตอบคำตอบอยู่ที่หัวยานเป็น puzzle จบเกม และที่รับการเช็คเป็นการกดปุ่มตัวเลข pin 6 หลักใช้วัตถุเท่าที่บอก และ hint1 คือตำแหล่งนี้ได้มาจากอะไร เช่น “พยางชื่อของดร. อาจมีความสำคัญกับการตอบนะ” = ตอบ 2

{
“story” : “…”,
“puzzle1”: {
 “story”: “บทพูดที่นำพาให้มาทำ puzzle นี้”,
   "easy": {
  “speech” : “....”,
  "lightBulb1": “ตัวเลข”,
  "lightBulb2": "ตัวเลข.",
  "lightBulb3": “ตัวเลข”,
  "lightBulb4": "ตัวเลข",
  “answer”: “ตัวเลข”
 }
 “medium”: {…},
 "hard”: {…}
},
“puzzle2”: {
 “story”: “บทพูดที่นำพาให้มาทำ puzzle นี้”,
 "easy": {
  “speech” : “....”,
  “total_value”: “….”,
  “hint”: “…”,
  "blue_battery": 
  {[
   “blue1”: “....”,
    “blue2”: “....”,
   “blue3”: “....”,
    “blue4”: “....”,
  ]},
  “grey_battery": {[…]},
  “red_battery": {[…]},
  “yellow_battery": {[…]},
 },
 “medium”: {…},
 "hard”: {…}
},
“puzzle3”: {
 “story”: “บทพูดที่นำพาให้มาทำ puzzle นี้”,
 "easy": {
  “speech” : “....”,
  “hint”: “…”,
  “typeIC”: “...”,
  “ic”: Boolean,
  “led”: Boolean,
  “buttonInput1”: Boolean,
  “buttonInput2”: Boolean,
  “wireVccToIC”: Boolean,
  “wireGndToIC”: Boolean,
  “wireBtn1ToIC”: Boolean,
  “wireBtn2ToIC”: Boolean,
  “wireLedToIC”: Boolean,
 },
 “medium”: {…},
 "hard”: {…}
},
“puzzle4”: {
 “story”: “บทพูดที่นำพาให้มาทำ puzzle นี้”,
 "easy": {
  “speech1” : “บทพูดที่ชวนให้ออกเดินหาคำตอบ”,
  “speech2” : “....”,
  “hint1”: “…”,
  “hint2”: “…”,
  “hint3”: “…”,
  “hint4”: “…”,
  “hint5”: “…”,
  “hint6”: “…”,
  “ans”: “123456”
 },
 “medium”: {…},
 "hard”: {…}
}
}"""

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


@app.post('/room1')
async def gen_puzzleT(request : Request):
    data = await request.json() # request จาก unity
    pt = ChatPromptTemplate.from_template(TemplateRoom1)
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