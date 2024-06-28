import setuptools
from pathlib import Path

#long_desc = Path("EL readme con el que lo explique")
#en este caso el readme no lo quiero usar. :)

setuptools.setup(
    name="holaMundoLayer",
    version="0.0.0",
    long_description="este es un pequete hecho con el curso de \"Ultimate python\"",
    packages=setuptools.find_packages(
        exclude=["mocks","test", "--", "archivos", "exceptions", "indice_paquetes","modulos","paquetes_nativos","rutas&Directorios","sqlite"]
    )
)