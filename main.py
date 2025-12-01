from fastapi import FastAPI, Form, Request, Query
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Model JSON
class SensorData(BaseModel):
    temp: float
    hum: float

# ===== GET API =====
@app.get("/get")
def get_data(temp: float = Query(...), hum: float = Query(...)):
    print(f"[GET] Temp={temp} | Hum={hum}")
    return {"status": "success", "method": "GET", "temp": temp, "hum": hum}

# ===== POST API =====
@app.post("/post")
async def post_data(
    request: Request,
    temp: float = Form(None),
    hum: float = Form(None)
):
    # Trường hợp 1: JSON
    if (temp is None or hum is None):
        try:
            json_body = await request.json()
            temp = json_body.get("temp")
            hum = json_body.get("hum")
            print(f"[POST-JSON] Temp={temp} | Hum={hum}")
        except:
            return {"error": "Invalid JSON or Form"}

    # Trường hợp 2: Form URL-Encoded
    else:
        print(f"[POST-FORM] Temp={temp} | Hum={hum}")

    return {"status": "success", "method": "POST", "temp": temp, "hum": hum}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
