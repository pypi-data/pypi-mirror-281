from setuptools import setup, find_packages

setup(
    name="fair_mobility_models", #***
    version="0.0.1",
    description="Extension of the fair-mobil package with synthetic data generation",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.6.0",
        "pandas>=1.2.0",
        "geopandas>=0.9.0",
        "plotly>=5.0.0",
        "scikit-mobility>=1.3.1"
    ],
    entry_points={
        "console_scripts": [
            "grav-model = fair_mobility_models.gravity:grav_Model",
            "rad-model = fair_mobility_models.radiation:rad_Model",
        ],
    },
)