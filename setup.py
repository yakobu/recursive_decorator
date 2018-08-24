"""Setup file for handling packaging and distribution."""
from setuptools import setup

__version__ = "1.0.1"

setup(
    name="recursive_decorator",
    version=__version__,
    long_description=open("README.rst").read(),
    description="Decorator to apply given decorator recursively on functions",
    license="MIT",
    author="yakobu",
    author_email="ronenya4321@gmail.com",
    url="https://github.com/ronen-y/recursive_decorator",
    keywords="decorator recursive recursive_decorator recursive-decorator",
    install_requires=["codetransformer", "cached-property"],
    packages=["recursive_decorator"],
    extras_require={
        'dev': [
            'mock',
            'flake8',
            'pytest',
            'pytest-cov',
        ],
    },
    package_data={'': ['*.xls', '*.xsd', '*.json',
                       '*.css', '*.xml', '*.rst']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: POSIX',
        'Topic :: Software Development :: Pre-processors',
    ],
    zip_safe=False
)