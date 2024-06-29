from setuptools import setup, find_packages

setup(
    name='trader-tweets-core',
    version='0.1.4',
    author='Will H-S',
    author_email='whardwicksmith@gmail.com',
    packages=find_packages(where='.'),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
    install_requires=[
        'openai==1.17.1',
        'requests==2.31.0',
        'setuptools~=69.1.1',
        'parameterized==0.9.0',
        'diskcache==5.6.3'
    ]
)
