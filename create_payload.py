# -*- coding: utf-8 -*-
import json

# 正しいPythonの辞書データ
data = {
    "conversation_log": "社長：火事が一番怖いね。\n社長：俺が倒れたらこの店は終わりだよ。"
}

# ファイルを正しい文字コード（UTF-8）で書き出す
file_path = 'payload.json'
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"✅ ファイル '{file_path}' を、正しい形式で作成（上書き）しました。")