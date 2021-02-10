
import setuptools

LONG_DESCRIPTION = """
rpcbSVG is a Python 3 library to generate SVG content.
"""

setuptools.setup(
    name="rpcbSVG", 
    version="0.9.0",
    author="Rui Pedro Cavaco Barrosa",
    author_email="rpcavaco@gmail.com",
    description="An SVG generating package",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/rpcavaco/rpcbSVG",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
