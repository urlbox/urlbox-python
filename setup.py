import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="urlbox",
    version="1.0.6",
    author="Urlbox",
    author_email="support@urlbox.io",
    description="Official Python client for the Ulrbox API",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/urlbox/urlbox-python",
    project_urls={
        "Bug Tracker": "https://github.com/urlbox/urlbox-python/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=["requests==2.26.0", "validators==0.18.2"],
)
