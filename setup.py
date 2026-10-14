import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="urlbox",
    version="1.0.7",
    author="Urlbox",
    author_email="support@urlbox.io",
    description="Official Python client for the Urlbox API",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/urlbox/urlbox-python",
    project_urls={
        "Bug Tracker": "https://github.com/urlbox/urlbox-python/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
    install_requires=["requests>=2.32.4,<3", "validators>=0.18.2"],
)
