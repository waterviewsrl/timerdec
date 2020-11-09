import setuptools

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="timerdec",
    version="0.0.1",
    author="Matteo Ferrabone",
    author_email="matteo.ferrabone@gmail.com",
    license='MIT',
    description="Simple decorators for measuring Python methods execution time",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/desmoteo/timerdec",
    packages=setuptools.find_packages(),
    install_requires=[
        "tqdm",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Topic :: Utilities ',
    ],
    python_requires='>=3.6',
)
