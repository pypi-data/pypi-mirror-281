from setuptools import setup, find_packages

setup(
    name='htbst',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'httpx',
        'asyncio'
    ],
    entry_points={
        'console_scripts': [
            'htbst-cli = htbst.main:main',  
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
