# -*- coding: utf-8 -*-

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

def create_solution_presentation(analysis_result: dict) -> str:
    """AIが提案した解決策を元に、解決策一覧のプレゼンテーションテキストを生成する"""
    presentation_text = "【リスク一覧と解決策（ソリューション）】\n"
    presentation_text += "----------------------------------------\n"

    risks = analysis_result.get("risks", [])
    if not risks:
        return "リスクは検出されませんでした。"

    for risk in risks:
        risk_summary = risk.get('risk_summary', '（内容不明）')
        solution = risk.get('recommended_solution', "個別相談")
        presentation_text += f"✅ {risk_summary}\n"
        presentation_text += f"   └─ 解決策 → 【{solution}】\n\n"
        
    return presentation_text