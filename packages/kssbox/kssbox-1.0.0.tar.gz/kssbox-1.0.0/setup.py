from setuptools import setup, find_packages

VERSION = '1.0.0'

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="kssbox",
    version=VERSION,
    author="kevin brother",
    author_email="1301239018@qq.com",
    description="kssbox test",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    keywords=['kssbox', 'add', 'test'],
    license="MIT",
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"
    ]
)