import setuptools

with open("requirements.txt", "r+", encoding="utf-8") as file:
    dependences = file.read().strip().split("\n")
file.close()

with open("README.md", "r+", encoding='utf-8') as file:
    long_description = file.read()
file.close()

setuptools.setup(
    name="BDXConverter",
    version="1.0.6",
    author="Minecraft Muti-Media Organization",
    author_email="TriM-Organization@hotmail.com",
    description="A code library to marshal, unmarshal, visual and reverse visualization of BDX files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TriM-Organization/BDXConverter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=dependences,
    python_requires='>=3.11',
)
