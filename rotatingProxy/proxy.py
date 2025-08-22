import random

class Proxy():
    def __init__(self,ip):
        self.count = 1
        self.header = {}
        self.ip = ip 
    
    def __lt__(self,other):
        return self.count < other

    def __gt__(self,other):
        return self.count > other

    def __eq__(self,other):
        return self.count == other

    def __le__(self,other):
        return self.count <= other

    def __ge__(self,other):
        return self.count >= other

    def __str__(self):
        return f"{self.ip}: {self.count}"

    def incrementCount(self):
        self.count += 1

    def decrementCount(self):
        self.count -= 1
    
    def generateHeader(self):
        """
        Creates a random header 
        """
        UA = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
             'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36']
        self.header = {'User-Agent': UA[random.randrange(3)]}
    

        
