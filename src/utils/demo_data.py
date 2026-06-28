import random

# デモロット初期データ
DEMO_LOTS = [
    {
        "id": "DEMO_LOT1",
        "farm_name": "KAISHI農場",
        "house_number": "1号棟",
        "crop_type": "トマト",
        "crop_variety": "シンディー",
        "plant_count": 540,
    },
    {
        "id": "DEMO_LOT2",
        "farm_name": "KAISHI農場",
        "house_number": "2号棟",
        "crop_type": "メロン",
        "crop_variety": "アールス",
        "plant_count": 320,
    },
    {
        "id": "DEMO_LOT3",
        "farm_name": "KAISHI農場",
        "house_number": "3号棟",
        "crop_type": "トマト",
        "crop_variety": "フルティカ",
        "plant_count": 480,
    },
]


def generate_ai_summary(
    crop_type: str,
    crop_variety: str | None,
    plant_condition: int,
    pest_condition: int,
    comment: str | None,
) -> str:
    """植物・病害虫スコアとコメントをもとにダミーAIまとめを生成する"""
    variety = f"（{crop_variety}）" if crop_variety else ""

    plant_desc = {
        1: "生育が不良で早急な対応が必要です",
        2: "生育がやや不良で注意が必要です",
        3: "生育はやや緩慢ですが、深刻な問題はありません",
        4: "生育は順調で良好な状態です",
        5: "生育は非常に良好で最良の状態です",
    }.get(plant_condition, "生育状況は普通です")

    pest_desc = {
        1: "病害虫の被害が深刻で即座の防除が必要です",
        2: "病害虫の兆候があり、早めの対応を推奨します",
        3: "病害虫の発生リスクがあるため、引き続き観察が必要です",
        4: "病害虫の発生はほとんど見られません",
        5: "病害虫の発生は確認されませんでした",
    }.get(pest_condition, "病害虫の状況は普通です")

    summary = f"本日の{crop_type}{variety}の状況をまとめます。{plant_desc}。{pest_desc}。"

    if comment:
        snippet = comment[:60] + "…" if len(comment) > 60 else comment
        summary += f"作業者のコメントによると、{snippet}とのことです。"

    summary += "引き続き適切な管理を継続してください。"
    return summary


def generate_temperature() -> float:
    """気温のランダム値を生成する（20〜30℃、小数点1桁）"""
    return round(random.uniform(20.0, 30.0), 1)


def generate_humidity() -> float:
    """湿度のランダム値を生成する（50〜70%、小数点1桁）"""
    return round(random.uniform(50.0, 70.0), 1)
