from setuptools import setup, find_packages

setup(
    name="shiutils",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple utility package with a hello function",
    long_description="# hello",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/shiutils",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
