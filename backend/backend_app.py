from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def generate_id():
    if not POSTS:
        return 1
    return max(post.get("id", 0) for post in POSTS) + 1


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'POST':
        try:
            raw_data = request.data.decode('utf-8')
            data = json.loads(raw_data)
        except Exception as e:
            return jsonify({
                "error": "Invalid JSON",
                "status": 415
            }), 415

        title = request.json.get('title')
        content = request.json.get('content')

        missing_fields = []
        if not title:
            missing_fields.append('title')
        if not content:
            missing_fields.append('content')

        if missing_fields:
            return jsonify({
                "error": f"The following field(s) are required: {', '.join(missing_fields)}",
                "status": 400
            }), 400

        POSTS.append({
            "id": generate_id(),
            "title": title,
            "content": content
        })

    return jsonify(POSTS), 201

@app.route('/api/posts/<id>', methods=['DELETE'])
def delete_post(id):
    try:
        post_id = int(id)
    except ValueError:
        return jsonify({
            "error": "Invalid ID format",
        }), 400

    for post in POSTS:
        if post["id"] == post_id:
            POSTS.remove(post)
            return jsonify({
                "message": f"Post with id {post_id} has been deleted successfully."
            }), 200

    return jsonify({
        "error": f"No post with id {post_id} exists.",
        "status": 404
    }), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
