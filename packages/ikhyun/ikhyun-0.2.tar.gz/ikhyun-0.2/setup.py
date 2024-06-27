from setuptools import setup, find_packages

setup(
    name='ikhyun',
    version='0.2',
    author="Ikhyun Cho",
    author_email="ikhyun_cho@tmax.co.kr",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "transformers",
        "torch",
        "tqdm",
        "overrides",
        "numpy",
        "dataclasses; python_version<'3.7'",
    ],
)
