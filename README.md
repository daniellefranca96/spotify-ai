
# Descrição do Projeto

Este projeto, chamado Spotify AI, permite a interação com a API do Spotify usando comandos de linguagem natural. Ele utiliza a API OpenAI GPT-3 para interpretar comandos do usuário e realizar ações correspondentes na API do Spotify, como reproduzir uma música, pausar a reprodução, pesquisar por músicas e assim por diante.

## Instalação

Para instalar este projeto, siga os seguintes passos:

1. Clone este repositório.
2. Instale as dependências usando pip:

```
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente necessárias. Copie o arquivo `env.example` para um novo arquivo chamado `.env` e preencha as seguintes variáveis:

    - `SPOTIPY_CLIENT_ID`: Sua ID de cliente Spotify.
    - `SPOTIPY_CLIENT_SECRET`: Seu segredo de cliente Spotify.

   Estes são necessários para a autenticação com a API do Spotify. Você pode obter esses valores criando um aplicativo no [Dashboard de Desenvolvedores do Spotify](https://developer.spotify.com/dashboard/applications).

## Uso

Para usar este projeto, siga os seguintes passos:

1. Execute o script `prompt.py` e siga as instruções para interagir com o Spotify AI.
2. Você também pode iniciar a API Flask executando `api.py` e enviar solicitações HTTP para ela.

## Roadmap

Aqui estão algumas das melhorias planejadas para o futuro deste projeto:

- Suporte para interação por voz, permitindo que os usuários falem seus comandos em vez de digitá-los.
- Integração com o Gradio para fornecer uma interface de usuário gráfica intuitiva.
- Publicação de uma demonstração interativa no Hugging Face.

## Contribuição

Contribuições para este projeto são bem-vindas. Por favor, abra um problema para discutir a mudança que você gostaria de fazer ou simplesmente faça um fork do projeto e abra uma solicitação pull.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.
