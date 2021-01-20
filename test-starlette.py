import uvicorn
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.requests import Request

from starlette_discord.client import DiscordOAuthClient
from auth import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI


app = Starlette()
client = DiscordOAuthClient(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scopes=('identify', 'guilds'))


@app.route('/login')
async def login_with_discord(_):
    return client.redirect()


@app.route('/callback')
async def callback(request: Request):
    code = request.query_params['code']
    async with client.session(code) as session:
        u = await session.identify()
    return JSONResponse(u)



uvicorn.run(app, host='0.0.0.0', port=9000)
