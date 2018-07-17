"""Setup file for handling packaging and distribution."""
from setuptools import setup

__version__ = "1.0.0"

setup(
    name="recursive_decorator",
    version=__version__,
    description="",
    license="MIT",
    author="ronen-y",
    url="https://github.com/ronen-y/recursive_decorator",
    keywords="decorator recursive recursive_decorator recursive-decorator",
    install_requires=["codetransformer"],
    extras_require={
        "dev": ["flake8", "pylint",
                "pytest", "pytest-cov",
                "mock"]
    },
    packages=["recursive_decorator"],
    python_requires=">=3,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*",
    package_data={'': ['*.xls', '*.xsd', '*.json',
                       '*.css', '*.xml', '*.rst']},
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    zip_safe=False
)