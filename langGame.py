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

TemplateRoom4 ="""สร้างคำใบ้สำหรับเกม Escape Room VR โดยใช้ฉากบ้านธรรมดา รับบทเป็น {occupations} ผู้เล่นต้องหาตัวเลข 4 หลักจากการแก้สมการเชาว์ง่าย ๆ ในคำใบ้เพื่อล็อกออกจากบ้าน โดยผู้เล่นไม่สามารถหยิบจับสิ่งของได้ ต้องใช้การสังเกต วิเคราะห์ และจดจำเบาะแสเท่านั้น

คำใบ้ในแต่ละจุด (8 จุด รวม 2 บ้าน) ประกอบด้วยสมการง่าย ๆ ที่ใช้ตัวแปร A,B,C,... แทนจำนวนเต็มบวก (1-9) สมการจะสุ่มเปลี่ยนไปทุกครั้งที่สร้างคำใบ้ โดยมีขั้นตอนและคำตอบที่แน่นอน
# ภายใน clues1
**แก้ไข**: ในแต่ละ "solutionLogic" ให้เขียนวิธีแก้เพื่อหาตัวแปรเดียวเท่านั้น เช่น  
"solutionLogic1_1": "จาก A + B + C = 12 หา A"  
โดยไม่ต้องแก้หาค่าตัวแปรทั้งหมดใน solutionLogic ให้โฟกัสการหาแค่ตัวแปรเดียวตามสมการนั้น

ตัวอย่างสมการเชาว์ง่าย เช่น
  "description1_1": "A + C = 7",
  "hint1_1": "B - C = 2",
  "solutionLogic1_1": "จาก A + B + C = 12 หา A"

# ภายใน clues2 puzzle sudoku ขนาด 4*4   
**เคร่งครัด
-ต้องเป็นไปตามกติกา  sudoku 4*4
-สร้าง sudoku ทุกตัวแปรเป็นเลขหลักเดียวทั้งหมด 
 *ตัวอย่าง
    "location2_1": "4,
    "description2_1": "2",
    "hint2_1": "3",
    "solutionLogic2_1": "1"

 ภายใน clues2 ต้องเป็นเลข 1-4 เท่านั้นห้ามมีตัวอักษร
สุดท้าย ให้คำนวณและระบุตัวเลข 4 หลักจริง ๆ ใน
- "finalCode1": ABCD
- "finalCode2": hint2_1 location2_2  description2_3 solutionLogic2_4

**สำคัญ:**
- สำหรับ "finalCode1" ให้ใช้เฉพาะค่าตัวแปรที่ถูก "หา" จาก solutionLogic1_1 ถึง solutionLogic1_4 ตามลำดับ เช่น  
  ถ้า solutionLogic1_1 = "หา A", solutionLogic1_2 = "หา C", solutionLogic1_3 = "หา E", solutionLogic1_4 = "หา G"  
  ให้ finalCode1 = A C E G (ตามลำดับ) เท่านั้น

โดยแต่ละตัวคือค่าของตัวแปรที่ได้จากการแก้สมการใน clues นั้น ๆ
โดยสมการและคำตอบจะเปลี่ยนแปลงทุกครั้งที่สร้างคำใบ้ใหม่และต้องง่ายมากๆ

**ข้อมูลที่ต้องมี:**
1. เนื้อเรื่องสั้น ๆ
2. คำพูดสำหรับการใบ้โดยแบ่งเป็น 2 ส่วน 1. puzzle สมาการตั้งแต่ srd1 ถึง srd5 เช่น "เอ๊ะ?!...บนกระดาษมีสัญลักษณะแบบเดียวกับตรงที่กรอกรหัสเลย" และ 2. puzzle sudoku ตั้งแต่ srd6 ถึง srd10  เช่น "อืมม...กระดานตรงนี้คล้ายๆ เกมซูโดกุเลยแฮะ"
3. clues1: 4 จุดในบ้านแรก (ห้องนั่งเล่น, ห้องน้ำ, ห้องครัว, ห้องนอน)
4. clues2: 4 ไม่ต้องสนตำแหน่ง ทุกตัวแปรแทนช่อง sudoku 

ตอบแค่ JSON ห้ามตอบอย่างอื่นอีก
**รูปแบบ JSON ตัวอย่าง:**

{{
  "story": "...",
 "selfReminders": {{
    "srd1":"พูดกับตัวเอง1",
    "srd2":"พูดกับตัวเอง 2",
    "srd3":"พูดกับตัวเอง 3",
    "srd4":"พูดกับตัวเอง4",
    "srd5":"พูดกับตัวเอง5",
    "srd6":"พูดกับตัวเอง 6",
    "srd7":"พูดกับตัวเอง 7",
    "srd8":"พูดกับตัวเอง8",
    "srd9":"พูดกับตัวเอง 9",
    "srd10":"พูดกับตัวเอง10"
  }},
  "clues1": {{
    "location1_1": "ห้องนั่งเล่น",
    "description1_1": "...สมการ...",
    "hint1_1": "...คำใบ้...",
    "solutionLogic1_1": "จาก A + B + C = 12 หา A",
    ...
    "location1_2": "ห้องน้ำ",
    "description1_2": "...",
    "hint1_2": "...",
    "solutionLogic1_2": "..."

    "location1_3": "ห้องครัว",
    "description1_3": "...",
    "hint1_3": "...",
    "solutionLogic1_3": "..."


    "location1_4": "ห้องนอน",
    "description1_4": "...",
    "hint1_4": "...",
    "solutionLogic1_4": "..."
  }},
  "clues2": {{
    "location2_1": "4,
    "description2_1": "2",
    "hint2_1": "3",
    "solutionLogic2_1": "1"

    "location2_2": "1",
    "description2_2": "2",
    "hint2_2": "4",
    "solutionLogic2_2": "3"

    "location2_3": "3",
    "description2_3": "4",
    "hint2_3": "1",
    "solutionLogic2_3": "2"


    "location2_4": "2",
    "description2_4": "1",
    "hint2_4": "3",
    "solutionLogic2_4": "4"
  }},
  "finalCode1": 1234,
  "finalCode2": 2144
}}
 """



