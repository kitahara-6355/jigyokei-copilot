# -*- coding: utf-8 -*-
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os
from dotenv import load_dotenv
import google.generativeai as genai
# --- ▼▼▼ CORS設定のために追加 ▼▼▼ ---
from fastapi.middleware.cors import CORSMiddleware
# --- ▲▲▲ ---

# --- 認証処理 ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("APIキーが.envファイルに設定されていません。")
genai.configure(api_key=api_key)

# 思考エンジンと表示エンジンをインポート
from risk_analyzer import analyze_conversation_for_risks
from presentation_generator import create_risk_list_presentation, create_solution_presentation

# FastAPIアプリケーションを初期化
app = FastAPI()

# --- ▼▼▼ CORS設定を追加 ▼▼▼ ---
# 許可するオリジン（アクセス元）のリスト。"*"はすべてを許可（開発時に便利）
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # すべてのHTTPメソッドを許可
    allow_headers=["*"], # すべてのHTTPヘッダーを許可
)
# --- ▲▲▲ ---


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