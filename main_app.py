# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
import google.generativeai as genai

# --- 認証処理 ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("APIキーが.envファイルに設定されていません。")
genai.configure(api_key=api_key)

# --- 部品のインポート ---
from risk_analyzer import analyze_conversation_for_risks
from presentation_generator import create_risk_list_presentation, create_solution_presentation

def get_multiline_input():
    """ユーザーから複数行の入力を受け取る関数"""
    print("会話ログをペーストしてください（最後に'analyze'と入力してEnterを押すと分析を開始します）:")
    lines = []
    while True:
        line = input()
        if line.strip().lower() == 'analyze':
            break
        lines.append(line)
    return "\n".join(lines)

def run_jigyokei_session(conversation_log: str):
    """単一の会話セッションを実行し、分析からプレゼンテーション生成までを行う。"""
    print("\n--- フェーズ1：AIによる会話分析を開始します ---")
    analysis_result = analyze_conversation_for_risks(conversation_log)
    
    if not analysis_result or not analysis_result.get("risks"):
        print("分析の結果、リスクは検出されませんでした。セッションを終了します。")
        return
        
    print("--- 分析完了。フェーズ2：プレゼンテーションを生成します ---\n")
    
    risk_presentation = create_risk_list_presentation(analysis_result)
    print(risk_presentation)

    print("\n----------------------------------------\n")
    solution_presentation = create_solution_presentation(analysis_result)
    print(solution_presentation)

# --- プログラムの実行部分 ---
if __name__ == "__main__":
    conversation_log_input = get_multiline_input()
    if conversation_log_input:
        run_jigyokei_session(conversation_log_input)
    else:
        print("会話ログが入力されませんでした。")