from setuptools import setup

setup(
    name='multidl',
    version='0.1',
    packages=['multidl'],
    install_requires=[
        'requests',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
    url='https://github.com/julienc91/multidl',
    license='MIT',
    author='Julien Chaumont',
    author_email='multidl@julienc.io',
    description='Download stuff in parallel'
)
