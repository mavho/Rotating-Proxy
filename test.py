import unittest 
from unittest.mock import patch,MagicMock,PropertyMock
import asyncio

from aiohttp import ClientConnectionError

from rotatingProxy.rotatingProxy import RotatingProxy
from rotatingProxy.heap import MaxHeap

class ProxyTests(unittest.TestCase):
    def setUp(self):
        pass


    def _test_make_req(self):
        async def get_html() -> list:
            rprox = RotatingProxy(proxy=['someproxy.net:8080'])
            rprox.excuse_proxy()
            res = []
            html = await rprox._make_request("http://www.ufcstats.com/statistics/events/completed")
            res.append(html)
            await rprox.session.close()

            return res

        loop = asyncio.get_event_loop()
        
        res = loop.run_until_complete(get_html())
        print(res)
        self.assertEqual(1, len(res))

    @patch('urllib.request.urlopen')
    def test_make_req_no_proxy(
        self,
        mock_urlopen:MagicMock
    ):
        ### mock the response object
        mock_reponse = MagicMock()
        mock_reponse.read.return_value = b''

        ### mock the with statement
        mock_urlopen.return_value.__enter__.return_value = mock_reponse

        async def get_html() -> list:
            """
            get URL w/o using the proxy
            """
            rprox = RotatingProxy(proxy_list=['someproxy.net:8080'])
            rprox.excuse_proxy()
            res = []
            html = await rprox._make_request("http://www.ufcstats.com/statistics/events/completed")
            res.append(html)
            await rprox.session.close()

            return res

        loop = asyncio.get_event_loop()
        
        res = loop.run_until_complete(get_html())
        print(f"Result: {res}")
        self.assertEqual(1, len(res))
        self.assertEqual(res[0],b"")

    @patch('rotatingProxy.rotatingProxy.open')
    def test_make_req_w_proxy_errs(
        self,
        mock_session:MagicMock,
    ):
        async def get_html(proxy_list) -> list:
            """
            get URL w/o using the proxy
            """
            rprox = RotatingProxy(proxy_list=proxy_list)
            res = []
            html = await rprox._make_request("http://www.ufcstats.com/statistics/events/completed")
            res.append(html)
            await rprox.session.close()

            return res

        loop = asyncio.get_event_loop()
        
        ### mock the with statement
        mock_session.side_effect = ClientConnectionError("ERROR")
        # mock_session.get.return_value.__enter__.return_value = mock_reponse

        proxy_list = [
            'fake_url_1',
            'fake_url_2',
            'fake_url_3'
        ]
        res = loop.run_until_complete(get_html(proxy_list))
        print(f"Result: {res}")
        self.assertEqual(1, len(res))
        self.assertIsNone(res[0])

        mock_session.side_effect = asyncio.TimeoutError("ERROR")
        # mock_session.get.return_value.__enter__.return_value = mock_reponse

        proxy_list = [
            'fake_url_1',
            'fake_url_2',
            'fake_url_3'
        ]
        res = loop.run_until_complete(get_html(proxy_list))
        print(f"Result: {res}")
        self.assertEqual(1, len(res))
        self.assertIsNone(res[0])

    def test_make_bad_url(self):
        async def getHtml() -> list:
            rprox = RotatingProxy(proxy_list=['localhost'])
            res = []
            html = await rprox._make_request("http://www.anljksdljsadfj.com")
            res.append(html)

            await rprox.session.close()

            return res

        loop = asyncio.get_event_loop()
        
        res = loop.run_until_complete(getHtml())
        self.assertIsNone(res[0])

class ProxyTest(unittest.TestCase):

    def test_class(self):
        from rotatingProxy.rotatingProxy import Proxy
        p = Proxy("http://testproxy:90")

        self.assertEqual(p.url,"http://testproxy:90")
        self.assertEqual(p.count,1)
        p.incrementCount()
        self.assertEqual(p.count,2)

    def test_header(self):
        from rotatingProxy.rotatingProxy import Proxy
        p = Proxy("http://testproxy:90")

        p.generateHeader()
        print(p.header)

class MaxHeapTest():
    pass
if __name__ == "__main__":
    unittest.main()