#"""สร้างคำใบ้สำหรับเกม Escape Room VR โดยใช้ฉากบ้านธรรมดา รับบทเป็น {occupations} ผู้เล่นต้องหาตัวเลข 4 หลักจากการแก้สมการเชาว์ง่าย ๆ ในคำใบ้เพื่อล็อกออกจากบ้าน โดยผู้เล่นไม่สามารถหยิบจับสิ่งของได้ ต้องใช้การสังเกต วิเคราะห์ และจดจำเบาะแสเท่านั้น

# คำใบ้ในแต่ละจุด (8 จุด รวม 2 บ้าน) ประกอบด้วยสมการง่าย ๆ ที่ใช้ตัวแปร A,B,C,... แทนจำนวนเต็มบวก (1-9) สมการจะสุ่มเปลี่ยนไปทุกครั้งที่สร้างคำใบ้ โดยมีขั้นตอนและคำตอบที่แน่นอน

# **แก้ไข**: ในแต่ละ "solutionLogic" ให้เขียนวิธีแก้เพื่อหาตัวแปรเดียวเท่านั้น เช่น  
# "solutionLogic1_1": "จาก A + B + C = 12 หา A"  
# โดยไม่ต้องแก้หาค่าตัวแปรทั้งหมดใน solutionLogic ให้โฟกัสการหาแค่ตัวแปรเดียวตามสมการนั้น

# ตัวอย่างสมการเชาว์ง่าย เช่น
#   "description1_1": "A + C = 7",
#   "hint1_1": "B - C = 2",
#   "solutionLogic1_1": "จาก A + B + C = 12 หา A"

# สุดท้าย ให้คำนวณและระบุตัวเลข 4 หลักจริง ๆ ใน
# - "finalCode1": ABCD
# - "finalCode2": EFGH

# โดยแต่ละตัวคือค่าของตัวแปรที่ได้จากการแก้สมการใน clues นั้น ๆ
# โดยสมการและคำตอบจะเปลี่ยนแปลงทุกครั้งที่สร้างคำใบ้ใหม่และต้องง่ายมากๆ
# **ข้อมูลที่ต้องมี:**
# 1. เนื้อเรื่องสั้น ๆ
# 2. คำเตือนตัวเอง 10 ข้อ
# 3. clues1: 4 จุดในบ้านแรก (ห้องนั่งเล่น, ห้องน้ำ, ห้องครัว, ห้องนอน)
# 4. clues2: 4 จุดในบ้านสอง (ห้องนั่งเล่น, ห้องน้ำ, ห้องครัว, ห้องนอน)

