from typing import Optional

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from schema.lot_schema import LotCreate, LotUpdate
from services import lot_service

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# ロット一覧
@router.get("/", response_class=HTMLResponse)
async def lots_show(request: Request, toast: str = "", db: Session = Depends(get_db)):
    lots = lot_service.get_all_lots(db)
    toast_messages = {
        "lot_created": "ロットを登録しました",
        "lot_saved": "ロットを保存しました",
    }
    toast_msg = toast_messages.get(toast, "")
    return templates.TemplateResponse(
        request,
        "lots_show.html",
        {"lots": lots, "toast_msg": toast_msg},
    )


# ロット登録ダイアログ（新規） — /{lot_id}/... より先に定義する
@router.get("/lots/dialog/new", response_class=HTMLResponse)
async def dialog_new(request: Request):
    return templates.TemplateResponse(
        request,
        "components/lot_registration_dialog.html",
        {"lot": None, "mode": "new"},
    )


# ロット編集ダイアログ
@router.get("/lots/{lot_id}/dialog/edit", response_class=HTMLResponse)
async def dialog_edit(lot_id: str, request: Request, db: Session = Depends(get_db)):
    lot = lot_service.get_lot_by_id(db, lot_id)
    return templates.TemplateResponse(
        request,
        "components/lot_registration_dialog.html",
        {"lot": lot, "mode": "edit"},
    )


# ロット新規登録
@router.post("/lots")
async def create_lot(
    lot_id: str = Form(...),
    farm_name: str = Form(...),
    house_number: str = Form(...),
    crop_type: str = Form(...),
    crop_variety: Optional[str] = Form(None),
    plant_count: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    data = LotCreate(
        id=lot_id,
        farm_name=farm_name,
        house_number=house_number,
        crop_type=crop_type,
        crop_variety=crop_variety or None,
        plant_count=int(plant_count) if plant_count and plant_count.strip() else None,
    )
    lot_service.create_lot(db, data)
    response = Response(status_code=204)
    response.headers["HX-Redirect"] = "/?toast=lot_created"
    return response


# ロット更新
@router.post("/lots/{lot_id}/update")
async def update_lot(
    lot_id: str,
    farm_name: str = Form(...),
    house_number: str = Form(...),
    crop_type: str = Form(...),
    crop_variety: Optional[str] = Form(None),
    plant_count: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    data = LotUpdate(
        farm_name=farm_name,
        house_number=house_number,
        crop_type=crop_type,
        crop_variety=crop_variety or None,
        plant_count=int(plant_count) if plant_count and plant_count.strip() else None,
    )
    lot_service.update_lot(db, lot_id, data)
    response = Response(status_code=204)
    response.headers["HX-Redirect"] = "/?toast=lot_saved"
    return response


# ロット削除
@router.post("/lots/{lot_id}/delete")
async def delete_lot(lot_id: str, db: Session = Depends(get_db)):
    lot_service.delete_lot(db, lot_id)
    response = Response(status_code=204)
    response.headers["HX-Redirect"] = "/"
    return response
