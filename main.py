from fastapi import FastAPI,UploadFile,Form,Request,Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse,Response
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from typing import Annotated
import sqlite3 
# sqllite3를 연결할 수 있는 라이브러리

con = sqlite3.connect('db.db',check_same_thread=False)
# 기존에 프로젝트 내부에 만든 db와 연결할 있게끔 하는 코드  
cur = con.cursor()
# 내부에서 sql문으로 변경한 후에 데이터베이스오 접속하여 값을 가지고 오는것
cur.execute(f"""
            CREATE TABLE IF NOT EXISTS items(
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                image BLOB,
                price INTEGER NOT NULL,
                description TEXT,
                place TEXT NOT NULL
            );
        """)
app = FastAPI()

#시크릿키를 생성하는 명렁어
SERCRET = "super-coding"
manager = LoginManager(SERCRET,'/login')

#query_user를 조죄할 떄 토큰도 같이 발급을 한다.
@manager.user_loader()
def query_user(data):
    WHERE_STATEMENTS = f'id="{data}"'
    if type(data) == dict:
        WHERE_STATEMENTS = f'id="{data['id']}"'
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    user = cur.execute(f"""
                       SELECT * FROM users WHERE {WHERE_STATEMENTS}
                       """).fetchone()
    return user

@app.post("/login")
def login(id:Annotated[str,Form()],
        password:Annotated[str,Form()]):
    user = query_user(id)
    if not user:
        #raise : 파이썬에서 에러메세지를 보내기 위한 것 
        #InvalidCredentialsException
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException
    #토큰 만들어주는 코드()
    acces_token = manager.create_access_token(data={
        'sub' :{
            'id' : user['id'],
            'name' : user['name'],
            'email': user['email']
        } 
    })
    
    return {"acces_token":acces_token}
    
@app.post('/signup')
def signup(id:Annotated[str,Form()],
           password:Annotated[str,Form()],
           name:Annotated[str,Form()],
           email:Annotated[str,Form()]
           ):
    cur.execute(f"""
                INSERT INTO users(id,name,email,password)
                VALUES ('{id}','{name}','{email}','{password}')
                """)
    con.commit()
    return "200"
    
            
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
#user=Depends(manager) 로그인이 유지되고 있을때
async def get_items(user=Depends(manager)):
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