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
def get_data(
    response: Response,  # Đối tượng để can thiệp vào HTTP Header
    temp: float = Query(None), 
    hum: float = Query(None), 
    motion: int = Query(0)
):
    # Kiểm tra dữ liệu đầu vào (Validation thủ công)
    if temp is None or hum is None:
        # Nếu thiếu dữ liệu, set HTTP Code thành 400 (Bad Request)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "http_code": 400,
            "status": "error",
            "message": "Thieu tham so temp hoac hum"
        }

    # Nếu thành công
    print(f"[GET] Temp={temp} | Hum={hum} | Motion={motion}")
    response.status_code = status.HTTP_200_OK # Set header thực tế
    
    return {
        "http_code": 200,          # Trả về code trong JSON để tiện check
        "status": "success", 
        "temp": temp, 
        "hum": hum, 
        "motion": motion
    }
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
