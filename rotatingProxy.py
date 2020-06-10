import urllib.request
from proxy import Proxy
import random, time, os

class RotatingProxy():
    def __init__(self, timeout=1, proxy_list=None, perserve_state=True):
        ###Utilize a heap representation
        self.proxy_heap= []
        self.proxy_size = 0 

        self.generateProxyList(proxy_list)

        ### optional declarations
        self.timeout=timeout 

    def generateProxyList(self,proxy_list):
        basedir = os.path.abspath(os.path.dirname(__file__))
        fobj = open(basedir + '/' + proxy_list, 'r')
        for line in fobj:
            self.proxy_size += 1
            proxy = Proxy(line)
            proxy.count = 1 
            self.pushToHeap(proxy)

    def pushToHeap(self, value):
        self.proxy_heap.append(value)
        _sift_up(self.proxy_heap, len(self) - 1)

    def popHeap(self):
        _swap(self.proxy_heap, len(self) - 1, 0)
        element = self.proxy_heap.pop()
        _sift_down(self.proxy_heap, 0)
        self.proxy_size -= 1
        return element
    
    def peekHeap(self):
        return self.proxy_heap[0] if len(self.proxy_heap) != 0 else None

    def __len__(self):
        return len(self.proxy_heap)

    def printHeap(self, index=1, indent=0):
        print("\t" * indent, f"{self.proxy_heap[index - 1].ip + ' ' +  str(self.proxy_heap[index-1].count)}")
        left, right = 2 * index, 2 * index + 1
        if left <= len(self):
            self.printHeap(left, indent=indent + 1)
        if right <= len(self):
            self.printHeap(right, indent=indent + 1)
    ###
    ### Successive calls to get RawHTML will alter the
    ### heap, and heapify accordingly
    ### 

    def heap_gen(self):
        for index,proxy in enumerate(self.proxy_heap):
            yield index,proxy

    def getRawHTML(self,url):
        for index,proxy in self.heap_gen():
            if self.proxy_size <= 0:
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
                time.sleep(random.randrange(self.timeout))
                return mybytes
            except Exception as e:
                print('Not able to open ' + proxy.ip,flush=True)
                self.proxy_heap[index].decrementCount()
                if self.proxy_heap[index].count <= 0:
                    self.popHeap()
                else:
                    _sift_down(self.proxy_heap,index)
                print(e ,flush=True)
                if self.proxy_size <= 0:
                    raise IndexError("No ip's work")
                time.sleep(random.randrange(self.timeout))
        return None 

### heap functions
def _swap(L, i, j):
    L[i], L[j] = L[j], L[i]


def _sift_up(heap, index):
    parent_index = (index - 1) // 2
    # If we've hit the root node, there's nothing left to do
    if parent_index < 0:
        return

    # If the current node is larger than the parent node, swap them
    if heap[index].count > heap[parent_index].count:
        _swap(heap, index, parent_index)
        _sift_up(heap, parent_index)


def _sift_down(heap, index):
    child_index = 2 * index + 1
    # If we've hit the end of the heap, there's nothing left to do
    if child_index >= len(heap):
        return

    # If the node has a both children, swap with the larger one
    if child_index + 1 < len(heap) and heap[child_index].count < heap[child_index + 1].count:
        child_index += 1

    # If the child node is smaller than the current node, swap them
    if heap[child_index].count > heap[index].count:
        _swap(heap, child_index, index)
        _sift_down(heap, child_index)