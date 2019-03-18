from setuptools import setup
from remarkable_keyboard import version

setup(
    name='remarkable-keyboard',
    version=version.__version__,
    packages=['remarkable_keyboard'],
    author="Evan Widloski",
    author_email="evan@evanw.org",
    description="use reMarkable as a graphics tablet",
    long_description=open('README.md').read(),
    license="GPLv3",
    keywords="remarkable tablet evdev",
    url="https://github.com/evidlo/remarkable_keyboard",
    entry_points={
        'console_scripts': [
            'remarkable-keyboard = remarkable_keyboard.remarkable_keyboard:main',
            'rekeyboard = remarkable_keyboard.remarkable_keyboard:main'
        ]
    },
    install_requires=[
        'paramiko',
        'screeninfo',
        'pynput',
        'remarkable-mouse'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
