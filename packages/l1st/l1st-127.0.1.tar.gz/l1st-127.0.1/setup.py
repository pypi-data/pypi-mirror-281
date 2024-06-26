from setuptools import setup, find_packages

VERSION = '127.0.1' 
DESCRIPTION = 'A 1-indexed list in Python'
LONG_DESCRIPTION = 'A, very unnecessary, 1-indexed list in Python'

setup(
        name="l1st", 
        version=VERSION,
        author="shotnothing",
        author_email="shotnothinggg@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        
        keywords=['python', 'index', 'list', 'matlab', 'brain', 'damage',
                  ],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)