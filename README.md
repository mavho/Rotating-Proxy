# Rotating-Proxy
Some site is blocking you from stealing their data? Hopefully this module can fix that!

Example run:
from rotatingProxy import RotatingProxy

### initiliaze the proxy list
```rprox = RotatingProxy(proxy_list='proxy_list.txt')```

Calling this function will initialize the Proxy with the specified proxy_list.
You can initialize the class without a proxy list, and it'll still work.

### Requests
```html = await rprox._make_request("some_sitestring.")```
html is the html of the site.


### Proxy List format
Each line has 1 IP:Port format.

Use it in successive calls, heap state is stored. Proxies that are more successfull will be
used more often.
