from setuptools import setup, find_packages

VERSION = "0.1.0"
DESCRIPTION = "Piaget's FUCs filler"
LONG_DESCRIPTION = ''

setup(
    name="pyfuc",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Natanael Quintino",
    author_email="natanael.quintino@ipiaget.pt",
    license='CC0 1.0 Universal',
    packages=find_packages(
        include=['pyfuc', 'pyfuc.*']
        ),
    install_requires=[
        "pdflatex", "langchain_openai", "deepl", "sydney-py"
    ],
    keywords='automation, curricular unit, FUC, piaget',
    classifiers= [
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ]
)
