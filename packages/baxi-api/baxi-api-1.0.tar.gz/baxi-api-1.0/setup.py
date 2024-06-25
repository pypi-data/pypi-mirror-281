import os
from setuptools import setup, find_packages

setup(
    name='baxi-api',
    version='1.0',
    packages=find_packages(where=os.path.dirname(__file__)),  # <--- Update this line
    package_dir={'': os.path.dirname(__file__)},
    install_requires=["requests", "discord.py"],
    author="Red_Wolf2467",
    author_email="support@pyropixle.com",
    description="Allows you to interact with our Baxi API."
)