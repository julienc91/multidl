from setuptools import setup

setup(
    name='multidl',
    version='1.0',
    packages=['multidl'],
    install_requires=[
        'requests',
        'argparse',
    ],
    url='https://github.com/julienc91/multidl',
    license='MIT',
    author='Julien Chaumont',
    author_email='multidl@julienc.io',
    description='Download stuff in parallel'
)
