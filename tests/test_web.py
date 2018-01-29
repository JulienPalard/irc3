# -*- coding: utf-8 -*-
import asyncio
import pytest
from irc3.plugins import web
from aiohttp.test_utils import make_mocked_request


class Payload:

    def __init__(self, data):
        self.data = data

    @asyncio.coroutine
    def readany(self):
        data = self.data
        self.data = b''
        return data


@pytest.mark.asyncio
def test_web_handler(irc3_bot_factory, raw_test_server, test_client):
    bot = irc3_bot_factory(includes=['irc3.plugins.web'])
    plugin = bot.get_plugin(web.Web)

    plugin.channels['channel'] = '#channel'
    handler = plugin.handler

    req = make_mocked_request('GET', '/')
    resp = yield from handler(req)
    assert resp.status == 200


@pytest.mark.asyncio
def test_web_handler_post(irc3_bot_factory, raw_test_server, test_client):
    bot = irc3_bot_factory(includes=['irc3.plugins.web'])
    plugin = bot.get_plugin(web.Web)
    plugin.server_ready()

    plugin.channels['channel'] = '#channel'
    handler = plugin.handler

    req = make_mocked_request('POST', '/channels/channel',
                              payload=Payload(b'hi'))
    resp = yield from handler(req)
    assert resp.status == 201


@pytest.mark.asyncio
def test_web_handler_404(irc3_bot_factory, raw_test_server, test_client):
    bot = irc3_bot_factory(includes=['irc3.plugins.web'])
    plugin = bot.get_plugin(web.Web)

    plugin.channels['channel'] = '#channel'
    handler = plugin.handler

    req = make_mocked_request('POST', '/channels/notfound')
    resp = yield from handler(req)
    assert resp.status == 404