# ตอบแค่ JSON ห้ามตอบอย่างอื่นอีก
# **รูปแบบ JSON ตัวอย่าง:**

# {{
#   "story": "...",
#  "selfReminders": {{
#     "srd1":"คำเตือน 1",
#     "srd2":"คำเตือน 2",
#     "srd3":"คำเตือน 3",
#     "srd4":"คำเตือน 4",
#     "srd5":"คำเตือน 5",
#     "srd6":"คำเตือน 6",
#     "srd7":"คำเตือน 7",
#     "srd8":"คำเตือน 8",
#     "srd9":"คำเตือน 9",
#     "srd10":"คำเตือน 10"
#   }},
#   "clues1": {{
#     "location1_1": "ห้องนั่งเล่น",
#     "description1_1": "...สมการ...",
#     "hint1_1": "...คำใบ้...",
#     "solutionLogic1_1": "จาก A + B + C = 12 หา A",
#     ...
#     "location1_2": "ห้องน้ำ",
#     "description1_2": "...",
#     "hint1_2": "...",
#     "solutionLogic1_2": "..."

#     "location1_3": "ห้องครัว",
#     "description1_3": "...",
#     "hint1_3": "...",
#     "solutionLogic1_3": "..."


#     "location1_4": "ห้องนอน",
#     "description1_4": "...",
#     "hint1_4": "...",
#     "solutionLogic1_4": "..."
#   }},
#   "clues2": {{
#     "location2_1": "ห้องนั่งเล่น",
#     "description2_1": "สมการ",
#     "hint2_1": "...คำใบ้...",
#     "solutionLogic2_1": "..."

#     "location2_2": "ห้องน้ำ",
#     "description2_2": "...",
#     "hint2_2": "...",
#     "solutionLogic2_2": "..."

#     "location2_3": "ห้องครัว",
#     "description2_3": "...",
#     "hint2_3": "...",
#     "solutionLogic2_3": "..."


#     "location2_4": "ห้องนอน",
#     "description2_4": "...",
#     "hint2_4": "...",
#     "solutionLogic2_4": "..."
#   }},
#   "finalCode1": 1234,
#   "finalCode2": 5678
# }}
#  """

# Prompt สำหรับปริศนา Escape Room
# TemplateRoom4="""สร้างคำใบ้สำหรับเกม Escape Room VR ที่ใช้ฉากบ้านธรรมดา รับบทเป็น{occupations} โดยผู้เล่นต้องหาตัวเลข 4 หลักจากคำใบ้เพื่อล็อกออกจากบ้าน ผู้เล่นไม่สามารถหยิบจับสิ่งของได้ และใช้แค่การสังเกต, วิเคราะห์ และจดจำเบาะแส

# สิ่งที่ต้องมี:
# 1. เนื้อเรื่องสั้น ๆ ที่บอกสถานการณ์และความลึกลับ
# 2. คำพูดเตือนตัวเองของผู้เล่นจำนวน 10 ข้อ ที่ช่วยให้ผู้เล่นโฟกัสกับการสังเกตและวิเคราะห์
# 3. คำใบ้ทั้งหมด 4 จุด (ในบ้านเดิมทุกครั้ง) คือ:
#    - ห้องนั่งเล่น → กระดาษเบาะแสจากเตาผิงไฟ
#    - ห้องน้ำ → กระดาษเบาะแสจากกระจกในไอน้ำ
#    - ห้องครัว → กระดาษเบาะแสบริเวณห้องครัว
#    - ห้องนอน → เบาะแสจากรูปถ่าย/วัตถุที่มองเห็นได้
#  4. คำใบ้ทั้งหมด 4 จุด (ในบ้านอีกหลัง) คือ:
#    - ห้องนั่งเล่น → กระดาษเบาะแสบริเวณของเล่นในห้องทั้ง 8 ชิ้น
#    - ห้องน้ำ → กระดาษเบาะแสจากบริเวณชักโครก
#    - ห้องครัว → กระดาษเบาะแสบริเวณตู้เย็น
#    - ห้องนอน → กระดาษเบาะแสจากเปียโน/วัตถุที่มองเห็นได้
# คำใบ้แต่ละข้อควรมี:
# - location: ระบุห้อง
# - description: คำอธิบายสิ่งที่ผู้เล่นเห็น
# - hint: คำใบ้ที่ช่วยให้ตีความได้
# - solutionLogic: วิธีตีความเพื่อให้ได้ตัวเลขจากจุดนั้น

