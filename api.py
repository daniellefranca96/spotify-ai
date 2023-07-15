from flask import Flask, request, session
from flask_session import Session
from dotenv import load_dotenv
from spotify import Spotify
import jsonify
from spotify_ai import SpotifyAI
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure the session to use filesystem (you can also use Redis, Memcached, SQLAlchemy, etc.)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    code = data.get('code', '')
    openai_api_key = data.get('openai_api_key', os.getenv('OPENAI_API_KEY', ''))
    if not openai_api_key:
        return jsonify({'error': 'openai_api_key not provided'}), 400
    if not code:
        return jsonify({'error': 'code not provided'}), 400

    session['openai_api_key'] = openai_api_key
    session['openai_model'] = os.getenv('OPENAI_API_KEY', 'gpt-3.5-turbo-0613')
    session['language'] = os.getenv('LANGUAGE', 'en')
    session['spotify_code'] = code

    return jsonify({'message': 'Logged in successfully'}), 200

@app.route('/send_command', methods=['POST'])
def send_command():
    data = request.get_json(force=True)
    command = data.get('command', '')

    if not command:
        return jsonify({'error': 'command not provided'}), 400

    try:
        # Recreate the Spotify and SpotifyAI instances for this user using the session data
        spotify = getSpotify()
        spotify_ai = SpotifyAI(sp=spotify, language=session['language'], openai_model=session['openai_model'], openai_api_key=session['openai_api_key'])

        result = spotify_ai.send_command(command)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def getSpotify():
    spotify = Spotify()
    spotify.set_code_auth_url(session['spotify_code'])
    return spotify


@app.route('/check_devices', methods=['GET'])
def check_devices():
    try:
        spotify = getSpotify()
        spotify_ai = SpotifyAI(sp=spotify, language=session['language'], openai_model=session['openai_model'], openai_api_key=session['openai_api_key'])

        result = spotify_ai.check_devices()
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_url_auth', methods=['GET'])
def get_url_auth():
    try:
        spotify = Spotify()
        result = spotify.get_url_authenticate()
        return jsonify({'url': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
