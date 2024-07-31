
from setuptools import setup, find_packages

setup(
    name='chat_client',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            'chat_client=chat_client:main',
        ],
    },
)

