from setuptools import setup, find_packages

setup(
    name="setuptools_pep660",
    version="0.1.3",
    description="An experimental replacement for 'setup.py develop'",
    long_description="Implements a PEP 517 + PEP 660 backend",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Archiving :: Packaging",
    ],
    author="Daniel Holth",
    author_email="dholth@fastmail.fm",
    maintainer="Frost Ming",
    maintainer_email="mianghong@gmail.com",
    url="https://github.com/frostming/setuptools_pep660",
    keywords="setuptools pep660 pep517",
    license="MIT",
    packages=find_packages("src"),  # returns ["setuptools_pep660"]
    package_dir={
        "": "src"
    },  # "setuptools_pep660": "src/setuptools_pep660" would work but not as well
    install_requires=["setuptools>=42,<61", "wheel"],
    entry_points={
        "distutils.commands": [
            "editable_wheel = setuptools_pep660.editable_wheel:editable_wheel"
        ]
    },
    include_package_data=True,
    zip_safe=False,
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*",
)
