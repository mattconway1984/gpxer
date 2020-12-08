import setuptools

setuptools.setup(
    packages=setuptools.find_namespace_packages(),
    name="gpxer",
    version="0.0.0",
    install_requires=[
        "geopy",
        "gpxpy",
    ],
    python_requires=">=3.8"
)
