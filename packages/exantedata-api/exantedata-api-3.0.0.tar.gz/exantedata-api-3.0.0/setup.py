import setuptools

setuptools.setup(
    name = "exantedata-api",
    version = "3.0.0",
    author = "tech@exantedata.com",
    description = "ExanteData API python library",
    packages=['exantedata_api'],
    install_requires=['pandas', 'requests'],
)
