from setuptools import setup

setup(name='rotatingProxy',
    version='0.2.1',
    description='Helper class to go through proxy URLs. Uses a heap to keep track of request errors for those proxies.',
    author='Maverick',
    packages=['rotatingProxy'],
    install_requires=["aiohttp"]
)
