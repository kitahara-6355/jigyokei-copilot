# -*- coding: utf-8 -*-
import json
from risk_analyzer import analyze_conversation_for_risks # 作成済みの思考エンジンをインポート

# --- ▼▼▼ サンプルデータ（ステップ2で作成したもの）▼▼▼ ---
# risk_analyzerがこのデータを返すことを想定しています
sample_analysis_result = {
  "risks": [
    {
      "risk_category": "ヒト",
      "risk_summary": "経営者の傷病による長期休業・廃業リスク",
      "trigger_phrase": "俺が倒れたら、この店は終わりだよ"
    },
    {
      "risk_category": "モノ",
      "risk_summary": "厨房からの火災による店舗・設備の焼失リスク",
      "trigger_phrase": "火事が一番怖いね"
    },
    {
      "risk_category": "賠償責任",
      "risk_summary": "食中毒の発生による営業停止と損害賠償リスク",
      "trigger_phrase": "食中毒かな"
    }
  ]
}

risk_solution_map = {
    "経営者の傷病による長期休業・廃業リスク": "商工会の福祉共済, 経営者休業補償制度",
    "厨房からの火災による店舗・設備の焼失リスク": "火災共済（店舗・設備補償）",
    "食中毒の発生による営業停止と損害賠償リスク": "ビジネス総合保険（PL責任補償）"
}
# --- ▲▲▲ サンプルデータ ▲▲▲ ---


def create_risk_list_presentation(analysis_result: dict) -> str:
    """リスク分析結果（JSON）から、リスク一覧のプレゼンテーションテキストを生成する"""
    presentation_text = "【事業継続を脅かすリスク一覧】\n"
    presentation_text += "----------------------------------------\n"

    risks = analysis_result.get("risks", [])
    if not risks:
        return "リスクは検出されませんでした。"

    for i, risk in enumerate(risks):
        presentation_text += f"{i+1}. {risk.get('risk_summary', '（内容不明）')}\n"
        presentation_text += f"   (社長の発言：'{risk.get('trigger_phrase', 'N/A')}')\n\n"

    return presentation_text

def create_solution_presentation(analysis_result: dict, solution_map: dict) -> str:
    """リスク分析結果と解決策マップから、解決策一覧のプレゼンテーションテキストを生成する"""
    presentation_text = "【リスク一覧と解決策（ソリューション）】\n"
    presentation_text += "----------------------------------------\n"

    risks = analysis_result.get("risks", [])
    if not risks:
        return "リスクは検出されませんでした。"

    for risk in risks:
        risk_summary = risk.get('risk_summary', '（内容不明）')
        solution = solution_map.get(risk_summary, "個別相談")
        presentation_text += f"✅ {risk_summary}\n"
        presentation_text += f"   └─ 解決策 → 【{solution}】\n\n"

    return presentation_text

# --- ここからがプログラムの実行部分 ---
if __name__ == "__main__":

    # 本来はここで実際の会話ログを使って思考エンジンを呼び出すが、
    # 今回はテスト用にサンプルデータを使います。
    # analysis_result = analyze_conversation_for_risks(実際の会話ログ)
    analysis_result = sample_analysis_result

    # --- ステップ1：リスク一覧の表示 ---
    print("--- クライマックス・プレゼンテーション：ステップ1（リスクの提示）---\n")
    risk_presentation = create_risk_list_presentation(analysis_result)
    print(risk_presentation)

    # --- ステップ2：解決策の表示 ---
    print("\n--- クライマックス・プレゼンテーション：ステップ2（解決策の提示）---\n")
    solution_presentation = create_solution_presentation(analysis_result, risk_solution_map)
    print(solution_presentation)