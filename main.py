from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import pdfplumber

app = FastAPI()

@app.get("/get_cte")
async def get_cte(tipo: str):
    if tipo.lower() not in ["gas", "luce"]:
        raise HTTPException(status_code=400, detail="Parametro tipo invalido (scegli gas o luce)")
    
    file_path = f"./pdf/sorgenia_{tipo.lower()}.pdf"
    
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        return JSONResponse({"tipo": tipo.lower(), "contenuto": text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
