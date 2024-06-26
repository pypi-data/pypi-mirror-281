from setuptools import setup
import os

VERSION = "0.0.0a0"

def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="nitsa",
    description="Placeholder",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Florents Tselai",
    url="https://github.com/Florents-Tselai/nitsa",
    entry_points="""
        [console_scripts]
        nitsa=nitsa.cli:cli
    """,
    project_urls={
        "Issues": "https://github.com/Florents-Tselai/nitsa/issues",
        "CI": "https://github.com/Florents-Tselai/nitsa/actions",
        "Changelog": "https://github.com/Florents-Tselai/nitsa/releases",
    },
    license="MIT License",
    version=VERSION,
    packages=["nitsa"],
    install_requires=[ "click", "setuptools", "pip"],
    extras_require={"test": ["pytest", "pytest-cov", "black", "ruff", "click"]},
    python_requires=">=3.7"
)
