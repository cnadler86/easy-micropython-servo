from setuptools import setup, find_packages

setup(
    name='easy-micropython-servo',
    version='0.1.0',
    url='https://github.com/cnadler86/easy-micropython-servo',
    author='Christopher Nadler',
    description='A MicroPython library for controlling servos by target angle and speed of movement.',
    packages=find_packages(),  # Automatische Suche nach allen Paketen
    install_requires=[],  # Liste der Abhängigkeiten (andere Pakete, die Ihre Bibliothek benötigt)
)
