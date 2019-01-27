import setuptools

with open("Readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jsonapi-simple",
    version="0.2.2",
    author="Alejandro Piad",
    author_email="apiad@apiad.net",
    description="A minimalistic JSON API framework in Python with support for graphql-style queries.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/apiad/jsonapi",
    packages=['jsonapi'],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
