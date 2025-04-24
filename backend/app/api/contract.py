from fastapi import APIRouter, HTTPException
from app.core.contract_renderer import ContractRenderer
from app.schemas import ContractData

router = APIRouter()


@router.post("/generate")
def generate_contract(request: ContractData):
    try:
        renderer = ContractRenderer(list(request.model_dump().values()))
        filename = renderer.save_docx()
        renderer.convert_to_pdf(filename)
        return {"status": "success",
                "filename": filename,
                "message": "合同文件已生成"
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
