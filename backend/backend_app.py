import json
import os
from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)  # enable CORS for all routes

# ---------- Swagger ----------
SWAGGER_URL = "/api/docs"
API_URL = "/static/masterblog.json"
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Masterblog API"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# ---------- JSON storage ----------
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "posts.json")
DATE_FORMAT = "%Y-%m-%d"
DEFAULT_POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post.",
     "author": "Admin", "date": "2023-06-07"},
    {"id": 2, "title": "Second post", "content": "This is the second post.",
     "author": "Admin", "date": "2023-06-08"},
]


def load_posts():
    """Read posts from the JSON file. Create it if missing or broken."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list) and data:
            return data
        if isinstance(data, list):
            return data
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        print("Warning: posts.json is not valid JSON. Resetting it.")
    save_posts(DEFAULT_POSTS)
    return list(DEFAULT_POSTS)


def save_posts(posts):
    """Write posts to the JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
    except OSError as err:
        print(f"Error saving posts: {err}")


def find_post(posts, post_id):
    for post in posts:
        if post["id"] == post_id:
            return post
    return None


def generate_id(posts):
    return max((p["id"] for p in posts), default=0) + 1


def valid_date(text):
    try:
        datetime.strptime(text, DATE_FORMAT)
        return True
    except (ValueError, TypeError):
        return False


# ---------- Endpoints ----------
@app.route("/api/posts", methods=["GET"])
def get_posts():
    posts = load_posts()
    sort_field = request.args.get("sort")
    direction = request.args.get("direction", "asc")

    if sort_field is None and "direction" not in request.args:
        return jsonify(posts), 200

    valid_fields = ["title", "content", "author", "date"]
    if sort_field is not None and sort_field not in valid_fields:
        return jsonify({"error": f"Invalid sort field '{sort_field}'. "
                                 f"Use one of: {', '.join(valid_fields)}."}), 400
    if direction not in ("asc", "desc"):
        return jsonify({"error": f"Invalid direction '{direction}'. "
                                 "Use 'asc' or 'desc'."}), 400
    if sort_field is None:
        return jsonify({"error": "Parameter 'direction' needs 'sort'."}), 400

    if sort_field == "date":
        def key(p):
            return datetime.strptime(p.get("date", "1900-01-01"), DATE_FORMAT)
    else:
        def key(p):
            return str(p.get(sort_field, "")).lower()

    posts = sorted(posts, key=key, reverse=(direction == "desc"))
    return jsonify(posts), 200


@app.route("/api/posts", methods=["POST"])
def add_post():
    data = request.get_json(silent=True) or {}
    missing = [f for f in ("title", "content") if not data.get(f)]
    if missing:
        return jsonify({"error": "Missing required field(s)",
                        "missing": missing}), 400

    date = data.get("date") or datetime.now().strftime(DATE_FORMAT)
    if not valid_date(date):
        return jsonify({"error": "Date must be in format YYYY-MM-DD"}), 400

    posts = load_posts()
    new_post = {
        "id": generate_id(posts),
        "title": data["title"],
        "content": data["content"],
        "author": data.get("author") or "Anonymous",
        "date": date,
    }
    posts.append(new_post)
    save_posts(posts)
    return jsonify(new_post), 201


@app.route("/api/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    posts = load_posts()
    post = find_post(posts, post_id)
    if post is None:
        return jsonify({"error": f"Post with id {post_id} was not found."}), 404
    posts.remove(post)
    save_posts(posts)
    return jsonify({"message":
                    f"Post with id {post_id} has been deleted successfully."}), 200


@app.route("/api/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    posts = load_posts()
    post = find_post(posts, post_id)
    if post is None:
        return jsonify({"error": f"Post with id {post_id} was not found."}), 404

    data = request.get_json(silent=True) or {}
    if "date" in data and not valid_date(data["date"]):
        return jsonify({"error": "Date must be in format YYYY-MM-DD"}), 400

    for field in ("title", "content", "author", "date"):
        if field in data and data[field]:
            post[field] = data[field]

    save_posts(posts)
    return jsonify(post), 200


@app.route("/api/posts/search", methods=["GET"])
def search_posts():
    posts = load_posts()
    terms = {f: request.args.get(f, "").lower()
             for f in ("title", "content", "author", "date")
             if request.args.get(f)}
    if not terms:
        return jsonify([]), 200

    results = [
        p for p in posts
        if any(term in str(p.get(field, "")).lower()
               for field, term in terms.items())
    ]
    return jsonify(results), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)