# **รูปแบบคำตอบต้องอยู่ใน JSON มีโครงสร้างดังนี้:**
# json
# {{
#   "story": "เนื้อเรื่อง",
#   "selfReminders": {{
#     "srd1":"คำเตือน 1",
#     "srd2":"คำเตือน 2",
#     "srd3":"คำเตือน 3",
#     "srd4":"คำเตือน 4",
#     "srd5":"คำเตือน 5",
#     "srd6":"คำเตือน 6",
#     "srd7":"คำเตือน 7",
#     "srd8":"คำเตือน 8",
#     "srd9":"คำเตือน 9",
#     "srd10":"คำเตือน 10"
 
#   }},
#   "clues1": 
#     {{
#       "location1_1": "ห้อง",
#       "description1_1": "คำอธิบายสิ่งที่เห็น",
#       "hint1_1": "คำใบ้",
#       "solutionLogic1_1": "วิธีตีความหาเลขพร้อมเลขตัวนั้น"

#       "location1_2": "ห้อง",
#       "description1_2": "คำอธิบายสิ่งที่เห็น",
#       "hint1_2": "คำใบ้",
#       "solutionLogic1_2": "วิธีตีความหาเลขพร้อมเลขตัวนั้น"

#       "location1_3": "ห้อง",
#       "description1_3": "คำอธิบายสิ่งที่เห็น",
#       "hint1_3": "คำใบ้",
#       "solutionLogic1_3": "วิธีตีความหาเลขพร้อมเลขตัวนั้น"
 
#       "location1_3": "ห้อง",
#       "description1_3": "คำอธิบายสิ่งที่เห็น",
#       "hint1_3": "คำใบ้",
#       "solutionLogic1_3": "วิธีตีความหาเลขพร้อมเลขตัวนั้น"
 
#       "location1_4": "ห้อง",
#       "description1_4": "คำอธิบายสิ่งที่เห็น",
#       "hint1_4": "คำใบ้",
#       "solutionLogic1_4": "วิธีตีความหาเลขพร้อมเลขตัวนั้น"
#     }}
#   ,
#  "clues2": 
#     {{
#       "location2_1": "ห้อง",
#       "description2_1": "คำอธิบายสิ่งที่เห็น",
#       "hint2_1": "คำใบ้",
#       "solutionLogic2_1": "วิธีตีความหาเลขพร้อมเลขตัวนั้น"

#       "location2_2": "ห้อง",
#       "description2_2": "คำอธิบายสิ่งที่เห็น",
#       "hint2_2": "คำใบ้",
#       "solutionLogic2_2": "วิธีตีความหาเลขพร้อมเลขตัวนั้น"

     
#       "location2_3": "ห้อง",
#       "description2_3": "คำอธิบายสิ่งที่เห็น",
#       "hint2_3": "คำใบ้",
#       "solutionLogic2_3": "วิธีตีความหาเลขพร้อมเลขตัวนั้น"

#       "location2_4": "ห้อง",
#       "description2_4": "คำอธิบายสิ่งที่เห็น",
#       "hint2_4": "คำใบ้",
#       "solutionLogic2_4": "วิธีตีความหาเลขพร้อมเลขตัวนั้น"
#     }},
  
#   "finalCode1": "ตัวเลข 4 หลัก",
#    "finalCode2": "ตัวเลข 4 หลัก"
# }}"""

