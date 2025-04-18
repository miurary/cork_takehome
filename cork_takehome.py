from datetime import datetime
from flask import Flask, request
from enum import Enum
from pydantic import BaseModel
import sqlite3
import json
from waitress import serve
from uuid import uuid4

app = Flask(__name__)

con = sqlite3.connect("main.db", check_same_thread=False)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS login_data(p_id integer primary key autoincrement, tenant_id text not null, user_id text not null, origin text not null, status text not null, date timestamp not null, i_key text not null)")

class LoginStatus(str, Enum):
    success = 'success'
    fail = 'fail'


class LoginData(BaseModel):
    tenant_id: str
    user_id: str
    origin: str
    status: LoginStatus
    date: datetime
    i_key: str # idempotency key passed from client


@app.route('/ingest_login_data', methods=['POST'])
def ingest_login_data():
    login_data = LoginData(**request.json) # add try catch here and raise on error

    data = cur.execute("SELECT * FROM login_data WHERE i_key=?", (login_data.i_key,)).fetchone()

    if data:
        json_data = { "date": data[5], "i_key": data[6], "origin": data[3], "status": data[4], "tenant_id": data[1], "user_id": data[2] }
        response_data = LoginData(**json_data)
        return response_data.model_dump()
    else:
        insert_params = (login_data.tenant_id, login_data.user_id, login_data.origin, login_data.status, login_data.date, login_data.i_key, )
        cur.execute(f"INSERT INTO login_data VALUES (null, ?, ?, ?, ?, ?, ? )", insert_params)

        return login_data.model_dump()

@app.route('/suspicious_events', methods=['GET'])
def suspicious_events():
    data = cur.execute("select count(origin) from (select origin from login_data where status = 'fail' and login_data.date >= date('now', '-5 minute') group by origin").fetchall()
    return str(datetime.now()) + " " + str(uuid4())

serve(app, host="0.0.0.0", port=5000)