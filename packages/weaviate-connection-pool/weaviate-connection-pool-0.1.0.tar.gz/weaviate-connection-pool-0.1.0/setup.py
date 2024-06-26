from setuptools import setup, find_packages

setup(
    name='weaviate-connection-pool',
    version='0.1.0',
    author='Sushil2308',
    author_email='SushilPrasad60649@gmail.com',
    packages=find_packages(),
    url='https://github.com/Sushil2308/weaviate_connection_pool',
    license='LICENSE.txt',
    description='An efficient connection pool for Weaviate clients.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Specify the format of the long_description
    install_requires=[
        "weaviate-client>=2.5.0",
    ],
)