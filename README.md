# Rotating-Proxy
Some site is blocking you from stealing their data? Hopefully this module can fix that!

Example run:

```
async def get_html():
    """
    get URL w/o using the proxy
    """
    rprox = RotatingProxy(proxy_list='proxy_list.txt')
    res = []
    html = await rprox._make_request("http://www.example_site.com")
    await rprox.session.close()

    return html

loop = asyncio.get_event_loop()
html = loop.run_until_complete(get_html())
```

You can also opt out of the proxy with `rprox.excuse_proxy()`


Use it in successive calls, heap state is stored. Proxies that are more successful will be
used more often.

### Proxy List format
Each line has 1 IP:Port format.

Use it in successive calls, heap state is stored. Proxies that are more successfull will be
used more often.
