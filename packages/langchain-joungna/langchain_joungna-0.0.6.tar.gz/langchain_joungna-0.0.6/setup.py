from setuptools import setup, find_packages

setup(
    name="langchain-joungna",
    version="0.0.6",
    description="LangChain Helper Library",
    author="joungna",
    author_email="joungna@gmail.com",
    url="https://github.com/joungna/langchain-joungna",
    install_requires=["langchain"],
    packages=find_packages(exclude=[]),
    keywords=[
        "langchain",
        "joungna",
    ],
    python_requires=">=3.10",
    package_data={},
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)