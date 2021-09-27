class HeapArr():
    def __init__(self):
        ###Utilize a heap representation
        self.arr = []

    def __len__(self):
        return len(self.arr)

    def __getitem__(self,idx):
        return self.arr[idx]

    def pushToHeap(self, value):
        self.arr.append(value)
        _sift_up(self.arr, len(self) - 1)

    def popHeap(self):
        _swap(self.arr, len(self) - 1, 0)
        element = self.arr.pop()
        _sift_down(self.arr, 0)
        self.proxy_size -= 1
        return element
    
    def peekHeap(self):
        return self.arr[0] if len(self.arr) != 0 else None

    def printHeap(self, index=1, indent=0):
        print("\t" * indent, f"{self.arr[index - 1]+ ' ' +  str(self.arr[index-1])}")
        left, right = 2 * index, 2 * index + 1
        if left <= len(self):
            self.printHeap(left, indent=indent + 1)
        if right <= len(self):
            self.printHeap(right, indent=indent + 1)

    def heap_gen(self):
        for index,proxy in enumerate(self.arr):
            yield index,proxy

### heap functions
def _swap(L, i, j):
    L[i], L[j] = L[j], L[i]


def _sift_up(heap, index):
    parent_index = (index - 1) // 2
    # If we've hit the root node, there's nothing left to do
    if parent_index < 0:
        return

    # If the current node is larger than the parent node, swap them
    if heap[index] > heap[parent_index]:
        _swap(heap, index, parent_index)
        _sift_up(heap, parent_index)


def _sift_down(heap, index):
    child_index = 2 * index + 1
    # If we've hit the end of the heap, there's nothing left to do
    if child_index >= len(heap):
        return

    # If the node has a both children, swap with the larger one
    if child_index + 1 < len(heap) and heap[child_index] < heap[child_index + 1]:
        child_index += 1

    # If the child node is smaller than the current node, swap them
    if heap[child_index]> heap[index]:
        _swap(heap, child_index, index)
        _sift_down(heap, child_index)
