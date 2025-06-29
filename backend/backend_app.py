from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

POSTS = [
    {"id": 1, "title": "First Post", "content": "This is the first post."},
    {"id": 2, "title": "Second Post", "content": "This is the second post."},
]

def get_next_id():
    if POSTS:
        return max(post['id'] for post in POSTS) + 1
    else:
        return 1

@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS), 200

@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request must be JSON"}), 400

    title = data.get('title')
    content = data.get('content')

    missing_fields = []
    if not title:
        missing_fields.append('title')
    if not content:
        missing_fields.append('content')

    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    new_post = {
        "id": get_next_id(),
        "title": title,
        "content": content
    }
    POSTS.append(new_post)
    return jsonify(new_post), 201

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = next((post for post in POSTS if post['id'] == post_id), None)
    if not post:
        return jsonify({"error": f"Post with id {post_id} not found"}), 404
    POSTS.remove(post)
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
