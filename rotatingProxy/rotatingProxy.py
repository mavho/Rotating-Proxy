import urllib.request
from asyncio import TimeoutError
from aiohttp import ClientSession, ClientResponseError,ClientTimeout, ClientConnectionError, ClientPayloadError
from aiohttp.client_exceptions import TooManyRedirects

from rotatingProxy.proxy import Proxy 
import rotatingProxy.heap as HA
import random, time, os

class InvalidContentTypeError(Exception):
    """
    This represents an exception when response content type is not in the valid content type set.
    """
    def __init__(self,response):
        self.response = response

class RotatingProxy():
    valid_content_types = set([
        'text/html',
        'text/xhtml',
        'application/xhtml+xml',
        'application/xhtml',
        'application/html'
    ])
    def __init__(self, timeout=1, proxy_list=None, perserve_state=True):
        ###Utilize a heap representation
        self.proxy_heap = HA.HeapArr() 
        self.proxy_size = 0 

        self.proxy_list = proxy_list
        if self.proxy_list is not None:
            self.generateProxyList(proxy_list)

        ### optional declarations
        self.timeout=timeout 

        self.session = ClientSession()

    def generateProxyList(self,proxy_list_path):
        with open(proxy_list_path,'r') as fobj:
            for line in fobj:
                self.proxy_size += 1
                proxy = Proxy(line)
                proxy.count = 1 
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
            self.session = ClientSession()
        timeout = ClientTimeout(total=self.timeout)

        ### If a proxy list isn't specified, try a simple urlopen.
        if self.proxy_list is None:
            with urllib.request.urlopen(url) as response:
                mybytes = response.read()

            return mybytes

        for index,proxy in self.proxy_heap.heap_gen():
            if len(self.proxy_heap)<= 0:
                raise IndexError("No ip's work")

            print(index,proxy)
            ### Build the proxy headers and http headers
            proxy.generateHeader() 

            try:
                async with self.session.get(
                    url = url,
                    headers = proxy.header,
                    raise_for_status=True,
                    timeout=timeout,
                    proxy=f"http://{proxy.ip}"
                ) as response:
                    if response.content_type not in self.valid_content_types:
                        raise InvalidContentTypeError(response)

                    html = await response.txt()
                    
            ### Handle the errors that is thrown from session.get()
            except ClientConnectionError as e:
                self.decrement_and_check(index,)
                print(e ,flush=True)
            except ClientResponseError as e:
                self.decrement_and_check(index)
                print(e ,flush=True)
            except TimeoutError as e:
                self.decrement_and_check(index)
                print(e ,flush=True)
            except Exception as e:
                print("ran into exception")
                print(e)
                raise e
            else:
                self.proxy_heap[index].incrementCount()
                HA._sift_up(self.proxy_heap, index)
                return html
    
        return None 