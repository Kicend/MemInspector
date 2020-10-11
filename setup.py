from setuptools import setup

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name='MemInspector',
    version='1.0.0',
    packages=[],
    install_requires=requirements,
    url='https://github.com/Kicend/MemInspector',
    license='MIT',
    author='Filip "Kicend" Szczepanowski',
    author_email='kicend@gmail.com',
    description='Menedżer pamięci'
)