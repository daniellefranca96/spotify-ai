
# SpotifyAI

SpotifyAI allows interaction with the Spotify API using natural language commands. It utilizes the OpenAI GPT-3 API to interpret user commands and carry out corresponding actions on the Spotify API, such as playing a song, pausing playback, searching for songs, and so on.

## Installation

To install this project, follow the steps below:

1. Clone this repository.
2. Install the dependencies using pip:

```
pip install -r requirements.txt
```

3. Set up the necessary environment variables. Copy the `env.example` file to a new file named `.env` and fill in the following variables:

    - `SPOTIPY_CLIENT_ID`: Your Spotify client ID.
    - `SPOTIPY_CLIENT_SECRET`: Your Spotify client secret.

   These are required for authentication with the Spotify API. You can obtain these values by creating an app on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).

## Usage

To use this project, follow the steps below:

1. Run the `prompt.py` script and follow the instructions to interact with SpotifyAI.
2. You can also start the Flask API by running `api.py` and sending HTTP requests to it.

## Roadmap

Here are some of the planned enhancements for the future of this project:

- Support for voice interaction, allowing users to speak their commands instead of typing them.
- Integration with Gradio to provide an intuitive graphical user interface.
- Publishing an interactive demo on Hugging Face.

## Contribution

Contributions to this project are welcome. Please open an issue to discuss the change you'd like to make or simply fork the project and open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
