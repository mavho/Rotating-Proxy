import random

import ua_generator

class Proxy():
    def __init__(self,url):
        self.count = 1
        self.header = {}
        self.url = url 
    
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
        default_UA = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Mozilla/5.0 (Linux; Android 5.1.1; MXQ-PRO) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.96 Mobile Safari/537.36,gzip(gfe),gzip(gfe)',
            'Mozilla/5.0 (Linux; Android 9; ANE-LX3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.96 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 11; RMX3151) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 7.1.1; SM-T355) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.96 Safari/537.36',
            'Dalvik/2.1.0 (Linux; U; Android 8.1.0; Masstel X6 Build/O11019)',
            'Mozilla/5.0 (Linux; Android 10; ONEPLUS A6010) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.96 Mobile Safari/537.36,gzip(gfe),gzip(gfe)',
            'Mozilla/5.0 (Linux; U; Android 6.0.1; SM-P555 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.101 Safari/537.36 OPR/50.0.2254.149182',
            'Mozilla/5.0 (Linux; Android 11; GM1900) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.66 Mobile Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.125'
        ]

        browser = ('chrome', 'edge', 'firefox', 'safari')
        platform = ('windows','linux','android')
        device = ('desktop')
        try:
            ua = ua_generator.generate(device=device,platform=platform,browser=browser)
            self.header = {
                **ua.headers.get(),
                "X-Forwarded-For": "127.0.0.1",
                "Forwarded": "for=127.0.0.1",
                "Via": "none"
            }
        except:
            self.header = {
                'User-Agent': default_UA[random.randrange(len(default_UA))],
                "X-Forwarded-For": "127.0.0.1",
                "Forwarded": "for=127.0.0.1",
                "Via": "none"
            }

    

        
