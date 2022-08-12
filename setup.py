from setuptools import setup
from remarkable_keyboard import version

setup(
    name='remarkable-keyboard',
    version=version.__version__,
    packages=['remarkable_keyboard'],
    author="Evan Widloski",
    author_email="evan@evanw.org",
    description="use reMarkable as a wireless mouse and keyboard",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license="GPLv3",
    keywords="remarkable tablet evdev mouse keyboard",
    url="https://github.com/evidlo/remarkable_keyboard",
    entry_points={
        'console_scripts': [
            'remarkable-keyboard = remarkable_keyboard.remarkable_keyboard:main',
            'rekeyboard = remarkable_keyboard.remarkable_keyboard:main'
        ]
    },
    install_requires=[
        'pycryptodome',
        'paramiko',
        'screeninfo',
        'pynput',
        'remarkable-mouse>=5',
        'sortedcontainers'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
