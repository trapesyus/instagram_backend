from flask import Flask, request, jsonify
from instagrapi import Client
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Başka domainlerden istek kabul etmek için

@app.route('/api/not_following_back', methods=['POST'])
def not_following_back():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    cl = Client()

    try:
        cl.login(username, password)
        user_id = cl.user_id_from_username(username)
        followers = cl.user_followers(user_id)
        following = cl.user_following(user_id)

        not_following = [
            following[uid].username for uid in following if uid not in followers
        ]

        return jsonify({"not_following_back": not_following})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
