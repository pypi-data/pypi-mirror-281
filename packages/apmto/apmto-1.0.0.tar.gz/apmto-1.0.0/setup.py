import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
with open('requirements.txt', 'r') as fh:
    requirements = [*map(str.strip, fh.readlines())]
    
setuptools.setup(
    name="apmto", 
    version="1.0.0",
    author="Geunhyeok Yu",
    author_email="geunhyeok0111@gmail.com",
    description="Simple python package wrapper for converting apple media formatted files into high-compatible formats.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nda111/APMTO",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=requirements
)