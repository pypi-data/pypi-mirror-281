from pathlib import Path

import setuptools

# The long_description field is used by PyPI when you publish a package,
# to build its project page.
long_description = Path("README.md").read_text(encoding="utf-8")
version = Path("orchestapicli/_version.py").read_text(encoding="utf-8")
about = {}
exec(version, about)

setuptools.setup(
    name="tto-cli",
    description="CLI for TTO",
    keywords="TTO",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=about["__version__"],
    license="Apache 2.0",
    author="Rick Lamers",
    author_email="rick@orchest.io",
    url="https://github.com/TapTarget/TTO",
    project_urls={
        "Documentation": ("https://docs.orchest.io/en/stable/"),
        "Source Code": ("https://github.com/TapTarget/TTO/tree/master/orchest-cli"),
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Utilities",
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        "click>=8.0.0",  # implies python >= 3.6
        "requests",  # required by kubernetes as well
    ],
    entry_points={
        "console_scripts": [
            "ttoa=orchestapicli.cli:cli",
        ],
    },
    # It is reasonable to follow:
    # https://numpy.org/neps/nep-0029-deprecation_policy.html#support-table
    python_requires=">=3.8",
)
