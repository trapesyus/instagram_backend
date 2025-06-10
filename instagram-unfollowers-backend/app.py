from flask import Flask, request, jsonify
from flask_cors import CORS
import instaloader

app = Flask(__name__)
CORS(app)

@app.route('/api/unfollowers', methods=['POST'])
def get_unfollowers():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    L = instaloader.Instaloader()
    try:
        L.login(username, password)
    except Exception as e:
        return jsonify({'error': str(e)}), 401

    profile = instaloader.Profile.from_username(L.context, username)
    followers = set(p.username for p in profile.get_followers())
    followees = set(p.username for p in profile.get_followees())

    not_following_back = list(followees - followers)

    return jsonify({'not_following_back': not_following_back})

if __name__ == '__main__':
    app.run(debug=True)
