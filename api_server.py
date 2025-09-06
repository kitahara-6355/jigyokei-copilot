# -*- coding: utf-8 -*-
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os
from dotenv import load_dotenv
import google.generativeai as genai

# --- ▼▼▼ ここに認証処理を追加 ▼▼▼ ---
# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からAPIキーを取得して設定
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("APIキーが.envファイルに設定されていません。")
genai.configure(api_key=api_key)
# --- ▲▲▲ 認証処理はここまで ▲▲▲ ---

# 思考エンジンと表示エンジンをインポート
from risk_analyzer import analyze_conversation_for_risks
from presentation_generator import create_risk_list_presentation, create_solution_presentation

# FastAPIアプリケーションを初期化
app = FastAPI()

# --- APIが受け取るデータの型を定義 ---
class ConversationRequest(BaseModel):
    conversation_log: str

# --- APIの「受付窓口」を定義 ---
@app.post("/analyze")
def analyze_endpoint(request: ConversationRequest):
    """
    会話ログを受け取り、リスク分析とプレゼンテーション生成を行うAPIエンドポイント。
    """
    analysis_result = analyze_conversation_for_risks(request.conversation_log)

    if not analysis_result or not analysis_result.get("risks"):
        return {"error": "リスクは検出されませんでした。"}

    risk_presentation = create_risk_list_presentation(analysis_result)
    solution_presentation = create_solution_presentation(analysis_result)

    return {
        "raw_analysis": analysis_result,
        "risk_presentation_text": risk_presentation,
        "solution_presentation_text": solution_presentation
    }

# --- サーバーを起動するための記述 ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)