import urllib.request
from proxy import Proxy
from heap import HeapArr,_sift_up,_sift_down
import random, time, os

class RotatingProxy():
    def __init__(self, timeout=1, proxy_list=None, perserve_state=True):
        ###Utilize a heap representation
        self.proxy_heap = HeapArr() 
        self.proxy_size = 0 

        self.proxy_list = proxy_list
        if self.proxy_list is not None:
            self.generateProxyList(proxy_list)

        ### optional declarations
        self.timeout=timeout 

    def generateProxyList(self,proxy_list):
        basedir = os.path.abspath(os.path.dirname(__file__))

        with open(f"{basedir}/{proxy_list}",'r') as fobj:
            for line in fobj:
                self.proxy_size += 1
                proxy = Proxy(line)
                proxy.count = 1 
                self.proxy_heap.pushToHeap(proxy)

    ###
    ### Successive calls to get RawHTML will alter the
    ### heap, and heapify accordingly
    ### 
    def getRawHTML(self,url):
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
            req = urllib.request.Request(
                url = url,
                data = None,
                headers = proxy.header,
            )
            authinfo = urllib.request.HTTPBasicAuthHandler()

            proxy_support = urllib.request.ProxyHandler({'http': proxy.ip})

            opener = urllib.request.build_opener(proxy_support,authinfo,urllib.request.CacheFTPHandler)

            ### attempt to read the page.
            try:
                endpoint = opener.open(req)
                mybytes = endpoint.read()
                endpoint.close()
                print('Able to open ' + proxy.ip,flush=True)
                self.proxy_heap[index].incrementCount()
                _sift_up(self.proxy_heap, index)
                return mybytes
            except Exception as e:
                print('Not able to open ' + proxy.ip,flush=True)
                self.proxy_heap[index].decrementCount()
                if self.proxy_heap[index].count <= 0:
                    self.proxy_heap.popHeap()
                else:
                    _sift_down(self.proxy_heap,index)
                print(e ,flush=True)
                if self.proxy_size <= 0:
                    raise IndexError("No ip's work")
        return None 