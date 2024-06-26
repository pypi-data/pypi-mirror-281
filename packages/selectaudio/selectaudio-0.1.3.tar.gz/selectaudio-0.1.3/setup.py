from setuptools import setup, find_packages

setup(
    name="selectaudio",
    version="0.1.3",
    description="A tool to set PulseAudio source/sink using an interactive menu",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="4thel00z",
    author_email="4thel00z@gmail.com",
    url="https://github.com/4thel00z/selectaudio",
    packages=find_packages(),
    install_requires=[
        "pulsectl",
        "prompt_toolkit",
    ],
    entry_points={
        "console_scripts": [
            "sa=selectaudio.__main__.py:main",
            "selectaudio=selectaudio.__main__.py:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

