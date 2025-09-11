# -*- coding: utf-8 -*-
from fastapi import FastAPI
from pydantic import BaseModel
import os
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
import json
import textwrap

# --- 認証処理 ---
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("警告: 環境変数 GOOGLE_API_KEY が設定されていません。")

# --- FastAPIアプリケーションを初期化 ---
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- AI思考エンジンの機能 ---
# (以前提供した、analyze_conversation_for_risks と map_risk_to_solution 関数をここに含める)
def map_risk_to_solution(risk_summary: str) -> str:
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    prompt = textwrap.dedent(f"""
        あなたは商工会の共済制度に詳しい専門家です。
        以下に提示される単一の「経営リスク」の概要文を読み、リストの中から最も適切な「解決策」を一つだけ選んで、その名称のみを返答してください。
        # 解決策リスト
        - "商工会の福祉共済, 経営者休業補償制度": 経営者や従業員の病気・ケガによる休業や所得減少を補償する。
        - "業務災害保険": 従業員の労働災害（労災）に対する企業の賠償責任を補償する。
        - "火災共済（店舗・設備補償）": 火災や水災による建物や設備の損害を補償する。
        - "ビジネス総合保険（PL責任補償）": 食中毒などの賠償責任に加え、サイバー攻撃による損害なども幅広く補償する。
        - "経営セーフティ共済": 取引先の倒産による売掛金回収不能などの損害に備える。
        - "地震保険, 地震特約": 地震による損害を補償する。
        - "個別相談": 上記のいずれにも明確に当てはまらない場合。
        # 入力される経営リスク
        {risk_summary}
        # 出力（解決策の名称のみを記述すること）
        """)
    response = model.generate_content(prompt)
    return response.text.strip()

def analyze_conversation_for_risks(conversation_log: str) -> dict:
    risk_extraction_model = genai.GenerativeModel('gemini-1.5-flash-latest')
    risk_extraction_prompt = textwrap.dedent(f"""
        あなたは聞き上手なリスクコンサルタントです。
        以下の会話ログから、事業継続を脅かす可能性のある「経営リスク」を抽出し、指定されたJSONフォーマットで出力してください。
        # 出力フォーマット（必ずこのJSON形式に従うこと）
        ```json
        {{
          "risks": [
            {{
              "risk_category": "（リスクの分類）",
              "risk_summary": "（抽出したリスクの概要）",
              "trigger_phrase": "（きっかけとなった経営者の発言）"
            }}
          ]
        }}
        ```
        # 入力：会話ログ
        {conversation_log}
        """)
    response = risk_extraction_model.generate_content(risk_extraction_prompt)
    try:
        json_text = response.text.strip().replace('```json', '').replace('```', '')
        analysis_result = json.loads(json_text)
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"❌ リスク抽出AIの応答解析中にエラー: {e}")
        return {{"risks": []}}

    if analysis_result.get("risks"):
        for risk in analysis_result["risks"]:
            risk_summary = risk.get("risk_summary")
            if risk_summary:
                solution = map_risk_to_solution(risk_summary)
                risk["recommended_solution"] = solution
    return analysis_result

# --- APIの受付窓口の定義 ---
class ConversationRequest(BaseModel):
    conversation_log: str

@app.post("/")
def analyze_endpoint(request: ConversationRequest):
    if not genai.get_key():
        return {{"error": "APIキーが設定されていません。Cloud Runの環境変数を確認してください。"}}

    analysis_result = analyze_conversation_for_risks(request.conversation_log)

    if not analysis_result or not analysis_result.get("risks"):
        return {{"error": "リスクは検出されませんでした。"}}

    return { "raw_analysis": analysis_result }