import setuptools

setuptools.setup(
    # Needed to actually package something
    packages=setuptools.find_packages(exclude=("tests", "docs", "examples")),
    # Needed for dependencies
    install_requires=[
        "tensorflow == 2.9",
        "nengo == 3.2",
        "nengo_dl == 3.5",
        "nengo_extras == 0.5.0",
        "numpy == 1.24.2",
        "opencv-python == 4.7.0.68",
        "matplotlib == 3.6.3"
    ],
)
