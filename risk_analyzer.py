# -*- coding: utf-8 -*-
import google.generativeai as genai
import json
import textwrap
import os  # osライブラリをインポート
from dotenv import load_dotenv  # dotenvライブラリをインポート

# --- ▼▼▼ 認証部分を全面的に修正 ▼▼▼ ---
# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からAPIキーを取得して設定
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("APIキーが.envファイルに設定されていません。")
genai.configure(api_key=api_key)
# --- ▲▲▲ 認証部分を全面的に修正 ▲▲▲ ---


def analyze_conversation_for_risks(conversation_log: str) -> dict:
    # ...（これ以降の関数の内容は変更なし）
    """
    会話ログを分析し、経営リスクをJSON形式で抽出する思考エンジン。

    Args:
        conversation_log: 分析対象の会話ログテキスト。

    Returns:
        抽出されたリスク情報を含む辞書（JSONオブジェクト）。
    """
    
    # Gemini AIモデルを初期化
    model = genai.GenerativeModel('gemini-pro')

    # AIへの指示書（プロンプト）。f-string方式に変更し、JSONの{}を{{}}にエスケープ
    prompt = textwrap.dedent(f"""
        あなたは商工会に所属する、経験豊富な中小企業向けのリスクコンサルタントです。
        以下の制約条件と出力フォーマットに従って、入力された会話ログから事業継続を脅かす可能性のある「経営リスク」を抽出してください。

        # 制約条件
        - 会話の中から、ヒト・モノ・カネ・情報・賠償責任など、経営に関するリスクのみを抽出する。
        - 抽出したリスクは、簡潔な一行で表現する。
        - 経営者の発言（トリガーフレーズ）を特定し、併記する。
        - 会話ログにないリスクは絶対に捏造しないこと。

        # 出力フォーマット（必ずこのJSON形式に従うこと）
        ```json
        {{
          "risks": [
            {{
              "risk_category": "（例：モノ）",
              "risk_summary": "（例：厨房の火災による店舗・設備の焼失リスク）",
              "trigger_phrase": "（例：火事が一番怖いね）"
            }}
          ]
        }}
        ```

        # 入力：会話ログ
        {conversation_log}
        """)
    
    # AIに、組み立てた指示書（f-stringで完成済み）を渡して分析を依頼
    response = model.generate_content(prompt)
    
    try:
        # AIの返答からJSON部分のみを抽出
        json_text = response.text.strip().replace('```json', '').replace('```', '')
        # JSON文字列をPythonの辞書オブジェクトに変換
        extracted_risks = json.loads(json_text)
        return extracted_risks
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"❌ AIの応答からJSONを解析中にエラーが発生しました: {e}")
        print(f"AIの生テキスト応答: {response.text}")
        return {{"risks": []}}


# --- ここからがプログラムの実行部分 ---
if __name__ == "__main__":

    # サンプルとなる会話ログ（〇〇キッチン編）
    conversation_log = """
    職員：社長、お店の心配事を色々お聞きしましたが、社長ご自身のことについてはいかがでしょう？もし、社長が病気やケガで1ヶ月お店に立てなくなったら…？
    社長：考えたくないけど、俺が倒れたら、この店は終わりだよ。レシピも仕入れも、全部俺の頭の中にあるからな…。
    職員：なるほど、社長への依存度が非常に高い状態なのですね。
    社長：あと、怖いのは設備だけじゃない。うちは火を使う商'便だから、やっぱり火事が一番怖いね。
    職員：火災は飲食店にとって最大のリスクの一つですね。
    社長：それと、食中毒かな。万が一うちの店から出してしまったら、もう信用はガタ落ちで、店を続けられないかもしれない。
    """

    print("--- 会話ログの分析を開始します ---")

    # 思考エンジンを呼び出し
    analysis_result = analyze_conversation_for_risks(conversation_log)

    print("\n--- ✅ AIによるリスク分析結果（JSON形式） ---")
    # 結果をきれいに整形して表示
    print(json.dumps(analysis_result, indent=2, ensure_ascii=False))

    print("\n--- リスク一覧 ---")
    if analysis_result and analysis_result.get("risks"):
        for i, risk in enumerate(analysis_result["risks"]):
            print(f"{i+1}. カテゴリ：{risk.get('risk_category')}")
            print(f"   リスク内容：{risk.get('risk_summary')}")
            print(f"   発言トリガー：'{risk.get('trigger_phrase')}'\n")
    else:
        print("リスクは検出されませんでした。")