from setuptools import setup

setup(
    name='multidl',
    version='0.1',
    packages=[
        'multidl',
        'multidl.constants',
        'multidl.downloaders'
    ],
    install_requires=[
        'requests',
        'tqdm',
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
    description='Download stuff in parallel',
    entry_points={
        'console_scripts': [
            'multidl = multidl.cli:main',
        ],
    },
)
