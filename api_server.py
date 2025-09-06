# -*- coding: utf-8 -*-
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# 思考エンジンと表示エンジンをインポート
from risk_analyzer import analyze_conversation_for_risks
from presentation_generator import create_risk_list_presentation, create_solution_presentation

# FastAPIアプリケーションを初期化
app = FastAPI()

# --- APIが受け取るデータの方を定義 ---
class ConversationRequest(BaseModel):
    conversation_log: str

# --- APIの「受付窓口」を定義 ---
@app.post("/analyze")
def analyze_endpoint(request: ConversationRequest):
    """
    会話ログを受け取り、リスク分析とプレゼンテーション生成を行うAPIエンドポイント。
    """
    # 思考エンジンを実行
    analysis_result = analyze_conversation_for_risks(request.conversation_log)
    
    if not analysis_result or not analysis_result.get("risks"):
        return {"error": "リスクは検出されませんでした。"}
    
    # 表示エンジンを実行
    risk_presentation = create_risk_list_presentation(analysis_result)
    solution_presentation = create_solution_presentation(analysis_result)
    
    # フロントエンド（GUIアプリ）が使いやすいように、結果をまとめて返す
    return {
        "raw_analysis": analysis_result,
        "risk_presentation_text": risk_presentation,
        "solution_presentation_text": solution_presentation
    }

# --- サーバーを起動するための記述 ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)