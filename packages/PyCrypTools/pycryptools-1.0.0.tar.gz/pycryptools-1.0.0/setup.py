from setuptools import setup, find_packages

setup(
    name="PyCrypTools",
    version="1.0.0",
    author="LixNew",
    author_email="lixnew2@gmail.com",
    description="A simple cryptography tools library for Python.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LixNew2/PyCrypTools",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={
        "pycryptools": ["bin/*.exe"]        
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "cryptography"
    ],
)