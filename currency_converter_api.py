import asyncio
from aiohttp import web
import json
import os

from services.exchange_rate_repository import ExchangeRateRepository


routes = web.RouteTableDef()
repo = ExchangeRateRepository(host="redis", port=6379)
loop = asyncio.get_event_loop()


@routes.get('/convert')
async def handle_converion(request: web.Request):
    resp = web.Response(status=400)
    resp.content_type = "application/json"
    resp.text = json.dumps({'status': 'failed'})

    params = ["from", "to", "amount"]
    all_params_present = all(param in request.query for param in params)
    if not all_params_present:
        return web.Response(
            status=400,
            content_type='application/json',
            text=json.dumps({
                'status': 'failed',
                'message': 'not all parameters specified'})
        )

    qfrom = request.query['from']
    qto = request.query['to']
    qamount = num(request.query['amount'])

    if qamount is None:
        return web.Response(
            status=400,
            content_type='application/json',
            text=json.dumps({
                'status': 'failed',
                'message': 'parameter "amount" must be 0 or 1'})
        )

    factor = repo.get_rates(qfrom, qto)
    if factor is None:
        return web.Response(
            status=404,
            content_type='application/json',
            text=json.dumps({
                'status': 'failed',
                'message': 'unknown currency names'})
        )

    resp = web.Response(status=200)
    resp_obj = {
        'status': 'success',
        'amount': qamount * factor
    }
    resp.text = json.dumps(resp_obj)
    return resp


@routes.post('/database')
async def handle_converion(request: web.Request):
    if 'merge' not in request.query or num(request.query['merge'] is None):
        return web.Response(
            status=400,
            text=json.dumps({
                'status': 'failed',
                'message': 'parameter "merge" is not present'}
            )
        )

    merge = int(request.query['merge'])
    body = await request.content.read()
    new_rates = {}
    try:
        new_rates = json.loads(body)
    except Exception:
        return web.Response(
            status=400,
            text=json.dumps({
                'status': 'failed',
                'message': 'data must be in json format'}
            )
        )

    repo.merge_rates(new_rates, merge)
    return web.Response(
        status=200,
        text=json.dumps({
            'status': 'success',
            'message': 'successfuly updated'}
        )
    )


def num(s):
    res = try_parse_int(s)
    if res:
        return res
    try:
        return float(s)
    except ValueError:
        return None


def try_parse_int(s):
    try:
        return int(s)
    except ValueError:
        return None


def main():
    port = int(os.environ['APP_PORT'])
    app = web.Application(loop=loop)
    app.add_routes(routes)
    web.run_app(app, port=port)


if __name__ == "__main__":
    main()
