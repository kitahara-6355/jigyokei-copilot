# -*- coding: utf-8 -*-
import google.generativeai as genai
import json
import textwrap

def map_risk_to_solution(risk_summary: str) -> str:
    """単一のリスク概要文を受け取り、最適な解決策を返すことに特化したAI。"""
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
    """【ステップ1】リスク抽出AI、【ステップ2】解決策マッピングAIを順に実行する。"""
    # --- ステップ1：リスク抽出AIの実行 ---
    risk_extraction_model = genai.GenerativeModel('gemini-1.5-flash-latest')
    risk_extraction_prompt = textwrap.dedent(f"""
        あなたは聞き上手なリスクコンサルタントです。
        以下の会話ログから、事業継続を脅かす可能性のある「経営リスク」を抽出し、指定されたJSONフォーマットで出力してください。
        解決策の提案は不要です。リスクの客観的な抽出に集中してください。

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

    # --- ステップ2：抽出した各リスクに解決策をマッピング ---
    if analysis_result.get("risks"):
        for risk in analysis_result["risks"]:
            risk_summary = risk.get("risk_summary")
            if risk_summary:
                solution = map_risk_to_solution(risk_summary)
                risk["recommended_solution"] = solution
    return analysis_result