TemplateRoom3= """
ช่วยสร้างเรื่องราวสำหรับเกมโดยสวมบทบาทโดยผู้เล่นมีบทบาทโดยเป็น{occupations}
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
TemplateRoom2_2= """ช่วยสร้างเรื่องราวสำหรับเกมโดยผู้เล่นมีบทบาทโดยเป็น {occupation} ภายในอุโมงท่อน้ำที่ลึกลับ แนว Escape room ให้ผู้เล่นโดยเหตุใดต้องทำ 4 สิ่งนี้  
1.ต่อ box ข้ามสายน้ำ 
2.หยิบถังในห้องไปวางเพื่อเติมระยะห่างระหว่างบรรไดเพื่อออกห้อง 
3.ฝ่าไปกลางเขาวงกตสังเกตเลขบนเสื้อตัวตลก 5 ตัว และนำมากรอกแท่นกลางเขาวงกต เพื่อเอากุญแจ 
4.สร้าง puzzle จากวัตถุต่อไปนี้ 
1.สมุดโน๊ตที่เขียนว่า “บันทึกวันที่ 1 ดร.เสกสรรค์ ฉันได้รับคำให้มาทำภารกิจลับ” 1 โน๊ต
2.สมุดโน๊ตที่เขียนว่า “บันทึกวันที่ 10 ของดร.เสกสรรค์ ที่นี่มีสิ่งแปลกใหม่ ที่น่าสนใจอย่ามากเราอาจปฏิวัติโลกใบนี้ได้เลยนะ !!!!!” 1 โน๊ต
3.สมุดโน๊ตที่เขียนว่า “บันทึกวันที่ 126 ของดร.เสกสรรค์สิ่งที่เกิดที่นี้มันหาคำอธิบายไม่ได้!เราต้องรีบหนีอย่าให้โดนจับ...ใครที่เห็นข้อความนี้รีบ...” 1 โน๊ต
4.ธงสีม่วง 1 ผืน
5.ธงสีฟ้า 1 ผืน
6.ถัง 3 ใบ
7.เก้าอี้ 1 ตัว

8.{object8}
9.{object9}
10.{object10}
11.{object11}
12.{object12}
13.{object13}
14.{object14}
15.{object15}
16.{object16}


โดยที่เป็น puzzle สุดท้าย และรับคำตอบเป็น pin 4 หลัก พร้อมทั้งคิดเรื่องที่เชื่อมกับเหตุการณ์ก่อนหน้าด้วย

ตอบในรูปแบบ JSON: {{
 "roleAndStory": "สิ่งนี้เป็นเรื่องราว", 
 "reasonDoing1": {{
  "easy": "เป็นบทพูดที่พูดกับตัวเอง", 
  "normal": "เป็นบทพูดที่พูดกับตัวเอง", 
  "hard": "เป็นบทพูดที่พูดกับตัวเอง" 
 }}, 
 "reasonDoing2": {{
  "easy": "...", 
  "normal": "...", 
  "hard": "..."
  }}, 
 "reasonDoing3": {{,
  "easy": "เป็นบทพูดที่พูดกับตัวเอง", 
  "normal": "เป็นบทพูดที่พูดกับตัวเอง", 
  "hard": "เป็นบทพูดที่พูดกับตัวเอง" 
 }},


 "reasonDoing4": {{ 
  “dialogue” : “....”,
  "easy": {{
   “answer”: “1234”,
   “hint1”: “คำพูดใบ้หลักที่ 1”,
   “hint2”: “คำพูดใบ้หลักที่ 2”,
   “hint4”: “คำพูดใบ้หลักที่ 3”,
   “hint4”: “คำพูดใบ้หลักที่ 4”,
  }}, 
  "normal": {{
   “answer”: “1234”,
   “hint1”: “คำพูดใบ้หลักที่ 1”,
   “hint2”: “คำพูดใบ้หลักที่ 2”,
   “hint3”: “คำพูดใบ้หลักที่ 3”,
   “hint4”: “คำพูดใบ้หลักที่ 4”,
  }}, 
  "hard": {{
   “answer”: “1234”,
   “hint1”: “คำพูดใบ้หลักที่ 1”,
   “hint2”: “คำพูดใบ้หลักที่ 2”,
   “hint3”: “คำพูดใบ้หลักที่ 3”,
   “hint4”: “คำพูดใบ้หลักที่ 4”,
  }}
 }}
}}
"""
TemplateRoom1="""ช่วยตอบทุกระดับของทุก puzzle (easy, medium, hard) ภายในคำตอบนี้โดยไม่แบ่งเป็นหลายรอบ
ช่วยคิดเรื่องราวพร้อมบทพูดของ {occupations} ความยาวไม่เกิน 500 ตัวอักษร โดยที่สถานการณ์ตอนนี้คือยานเกิดอุบัติเหตุก่อนหน้า และเมื่อเกิดมีอุกกาบาตกำลังจะพุ่งชนยาน ต้องเปิดระบบป้องกันยาน
ช่วยคิดปริศณาแนว escape room สถานที่ยานอวกาศ โดยห้ามใช้วัตถุที่บอก มีความยากง่าย 3 ระดับคือ ง่าย, กลาง, ยาก และมีคำใบ้(hint) ที่เป็นแนวพูดให้ทำเช่น "เอ๊ะ…ฉันคิดว่าที่ไฟมีกระพริบเป็นแพทเทิร์นนะ"
1.
มีหลอดไฟสีแดงจำนวน 1
มีหลอดไฟสีน้ำเงินจำนวน 1
มีหลอดไฟสีเขียวจำนวน 1 
มีหลอดไฟสีชมพูจำนวน 1
กำหนดจำนวนครั้งที่ไฟกระพริบ ไฟกระพริบด้วยความถี่ที่เท่ากัน ตอบเป็นตัวเลขเช่น lightBulb1 กระพริบ 1, lightBulb2 กระพริบ 2, lightBulb3 กระพริบ 3, lightBulb3 กระพริบ 3 ตอบ "1234" พร้อมบทพูดที่สอดคล้องกับการเปิดประตู

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
รูปภาพเอดา เลิฟเลซ ต่ำแหน่ง รองกัปตัน และสถาปนิกระบบ AI ยาน DPU จำนวน 1 รูป
ตู้ล็อกเกอร์เปล่า 5 ตู้
กล่อง 35 กล่อง
ชั้นวางของ 5 ชิ้น
คิด puzzle ที่สอดคล้องกับสถานที่ตอบคำตอบอยู่ที่หัวยานเป็น puzzle จบเกม และที่รับการเช็คเป็นการกดปุ่มตัวเลข pin 6 หลักใช้วัตถุเท่าที่บอก และ hint1 คือตำแหล่งนี้ได้มาจากอะไร เช่น "พยางชื่อของดร. อาจมีความสำคัญกับการตอบนะ" = ตอบ 2

