import unittest 
from unittest.mock import patch,MagicMock,PropertyMock
import asyncio

from rotatingProxy.rotatingProxy import RotatingProxy
from rotatingProxy.heap import MaxHeap

class ProxyTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_class(self):
        from rotatingProxy.rotatingProxy import Proxy
        p = Proxy("asdf")

        self.assertEqual(p.ip,"asdf")
        self.assertEqual(p.count,1)
        p.incrementCount()
        self.assertEqual(p.count,2)

    def _test_make_req(self):
        async def get_html() -> list:
            rprox = RotatingProxy(proxy_list='proxy_list.txt')
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
            rprox = RotatingProxy(proxy_list='proxy_list.txt')
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

    @patch('rotatingProxy.rotatingProxy.open')
    @patch('rotatingProxy.rotatingProxy.ClientSession.get',new_callable=PropertyMock)
    def test_make_req_w_proxy_errs(
        self,
        mock_session:MagicMock,
        mock_open:PropertyMock
    ):
        from aiohttp import ClientConnectionError,ClientResponseError


        async def get_html() -> list:
            """
            get URL w/o using the proxy
            """
            rprox = RotatingProxy(proxy_list='proxy_list.txt')
            res = []
            html = await rprox._make_request("http://www.ufcstats.com/statistics/events/completed")
            res.append(html)
            await rprox.session.close()

            return res

        loop = asyncio.get_event_loop()
        
        ### mock the with statement
        mock_session.side_effect = ClientConnectionError("ERRORR")
        # mock_session.get.return_value.__enter__.return_value = mock_reponse

        mock_open.return_value.__enter__.return_value = [
            'fake_url_1',
            'fake_url_2',
            'fake_url_3'
        ]
        res = loop.run_until_complete(get_html())
        print(f"Result: {res}")
        self.assertEqual(1, len(res))
        self.assertIsNone(res[0])

        mock_session.side_effect = TimeoutError("ERRORR")
        # mock_session.get.return_value.__enter__.return_value = mock_reponse

        mock_open.return_value.__enter__.return_value = [
            'fake_url_1',
            'fake_url_2',
            'fake_url_3'
        ]
        res = loop.run_until_complete(get_html())
        print(f"Result: {res}")
        self.assertEqual(1, len(res))
        self.assertIsNone(res[0])


        ### mock the with statement
        mock_session.side_effect = Exception("ERRORR")
        # mock_session.get.return_value.__enter__.return_value = mock_reponse

        mock_open.return_value.__enter__.return_value = [
            'fake_url_1',
            'fake_url_2',
            'fake_url_3'
        ]
        ## exceptions will just trigger an error
        with self.assertRaises(Exception):
            res = loop.run_until_complete(get_html())


    def test_make_bad_url(self):
        async def getHtml() -> list:
            rprox = RotatingProxy(proxy_list='proxy_list.txt')
            res = []
            html = await rprox._make_request("http://www.anljksdljsadfj.com")
            res.append(html)

            await rprox.session.close()

            return res

        loop = asyncio.get_event_loop()
        
        with self.assertRaises(asyncio.TimeoutError):
            res = loop.run_until_complete(getHtml())


class MaxHeapTest():
    pass
if __name__ == "__main__":
    unittest.main()