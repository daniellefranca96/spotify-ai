
# spotify_ai.py

Este arquivo contém a classe `SpotifyAI`, que é usada para processar comandos do usuário e interagir com a API do Spotify.

## Métodos da Classe SpotifyAI

- `__init__`: Este é o construtor da classe. Ele inicializa o cliente Spotify e o wrapper OpenAI.
- `extract_functions`: Extrai todas as funções disponíveis da classe Spotify.
- `create_openai_function`: Cria uma função OpenAI a partir do nome, descrição e argumentos da função.
- `check_devices`: Verifica se existem dispositivos disponíveis e ativos.
- `process_response`: Processa a resposta da API OpenAI e realiza a ação correspondente.
- `get_template`: Retorna o modelo de assistente Spotify para a API OpenAI.
- `assemble_messages`: Monta as mensagens para serem enviadas para a API OpenAI.
- `send_command`: Envia um comando do usuário para a API OpenAI e processa a resposta.
