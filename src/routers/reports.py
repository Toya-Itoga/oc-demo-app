import json
import os
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from services import lot_service, report_service
from utils.datetime_utils import format_date_dot, format_date_jp, format_date_short

router = APIRouter(prefix="/lots")
templates = Jinja2Templates(directory="templates")


# 最新レポートへのリダイレクト — /{lot_id}/report/{report_id} より先に定義する
@router.get("/{lot_id}/report/latest")
async def view_latest_report(lot_id: str, db: Session = Depends(get_db)):
    reports = report_service.get_reports_by_lot(db, lot_id)
    if not reports:
        return RedirectResponse(url=f"/lots/{lot_id}/report/new")
    return RedirectResponse(url=f"/lots/{lot_id}/report/{reports[0].id}")


# 日報作成・編集画面 — /{lot_id}/report/{report_id} より先に定義する
@router.get("/{lot_id}/report/new", response_class=HTMLResponse)
async def report_new(request: Request, lot_id: str, db: Session = Depends(get_db)):
    lot = lot_service.get_lot_by_id(db, lot_id)
    if not lot:
        return RedirectResponse(url="/")
    existing = report_service.get_today_report(db, lot_id)
    existing_photos: list[str] = []
    if existing and existing.photo_paths:
        existing_photos = json.loads(existing.photo_paths)
    return templates.TemplateResponse(
        request,
        "report_registration.html",
        {
            "lot": lot,
            "existing": existing,
            "existing_photos": existing_photos,
        },
    )


# 日報保存
@router.post("/{lot_id}/report")
async def save_report(
    lot_id: str,
    plant_condition: int = Form(...),
    pest_condition: int = Form(...),
    comment: Optional[str] = Form(None),
    existing_paths: list[str] = Form(default=[]),
    photos: list[UploadFile] = File(default=[]),
    db: Session = Depends(get_db),
):
    lot = lot_service.get_lot_by_id(db, lot_id)
    if not lot:
        return {"error": "lot not found"}, 404

    # 新規写真を保存する
    saved_paths: list[str] = list(existing_paths)
    from utils.datetime_utils import get_today_str
    from ulid import ULID

    os.makedirs("imgs", exist_ok=True)
    for upload in photos:
        if not upload.filename:
            continue
        ext = os.path.splitext(upload.filename)[1].lower() or ".jpg"
        filename = f"{get_today_str()}_{str(ULID())}{ext}"
        filepath = f"imgs/{filename}"
        content = await upload.read()
        with open(filepath, "wb") as f:
            f.write(content)
        saved_paths.append(filepath)
        # 写真は最大3枚
        if len(saved_paths) >= 3:
            break

    report = report_service.create_or_update_report(
        db=db,
        lot_id=lot_id,
        crop_type=lot.crop_type,
        crop_variety=lot.crop_variety,
        plant_condition=plant_condition,
        pest_condition=pest_condition,
        comment=comment or None,
        photo_paths=saved_paths,
    )
    return {"redirect": f"/lots/{lot_id}/report/{report.id}?new=1"}


# 日報閲覧
@router.get("/{lot_id}/report/{report_id}", response_class=HTMLResponse)
async def report_show(
    request: Request,
    lot_id: str,
    report_id: str,
    new: str = "",
    db: Session = Depends(get_db),
):
    lot = lot_service.get_lot_by_id(db, lot_id)
    report = report_service.get_report_by_id(db, report_id)
    if not lot or not report:
        return RedirectResponse(url="/")

    # タイムライン：このロットの全レポート
    all_reports = report_service.get_reports_by_lot(db, lot_id)
    timeline = [
        {
            "id": r.id,
            "date_label": format_date_short(r.date),
            "plant": r.plant_condition,
            "pest": r.pest_condition,
            "is_active": r.id == report_id,
            "url": f"/lots/{lot_id}/report/{r.id}",
        }
        for r in all_reports
    ]

    # 写真パスリスト
    photo_paths: list[str] = []
    if report.photo_paths:
        photo_paths = json.loads(report.photo_paths)

    return templates.TemplateResponse(
        request,
        "report_show.html",
        {
            "lot": lot,
            "report": report,
            "photo_paths": photo_paths,
            "timeline": timeline,
            "date_jp": format_date_jp(report.date),
            "is_new": new == "1",
        },
    )
