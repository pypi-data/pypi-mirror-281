from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = "0.1"
DESCRIPTION = "Accuracy assessment on edge"

setup(
    name="AssessEdge",
    version=VERSION,
    author="Yingfan Zhang",
    author_email="<zhangyingfanuk@163.com>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Remote-Sensing-of-Land-Resource-Lab/AssessEdge",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy",
        "scipy",
        "seaborn",
        "matplotlib",
        "scikit-image",
        "rasterio",
    ],
    keywords=["python", "edge", "accuracy"],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows",
    ],
)
