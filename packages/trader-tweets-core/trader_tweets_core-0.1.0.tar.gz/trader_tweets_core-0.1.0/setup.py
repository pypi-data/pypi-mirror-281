from setuptools import setup, find_packages

setup(
    name='trader_tweets_core',
    version='0.1.0',
    author='Will H-S',
    author_email='whardwicksmith@gmail.com',
    description='A module for processing and analyzing trader tweets.',
    packages=find_packages(where='.'),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
    install_requires=[
        'openai~=0.18.1',
        'setuptools~=62.3.2',
        'pytest~=5.4.1',
        'parameterized~=0.8.1',
        'diskcache~=5.4.0',
        'functions-framework==3.*',
    ]
)
