from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='trader-tweets-core',
    version='0.1.2',
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
    install_requires=required,
)
