from spotify_ai import SpotifyAI
from spotify import Spotify
from dotenv import load_dotenv
import os

load_dotenv()

openai_key = os.getenv('OPENAI_API_KEY')
os.environ['OPENAI_API_KEY'] = openai_key


cont = True
sp = Spotify()

print("Welcome to Spotify AI!")
if not sp.check_auth():
    url = sp.get_url_authenticate()
    code = input('Paste the above link into your browser, then paste the redirect url here: ')
    sp.set_code_auth_url(code)

spAI = SpotifyAI(sp, openai_api_key=openai_key)
if spAI.check_devices():
    print("No devices found. Please open a Spotify on one of your devices and try again.")
    exit(1)

cont = True
while cont:
    try:
        request = input("Make a request or write 'exit' to stop the program: ")
        if request == "exit":
            cont = False
        print(spAI.send_command(request))
    except:
     print("Error")
