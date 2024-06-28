from setuptools import find_packages, setup

setup(
    name="refspy",
    version="0.9.0",
    description="A Python package for working with biblical references in texts",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Nigel Chapman",
    author_email="nigel@chapman.id.au",
    url="https://github.com/eukras/refspy",
    package_dir={"": "refspy"},
    packages=find_packages(where="refspy"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pydantic 2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Religion",
    ],
)
