import urllib.request
import asyncio 
import heapq
from typing import List

from aiohttp import (
    ClientSession,
    ClientResponseError,
    ClientTimeout,
    ClientConnectionError,
    ClientPayloadError
)
from aiohttp.client_exceptions import TooManyRedirects

from rotatingProxy.proxy import Proxy 
import rotatingProxy.heap as HA

class InvalidContentTypeError(Exception):
    """
    This represents an exception when response content type is not in the valid content type set.
    """
    def __init__(self,response):
        self.response = response

class RotatingProxy():
    """Inserts URLS from proxy list into a priority queue.
    Used to crawl URLS
    """
    valid_content_types = set([
        'text/html',
        'text/xhtml',
        'application/xhtml+xml',
        'application/xhtml',
        'application/html'
    ])
    def __init__(
        self,
        timeout=1,
        proxy_list:list=None,
        perserve_state=True,
        loop:asyncio.AbstractEventLoop=None
    ):
        ###Utilize a heap representation
        self.proxy_heap = HA.MaxHeap() 
        self.proxy_size = 0 

        self.proxy_list = proxy_list
        if self.proxy_list is not None:
            self.generateProxyList(proxy_list)

        ### optional declarations
        self.timeout=timeout 

        if not loop:
            loop = asyncio.get_event_loop()
        
        self.loop = loop

        self.session = ClientSession(loop=self.loop)

    def excuse_proxy(self):
        """
        Call to not use a proxy
        """
        self.proxy_list = None

    def generateProxyList(self,proxy_list_path):
        """Inserts proxy list text file into priority queue.

        Args:
            proxy_list_path (str): Path to proxy file list. Each line must be a url.
        """
        with open(proxy_list_path,'r') as fobj:
            for line in fobj:
                proxy = Proxy(line)
                self.proxy_heap.pushToHeap(proxy)

    def decrement_and_check(self,index):
        self.proxy_heap[index].decrementCount()
        if self.proxy_heap[index].count <= 0:
            self.proxy_heap.popHeap()
        else:
            HA._sift_down(self.proxy_heap,index)
        if self.proxy_size <= 0:
            raise IndexError("No ip's work")
    ###
    ### Successive calls to get RawHTML will alter the
    ### heap, and heapify accordingly
    ### 
    async def _make_request(self,url):
        if not self.session:
            self.session = ClientSession(loop=self.loop)

        timeout = ClientTimeout(total=self.timeout)

        ### If a proxy list isn't specified, try a simple urlopen.
        if self.proxy_list is None or not self.proxy_heap:
            try:
                with urllib.request.urlopen(url) as response:
                    mybytes = response.read()
            except Exception:
                return None

            return mybytes

        while self.proxy_heap:
            top_proxy = self.proxy_heap.popHeap()
            # print(top_proxy.ip)

            if not top_proxy:
                raise IndexError("No ip's Work") 
            top_proxy.generateHeader() 

            try:
                async with self.session.get(
                    url = url,
                    headers = top_proxy.header,
                    raise_for_status=True,
                    timeout=timeout,
                    proxy=f"http://{top_proxy.ip}"
                ) as response:
                    if response.content_type not in self.valid_content_types:
                        raise InvalidContentTypeError(response)

                    html = await response.txt()
                    
            ### Handle the errors that is thrown from session.get()
            except ClientConnectionError as e:
                top_proxy.decrementCount()
                if top_proxy >= 0:
                    self.proxy_heap.pushToHeap(top_proxy)
                print(e)
            except ClientResponseError as e:
                top_proxy.decrementCount()
                if top_proxy >= 0:
                    self.proxy_heap.pushToHeap(top_proxy)
                print(e)
            except TimeoutError as e:
                top_proxy.decrementCount()

                if top_proxy >= 0:
                    self.proxy_heap.pushToHeap(top_proxy)
                print(e)
            except Exception as e:
                print("ran into exception")
                print(e)
                raise e
            else:
                top_proxy.incrementCount()
                self.proxy_heap.pushToHeap(top_proxy)
                return html