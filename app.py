
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# CSVを読み込み
df = pd.read_csv("preflop_range_gto_full.csv")
gto_dict = {}
for _, row in df.iterrows():
    pos = row['position']
    hand = row['hand']
    action = row['action']
    gto_dict.setdefault(pos, {})[hand] = action

@app.route('/gto/preflop', methods=['POST'])
def get_action():
    data = request.get_json()
    hand = data.get("hand")
    position = data.get("position")

    if not hand or not position:
        return jsonify({"error": "hand and position are required"}), 400

    action = gto_dict.get(position, {}).get(hand, "Fold")
    return jsonify({"hand": hand, "position": position, "action": action})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
