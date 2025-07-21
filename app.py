from flask import Flask, request, jsonify, abort
from datetime import datetime

app = Flask(__name__)

ads = {}
next_id = 1


def make_ad_json(ad_id, data):
    return {
        "id": ad_id,
        "title": data["title"],
        "description": data.get("description", ""),
        "created_at": data["created_at"].isoformat() + "Z",
        "owner": data["owner"],
    }


@app.route("/ads", methods=["POST"])
def create_ad():
    payload = request.get_json(silent=True) or {}
    title = payload.get("title")
    owner = payload.get("owner")
    if not title or not owner:
        return jsonify({"error": "fields 'title' and 'owner' are required"}), 400

    global next_id
    ad_id = next_id
    next_id += 1

    ads[ad_id] = {
        "title": title.strip(),
        "description": str(payload.get("description", "")).strip(),
        "created_at": datetime.utcnow(),
        "owner": owner.strip(),
    }
    return jsonify(make_ad_json(ad_id, ads[ad_id])), 201


@app.route("/ads/<int:ad_id>", methods=["GET"])
def get_ad(ad_id):
    ad = ads.get(ad_id)
    if ad is None:
        abort(404)
    return jsonify(make_ad_json(ad_id, ad))


@app.route("/ads/<int:ad_id>", methods=["DELETE"])
def delete_ad(ad_id):
    if ads.pop(ad_id, None) is None:
        abort(404)
    return "", 204


if __name__ == "__main__":
    app.run()

