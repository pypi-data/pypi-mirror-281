from setuptools import setup, find_packages

setup(
    name="romer_midibot",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pyserial",
    ],
    author="Omar Habib",
    author_email="omar1farouk@gmail.com",
    description="A Python API for the MIDIbot",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    python_requires=">=3.6",
    license="Apache License 2.0",
)
