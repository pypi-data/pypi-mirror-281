from setuptools import setup, find_packages


import urllib.request

url = "https://raw.githubusercontent.com/d2cml-ai/synthdid.py/main/Readme.md"
response = urllib.request.urlopen(url)
long_description = response.read().decode("utf-8")

setup(
    dependency_links=[],
    install_requires=[
        "appdirs==1.4.3",
        "attrs==19.1.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "black==19.3b0; python_version >= '3.6'",
        "click==7.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "contourpy==1.0.7",
        "cycler==0.11.0",
        "fonttools==4.39.0",
        "importlib-resources==5.12.0",
        "kiwisolver==1.4.4",
        "matplotlib==3.7.1",
        "numpy==1.23.5",
        "packaging==23.0",
        "pandas==1.5.3",
        "patsy==0.5.3",
        "pillow==9.4.0",
        "pipenv-setup==2.0.0",
        "pipfile==0.0.2",
        "pyparsing==3.0.9",
        "python-dateutil==2.8.2",
        "pytz==2022.7.1",
        "scipy==1.10.1; python_version >= '3.10' and python_version < '3.12' and platform_system != 'Windows' or platform_machine != 'x86'",
        "six==1.16.0",
        "statsmodels==0.13.5",
        "toml==0.10.0",
        "zipp==3.15.0",
    ],
    name="synthdid",
    author="D2CML Team, Alexander Quispe, Rodrigo  Grijalba, Jhon Flores, Franco Caceres",
    version="0.10.1",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="causal-inference",
    url="https://github.com/d2cml-ai/synthdid.py",
    license="MIT",
    description="Synthdid",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Scientific/Engineering",
    ],
)