{{
"story" : "…",
"puzzle1": {{
 "story": "บทพูดที่นำพาให้มาทำ puzzle นี้",
   "easy": {{
  "speech" : "....",
  "lightBulb1": "ตัวเลข",
  "lightBulb2": "ตัวเลข",
  "lightBulb3": "ตัวเลข",
  "lightBulb4": "ตัวเลข",
  "answer": "ตัวเลข"
 }}
    "medium": {{"story": "บทพูดที่นำพาให้มาทำ puzzle นี้",
   "easy": {{
  "speech" : "....",
  "lightBulb1": "ตัวเลข",
  "lightBulb2": "ตัวเลข",
  "lightBulb3": "ตัวเลข",
  "lightBulb4": "ตัวเลข",
  "answer": "ตัวเลข"}},
 "hard": {{"story": "บทพูดที่นำพาให้มาทำ puzzle นี้",
   "easy": {{
  "speech" : "....",
  "lightBulb1": "ตัวเลข",
  "lightBulb2": "ตัวเลข",
  "lightBulb3": "ตัวเลข",
  "lightBulb4": "ตัวเลข",
  "answer": "ตัวเลข"}}
}},
"puzzle2": {{
 "story": "บทพูดที่นำพาให้มาทำ puzzle นี้",
 "easy": {{
  "speech" : "....",
  "total_value": "….",
  "hint": "…",
  "blue_battery": 
  {{
   "blue1": "....",
    "blue2": "....",
   "blue3": "....",
    "blue4": "....",
  }},
  "grey_battery": {{   
    "grey1": "....",
    "grey2": "....",
   "grey3": "....",
    "grey4": "....",
    }},
  "red_battery": {{
     "red1": "....",
    "red2": "....",
   "red3": "....",
    "red4": "....",
  }},
  "yellow_battery": {{
       "yellow1": "....",
    "yellow2": "....",
   "yellow3": "....",
    "yellow4": "....",
    }},
 }},
 “medium": {{
 "speech" : "....",
  "total_value": "….",
  "hint": "…",
  "blue_battery": 
  {{
   "blue1": "....",
    "blue2": "....",
   "blue3": "....",
    "blue4": "....",
  }},
  "grey_battery": {{   
    "grey1": "....",
    "grey2": "....",
   "grey3": "....",
    "grey4": "....",
    }},
  "red_battery": {{
     "red1": "....",
    "red2": "....",
   "red3": "....",
    "red4": "....",
  }},
  "yellow_battery": {{
       "yellow1": "....",
    "yellow2": "....",
   "yellow3": "....",
    "yellow4": "....",
    }},
 }},
 "hard": {{
 "speech" : "....",
  "total_value": "….",
  "hint": "…",
  "blue_battery": 
  {{
   "blue1": "....",
    "blue2": "....",
   "blue3": "....",
    "blue4": "....",
  }},
  "grey_battery": {{   
    "grey1": "....",
    "grey2": "....",
   "grey3": "....",
    "grey4": "....",
    }},
  "red_battery": {{
     "red1": "....",
    "red2": "....",
   "red3": "....",
    "red4": "....",
  }},
  "yellow_battery": {{
       "yellow1": "....",
    "yellow2": "....",
   "yellow3": "....",
    "yellow4": "....",
    }},
}},
"puzzle3": {{
 "story": "บทพูดที่นำพาให้มาทำ puzzle นี้",
 "easy": {{
  "speech" : "....",
  "hint": "…",
  "typeIC": "...",
  "ic": Boolean,
  "led": Boolean,
  "buttonInput1": Boolean,
  "buttonInput2": Boolean,
  "wireVccToIC": Boolean,
  "wireGndToIC": Boolean,
  "wireBtn1ToIC": Boolean,
  "wireBtn2ToIC": Boolean,
  "wireLedToIC": Boolean,
 }},
 "medium": {{"story": "บทพูดที่นำพาให้มาทำ puzzle นี้",
 "easy": {{
  "speech" : "....",
  "hint": "…",
  "typeIC": "...",
  "ic": Boolean,
  "led": Boolean,
  "buttonInput1": Boolean,
  "buttonInput2": Boolean,
  "wireVccToIC": Boolean,
  "wireGndToIC": Boolean,
  "wireBtn1ToIC": Boolean,
  "wireBtn2ToIC": Boolean,
  "wireLedToIC": Boolean,}},
 "hard": {{"story": "บทพูดที่นำพาให้มาทำ puzzle นี้",
 "easy": {{
  "speech" : "....",
  "hint": "…",
  "typeIC": "...",
  "ic": Boolean,
  "led": Boolean,
  "buttonInput1": Boolean,
  "buttonInput2": Boolean,
  "wireVccToIC": Boolean,
  "wireGndToIC": Boolean,
  "wireBtn1ToIC": Boolean,
  "wireBtn2ToIC": Boolean,
  "wireLedToIC": Boolean,}}
}},
"puzzle4": {{
 "story": "บทพูดที่นำพาให้มาทำ puzzle นี้",
 "easy": {{
  "speech1" : "บทพูดที่ชวนให้ออกเดินหาคำตอบ",
  "speech2" : "....",
  "hint1": "…",
  "hint2": "…",
  "hint3": "…",
  "hint4": "…",
  "hint5": "…",
  "hint6": "…",
  "ans": "123456"
 }},
 "medium": {{ "story": "บทพูดที่นำพาให้มาทำ puzzle นี้",
 "easy": {{
  "speech1" : "บทพูดที่ชวนให้ออกเดินหาคำตอบ",
  "speech2" : "....",
  "hint1": "…",
  "hint2": "…",
  "hint3": "…",
  "hint4": "…",
  "hint5": "…",
  "hint6": "…",
  "ans": "123456"}},
 "hard": {{ "story": "บทพูดที่นำพาให้มาทำ puzzle นี้",
 "easy": {{
  "speech1" : "บทพูดที่ชวนให้ออกเดินหาคำตอบ",
  "speech2" : "....",
  "hint1": "…",
  "hint2": "…",
  "hint3": "…",
  "hint4": "…",
  "hint5": "…",
  "hint6": "…",
  "ans": "123456"}}
}}
}}"""
@app.post('/room4')
async def gen_puzzleT(request : Request):
    data = await request.json() # request จาก unity
    pt = ChatPromptTemplate.from_template(TemplateRoom4)
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
    pt = ChatPromptTemplate.from_template(TemplateRoom2_2)
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