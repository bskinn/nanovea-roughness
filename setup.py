from setuptools import find_packages, setup


# May need to do more with an install_requires??

setup(
    name="nanovea_roughness",
    version="2020.09.11.1000",
    description="Surface roughness calculator for Nanovea scan export files",
    author="Brian Skinn",
    author_email="brian.skinn@gmail.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    provides=["nanovea_roughness"],
    python_requires=">=3.5",
    install_requires=["numpy~=1.19", "scipy~=1.5", "openpyxl==3.0.5", "tqdm==4.48.2"],
    entry_points={
        "console_scripts": ["nanovea-roughness = nanovea_roughness:main"],
    },
)
