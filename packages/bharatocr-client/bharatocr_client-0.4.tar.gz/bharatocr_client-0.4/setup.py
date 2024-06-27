# author:    Kunal Kumar Kushwaha
# website:   http://www.essentia.dev

import setuptools
import glob

# Long description
with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fp:
    install_requires = fp.read()

setuptools.setup(
    name="bharatocr-client",
    version="0.4",
    description="bharatocr-client is an opensource python library to access BharatOcrAPIs ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/essentiasoftserv/bharatocrclient",
    author="essentiasoftserv",
    python_requires=">=3.6",
    install_requires=install_requires,
    author_email="kunal@essentia.dev",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    license="Apache",
)
