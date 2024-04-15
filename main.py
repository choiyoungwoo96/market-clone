from fastapi import FastAPI,UploadFile,Form,Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse,Response
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from typing import Annotated
import sqlite3 
# sqllite3를 연결할 수 있는 라이브러리

con = sqlite3.connect('db.db',check_same_thread=False)
# 기존에 프로젝트 내부에 만든 db와 연결할 있게끔 하는 코드  
cur = con.cursor()
# 내부에서 sql문으로 변경한 후에 데이터베이스오 접속하여 값을 가지고 오는것

app = FastAPI()

@app.post("/items")
async def create_item(image:UploadFile,
                title:Annotated[str,Form()],
                price:Annotated[int,Form()],
                description:Annotated[str,Form()],
                place:Annotated[str,Form()],
                insertAt:Annotated[int,Form()]
                ):
    image_byte = await image.read()
    cur.execute(f"""
                INSERT INTO items(title,image,price,description,place,insertAt)
                VALUES ('{title}','{image_byte.hex()}',{price},'{description}','{place}',{insertAt})
                """)
    con.commit()
    return "200"

@app.get("/items")
async def get_items():
    # 컬럼명까지 가지고올수 있도록 명령어
    con.row_factory = sqlite3.Row
    # db 현재 위치는 업데이틀 랗기 위한 것
    cur = con.cursor()
    rows = cur.execute(f"""
                       SELECT * FROM items;
                       """).fetchall()
    # fetchall() : 가져오는 경우에 써야 되는 문구
    return JSONResponse(jsonable_encoder(dict(row) for row in rows))
    # JSONResponse 리턴값에 json형식으로 바꾸지 위한 라이브러리
    # jsonable_encoder JSONReponse로형식으로 보낼때 인코딩을 해서 보내야 할때 사용하는 라이브러리
    # dict object로 만들어주는 함수

@app.get("/images/{item_id}")
async def get_image(item_id):
    cur = con.cursor();
    image_bytes = cur.execute(f"""
                              SELECT image FROM items WHERE id={item_id}
                              """).fetchone()[0]
    return Response(content=bytes.fromhex(image_bytes))

app.mount("/", StaticFiles(directory="frontend",html="True"), name="frontend")