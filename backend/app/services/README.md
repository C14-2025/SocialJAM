# Uso da API do Spotify (HTTPS obrigatório)

Esta documentação explica como configurar o projeto para usar a API do Spotify localmente. O Spotify exige que a Redirect URI seja HTTPS; a forma recomendada em desenvolvimento é usar o ngrok para expor um túnel HTTPS para o seu servidor local.

Links úteis
- Spotify Developer Dashboard: https://developer.spotify.com/dashboard/
- ngrok: https://ngrok.com

Requisitos
- Python e dependências do projeto já instaladas (uso do `pyproject.toml`).
- Conta no Spotify Developer e criação de uma app (para obter `Client ID` e `Client Secret`).
- Conta no ngrok (gratuita serve para desenvolvimento) — será necessário um auth token.

Passo a passo

1) Instale o ngrok
- No Windows: instale via **Windows Store** procurando por "ngrok" ou baixe do site do ngrok.
- No Linux: use seu package manager (snap, apt, etc.) ou baixe do site.

Observação: se preferir, siga as instruções oficiais: https://ngrok.com/docs

2) Configure o ngrok com seu auth token
- Crie uma conta no site do ngrok.
- No dashboard do ngrok, vá para "Setup & Installation" e copie o seu `authtoken`.
- No terminal, execute (substitua pelo seu token):

```powershell
ngrok config add-authtoken {seu_token_aqui}
```

3) Configure o `.env`
Dentro da pasta `backend` crie/edite o arquivo `.env` com exatamente estas chaves (sem espaços extras):

```
SPOTIFY_CLIENT_ID=seu_client_id
SPOTIFY_CLIENT_SECRET=seu_client_secret
SPOTIFY_REDIRECT_URI=https://<seu_endereco_ngrok>/spotify/callback
```

- `SPOTIFY_CLIENT_ID` e `SPOTIFY_CLIENT_SECRET` você obtém ao criar uma app no Spotify Developer Dashboard: https://developer.spotify.com/dashboard/
- `SPOTIFY_REDIRECT_URI` será preenchida com a URL pública gerada pelo ngrok (veja passo 5).

4) Crie/registre a app no Spotify
- Acesse o Dashboard: https://developer.spotify.com/dashboard/
- Crie uma nova aplicação (ou use uma existente) e copie o Client ID/Client Secret para o `.env`.
- Em "Edit Settings" adicione a Redirect URI exatamente como estará no `.env` (veja o formato no passo 5).

5) Rode o ngrok
No diretório local (ou de qualquer lugar), execute:

```powershell
ngrok http 8000
```

- O ngrok abrirá uma sessão e mostrará linhas com "Forwarding".
- Copie o endereço HTTPS mostrado em "Forwarding" (ex: `https://abc123def4f0.ngrok.io`).

6) Atualize o `.env` com a Redirect URI correta
- No `.env`, coloque:

```
SPOTIFY_REDIRECT_URI=https://abc123def4f0.ngrok.io/spotify/callback
```

Observação importante: a URI deve terminar em `/spotify/callback` porque a rota implementada na API é `/spotify/callback`.

7) Atualize a Redirect URI na sua app do Spotify
- No Spotify Dashboard -> Edit Settings -> Redirect URIs, adicione a mesma URI que você colocou no `.env`.

8) Rode o servidor e acesse pela URL do ngrok
- Inicie o servidor como de costume (no diretório `backend`):

```powershell
uv run python main.py
```

- Agora acesse a aplicação pelo endereço HTTPS do ngrok (ex: `https://abc123def4f0.ngrok.io`) — NÃO use `http://localhost:8000` para o fluxo do Spotify.

Fluxo de autenticação com Spotify (resumido)
1. Frontend pede a URL de login (`GET /spotify/login`) — o backend retorna a URL do Spotify para redirecionamento.
2. Usuário se autentica no Spotify.
3. Spotify redireciona o navegador para: `https://abc123def4f0.ngrok.io/spotify/callback?code=...`.
4. O backend troca o `code` por um `access_token` e o frontend pode usá-lo para chamadas autorizadas (por exemplo `GET /spotify/top-artists?access_token=...`).

Notas e dicas
- A URL do ngrok muda a cada execução (a não ser que você use domínios reservados do ngrok). Sempre atualize o `.env` e o Redirect URI no Spotify Dashboard quando iniciar uma nova sessão do ngrok.
- Se receber aviso no browser sobre certificado não confiável, isso não acontece com ngrok — ngrok fornece um certificado válido. O aviso aparece apenas quando você usa certificados autoassinados.
- Para desenvolvimento alternativo (sem ngrok) é possível gerar certificados e rodar o uvicorn com `ssl_keyfile` e `ssl_certfile`, mas o Spotify frequentemente rejeita certificados autoassinados. Por isso o ngrok é a opção mais prática.

Exemplo de `.env` final (apenas exemplo — não compartilhe seu client secret):

```
SPOTIFY_CLIENT_ID=abcd1234efgh5678
SPOTIFY_CLIENT_SECRET=verysecretvalue
SPOTIFY_REDIRECT_URI=https://abc123def4f0.ngrok.io/spotify/callback
```

Links finais
- Spotify Developer Dashboard: https://developer.spotify.com/dashboard/
- ngrok: https://ngrok.com