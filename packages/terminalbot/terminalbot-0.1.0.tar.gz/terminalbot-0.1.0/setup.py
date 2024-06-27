# setup.py

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='terminalbot',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'terminalbot=terminalbot.bot:main',
        ],
    },
    author='Fidal',
    author_email='mrfidal@proton.me',
    description='A package to interact with a Telegram group by sending and receiving messages',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://mrfidal.in', 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
