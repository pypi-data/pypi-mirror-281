from setuptools import setup, find_packages

setup(
    name="easy-function-time",
    version="1.0.0",
    packages=find_packages(),
    description="A simple decorator to measure function execution time",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="lukesud0m",
    author_email="lukemarshall511@gmail.com",
    url="https://github.com/lukesudom/easy-function-time",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)