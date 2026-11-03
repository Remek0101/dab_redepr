from setuptools import setup, find_packages

setup(
    name="dab_redepr",
    version="0.0.4",
    description="This contains the dab_redepr project code",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
