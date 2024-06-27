from setuptools import setup, find_packages

setup(
    name='python_chibisafe',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',  # Adicione todas as dependências necessárias aqui
    ],
    author='Andre Felipe Oliveira de Azevedo Dantas',
    author_email='andre.dantas@isd.org.br',
    description='Um facilitador para usar a API Chibisafe',
    keywords='caddywrapper chibisafe api wrapper',
    url='https://github.com/isd-iin-els/python_chibisafe',  # Opcional
)