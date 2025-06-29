from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First Post", "content": "This is the first post."},
    {"id": 2, "title": "Second Post", "content": "This is the second post."},
]

# Auto-Increment ID Helper
def get_next_id():
    if POSTS:
        return max(post["id"] for post in POSTS) + 1
    return 1

# GET /api/posts
@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS), 200

# POST /api/posts
@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({"error": "Missing title or content"}), 400

    new_post = {
        "id": get_next_id(),
        "title": title,
        "content": content
    }
    POSTS.append(new_post)
    return jsonify(new_post), 201

# DELETE /api/posts/<id>
@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    for post in POSTS:
        if post["id"] == post_id:
            POSTS.remove(post)
            return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200

    return jsonify({"error": f"Post with id {post_id} not found."}), 404

# PUT /api/posts/<id>
@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    for post in POSTS:
        if post["id"] == post_id:
            post["title"] = data.get("title", post["title"])
            post["content"] = data.get("content", post["content"])
            return jsonify(post), 200

    return jsonify({"error": f"Post with id {post_id} not found."}), 404

# GET /api/posts/search?title=...&content=...
@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    filtered_posts = []
    for post in POSTS:
        title_match = title_query in post['title'].lower() if title_query else True
        content_match = content_query in post['content'].lower() if content_query else True
        if title_match and content_match:
            filtered_posts.append(post)

    return jsonify(filtered_posts), 200

# Run App
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
