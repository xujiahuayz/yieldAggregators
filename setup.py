from setuptools import setup, find_packages


setup(
    name="yield",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
    ],
    extras_require={"dev": ["pylint", "black", "pytest"]},
    entry_points={
        "console_scripts": ["yieldenv=yieldenv.cli:run"],
    },
)
