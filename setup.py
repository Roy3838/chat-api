
from setuptools import setup

setup(
    name='chat_client',
    version='1.0.0',
    py_modules=['main'],  # This tells setup to include 'main.py'
    include_package_data=True,
    install_requires=[
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            'chat_client=main:main',
        ],
    },
)
