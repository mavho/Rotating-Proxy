# Rotating-Proxy
Some site is blocking you from stealing their data? Hopefully this module can fix that!

Example run:
from rotatingProxy import RotatingProxy

rprox = RotatingProxy()

### initiliaze the proxy list
rprox.generateProxyList()

bytes = rprox.getRawHTML('some url')


Use it in successive calls, heap state is stored. Proxies that are more successfull will be
used more often.


WIP:
    More user agents.
    Error Handling.
    request headers.