from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

BINLIST_URL = "https://lookup.binlist.net/"

def get_card_info(card_number):
    response = requests.get(f"{BINLIST_URL}{card_number}")
    if response.status_code == 200:
        return response.json()
    return None

# Dummy data for card stats
card_stats = {
    "card-xyz": 5,
    "card-jkl": 4,
    "card-bnm": 1
}

@app.route('/api/card-scheme/verify/<card_number>', methods=['GET'])
def verify_card(card_number):
    card_info = get_card_info(card_number)
    if card_info:
        payload = {
            "scheme": card_info.get("scheme"),
            "type": card_info.get("type"),
            "bank": card_info.get("bank", {}).get("name")
        }
        return jsonify(success=True, payload=payload)
    return jsonify(success=False, message="Card not found"), 404

@app.route('/api/card-scheme/stats', methods=['GET'])
def card_stats_endpoint():
    start = request.args.get('start', default=0, type=int)
    limit = request.args.get('limit', default=10, type=int)

    # Slice the card stats based on start and limit
    sliced_stats = dict(list(card_stats.items())[start:start + limit])

    response = {
        "success": True,
        "start": start,
        "limit": limit,
        "size": len(card_stats),
        "payload": sliced_stats
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
