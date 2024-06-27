from setuptools import setup, find_packages

setup(
    name="S3Lister",
    version="1.0.0",
    author="Cybenari",
    author_email="idan@cybenari.com",
    description="A S3 listing test",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cybenari",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
