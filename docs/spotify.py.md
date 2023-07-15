
# spotify.py

Este arquivo contém a classe `Spotify`, que encapsula a interação com a API do Spotify.

## Métodos da Classe Spotify

- `__init__`: Este é o construtor da classe. Ele inicializa a autenticação com a API do Spotify e define as permissões necessárias.
- `call_method`: Retorna um dicionário de todos os métodos disponíveis da classe Spotify com suas descrições e parâmetros.
- `devices`: Retorna uma lista de todos os dispositivos do usuário atualmente disponíveis.
- `get_album`: Retorna informações sobre um álbum específico dado o ID do álbum.
- `current_playback`: Retorna informações sobre a reprodução atual.
- `start_playback`: Inicia a reprodução de uma faixa, episódio, álbum ou playlist.
- `pause`: Pausa a reprodução atual.
- `repeat`: Alterna o estado de repetição.
- `shuffle`: Alterna o estado de aleatório.
- `add_to_queue`: Adiciona uma faixa à fila de reprodução.
- `get_playlists`: Retorna uma lista de todas as playlists do usuário.
- `get_playlist`: Retorna uma lista de faixas de uma playlist específica.
- `get_artist`: Retorna informações sobre um artista específico dado o ID do artista.
- `get_podcasts`: Retorna uma lista de todos os podcasts do usuário.
- `extract_info_one`: Extrai informações específicas de um objeto de dados.
- `extract_info`: Chama `extract_info_one` para uma lista de objetos de dados.
- `search`: Pesquisa por faixas, artistas, álbuns, podcasts, episódios, etc. no Spotify.
- `queue`: Retorna a fila de reprodução atual.
- `current_user_recently_played`: Retorna uma lista de faixas reproduzidas recentemente pelo usuário.
- `next_track`: Pula para a próxima faixa na fila de reprodução.
- `previous_track`: Volta para a faixa anterior na fila de reprodução.
- `set_code_auth_url`: Define o código de autorização da URL.
- `get_url_authenticate`: Retorna a URL de autenticação.
- `check_auth`: Verifica se o token de autenticação está armazenado em cache e se ainda é válido.
