import json
import os
import inspect
import logging

import openai

from spotify import Spotify


logging.basicConfig(level=logging.INFO)


class OpenAIWrapper:
    """Encapsulates the OpenAI API, reducing key exposure and isolating the API interactions."""

    def __init__(self, api_key=None, model=None):
        if api_key is None:
            raise ValueError("OPENAI_API_KEY is not set")
        self.api_key = api_key
        self.model = model if model else 'gpt-3.5-turbo-0613'
        openai.api_key = self.api_key

    def chat_completion(self, messages_r: list, functions: list):
        return openai.ChatCompletion.create(
            model=self.model,
            messages=messages_r,
            functions=functions)


class SpotifyAI:
    openai_api_key: str
    openai_model: str
    language: str

    def __init__(self, sp: Spotify = None, language=None, openai_model=None, openai_api_key=None):
        self.sp = sp
        self.language = language if language else 'en'
        self.ai = OpenAIWrapper(api_key=openai_api_key, model=openai_model)

        if self.sp is None:
            logging.warning("Spotify client is not set")
            self.sp = Spotify()

        self.functions = self.extract_functions()

    def extract_functions(self):
        functions = []
        library_f = self.sp.call_method()
        for func in library_f.keys():
            description = library_f[func].get('description')
            parameters = library_f[func].get('parameters')
            functions.append(self.create_openai_function(func, description, parameters))
        return functions

    @staticmethod
    def create_openai_function(name: str, description: str, arguments: dict):
        return {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": arguments if arguments else {
                    'action:': {'type': 'string', 'description': 'action to perform'}},
                "required": list(arguments.keys()) if arguments else ['action']
            }
        }

    def check_devices(self):
        devices = self.sp.devices()
        return len(devices['devices']) == 0 or True not in [d['is_active'] for d in devices['devices']]

    def process_response(self, response: dict, messages: list):
        response_choice = response['choices'][0]

        logging.info("Response: %s", response_choice)

        if '"finish_reason"' in json.dumps(response) and '"stop"' in json.dumps(response):
            return response_choice['message']['content']

        function_call = response_choice['message']['function_call']
        function_name = function_call['name']
        function_args = function_call['arguments']

        if "action" in function_args:
            function_args = {}
        else:

            function_args = json.loads(function_args)

        logging.info("Call function: %s", function_args)

        if function_name not in self.sp.call_method():
            logging.error("Function %s not in Spotify client", function_name)
            raise ValueError(f"Function {function_name} not in Spotify client")

        function = self.sp.call_method()[function_name].get('method')
        if function is None:
            logging.error("Method %s not found in Spotify client", function_name)
            raise ValueError(f"Method {function_name} not found in Spotify client")

        returned = function(**function_args)

        logging.info("Return function: %s", returned)

        messages.append(response_choice['message'])
        messages.append({'role': 'function', 'content': str(returned), 'name': function_name})

        return self.process_response(self.ai.chat_completion(messages, self.functions), messages)

    def get_template(self):
        return "As Spotify Assistant, interpret user's natural language commands. You are very rule abiding and always follow the below rules always when applicable:" \
               "- If an ID request refers to Spotify ID. Search if unsure. Recognize songs from lyrics before function calls. " \
               "- Prioritize episode search with podcast name. " \
               "- Respond in user's language: {self.language}. " \
               "- Only request functions provided to you don't call names not in the list. " \
               "- You can use to parameter offset to ask for more results in a method, for example, if then limit of the method is 5 per request offset 0 brings 0-5 results, offset 5 brings 6-10 results and so on. " \
               "- When the user asks to play a song in a specific playlist, query the playlist using offset until you find the song, do not play the playlist uri. " \
               "- When the user asks 'next' or 'previous' he means he wants to go to next item or previous item in the queue, this is also valid for translations of this words. " \
               "- When the user asks to play a song/episode and more of one result appear on the search always play the first one. " \
               "- Think step by step and reflect if the answer is the best for fulfilling user request"

    def assemble_messages(self, inuser: str):
        template = self.get_template()
        return [
            {'role': 'system', 'content': template},
            {'role': 'user', 'content': 'User:' + inuser}
        ]

    def send_command(self, inuser: str):
        messages = self.assemble_messages(inuser)
        return self.process_response(self.ai.chat_completion(messages, self.functions), messages)
