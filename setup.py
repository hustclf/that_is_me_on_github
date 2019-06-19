import setuptools
from that_is_me_on_github.config import VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="that_is_me_on_github",
    version=VERSION,
    author="hustclf",
    author_email="hustclf@gmail.com",
    description="A Python cli for collecting and showing your github contributions as simple and detailed as possible.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hustclf/that_is_me_on_github",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "that_is_me_on_github = that_is_me_on_github.main:that_is_me_on_github"
        ]
    },
    install_requires=[
        "atomicwrites==1.3.0",
        "attrs==19.1.0",
        "certifi==2019.3.9",
        "chardet==3.0.4",
        "Click==7.0",
        "Deprecated==1.2.5",
        "idna==2.8",
        "importlib-metadata==0.17",
        "more-itertools==7.0.0",
        "packaging==19.0",
        "pluggy==0.12.0",
        "py==1.8.0",
        "PyGithub==1.43.7",
        "PyJWT==1.7.1",
        "pyparsing==2.4.0",
        "pytest==4.6.2",
        "requests==2.22.0",
        "six==1.12.0",
        "urllib3==1.25.3",
        "wcwidth==0.1.7",
        "wrapt==1.11.1",
    ],
)
