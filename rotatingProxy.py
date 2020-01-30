import urllib.request
from proxy import Proxy

class RotatingProxy():
    def __init__(self, entropy=0.3):
        self.working_proxy = ''
        ###Utilize a heap representation
        self.proxy_list = []
        self.proxy_size = 0 

        #self.generateProxyList(self.proxy_list)

        ### optional declarations
        self.entropy = entropy

    def generateProxyList(self):
        fobj = open('proxy_list.txt', 'r')
        count = 0
        for line in fobj:
            count += 1
            proxy = Proxy(line)
            proxy.count = count
            self.pushToHeap(proxy)

    def pushToHeap(self, value):
        self.proxy_list.append(value)
        _sift_up(self.proxy_list, len(self) - 1)

    def popHeap(self):
        _swap(self.proxy_list, len(self) - 1, 0)
        element = self.proxy_list.pop()
        _sift_down(self.proxy_list, 0)
        return element
    
    def peekHeap(self):
        return self.proxy_list[0] if len(self.proxy_list) != 0 else None

    def __len__(self):
        return len(self.proxy_list)

    def printHeap(self, index=1, indent=0):
        print("\t" * indent, f"{self.proxy_list[index - 1].ip + ' ' +  str(self.proxy_list[index-1].count)}")
        left, right = 2 * index, 2 * index + 1
        if left <= len(self):
            self.printHeap(left, indent=indent + 1)
        if right <= len(self):
            self.printHeap(right, indent=indent + 1)
    ###
    ### Successive calls to get RawHTML will alter the
    ### heap, and heapify accordingly
    ### 

    def getRawHTML(self,url):
        success=False
        for proxy in self.proxy_list.keys()[:]:
            proxy.generateHeader() 
            req = urllib.request.Request(
                url = url,
                data = None,
                headers = proxy.header,
            )
            authinfo = urllib.request.HTTPBasicAuthHandler()
            if self.working_proxy is not '':
                proxy_support = urllib.request.ProxyHandler({'http': self.working_proxy})
            else:
                proxy_support = urllib.request.ProxyHandler({'http': proxy.ip})

            opener = urllib.request.build_opener(proxy_support,authinfo,urllib.request.CacheFTPHandler)
            try:
                endpoint = opener.open(req)
                #endpoint = urllib.request.urlopen(req) 
                mybytes = endpoint.read()
                endpoint.close()
                print('Able to open ' + proxy.ip,flush=True)
                self.working_proxy = proxy.ip
                success=True
                time.sleep(random.randrange(entropy))
                proxy_list[proxy] += 1
                break
            except Exception as e:
                success=False
                if proxy in proxy_list and proxy_list[proxy] == 0:
                    del proxy_list[proxy]
                else:
                    proxy_list[proxy] -= 1
                print(e ,flush=True)
                self.working_proxy = ''
                time.sleep(random.randrange(entropy))
        #endpoint = request.get(url) #mybytes = endpoint.content
        return mybytes

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


