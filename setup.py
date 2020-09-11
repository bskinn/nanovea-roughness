from setuptools import find_packages, setup


# May need to do more with an install_requires??

setup(
    name="neutrino_polzn",
    version="2020.07.31.1056",
    description="Data preprocessor for GDOEII_Neutrino polarization scans",
    author="Brian Skinn",
    author_email="brianskinn@faradaytechnology.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    provides=["neutrino_polzn"],
    python_requires=">=3.8",  # assignment expressions
    install_requires=["numpy", "scipy", "matplotlib", "pandas", "openpyxl", "pent", "attrs", "tqdm"]
)
