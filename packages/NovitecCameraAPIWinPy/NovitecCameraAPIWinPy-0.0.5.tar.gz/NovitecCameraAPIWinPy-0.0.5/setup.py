from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='NovitecCameraAPIWinPy',
    version='0.0.5',
    packages=find_packages(),
    include_package_data=True,
    description='Python wrapper for Novitec Camera API (Windows only)',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='kkomadev',
    author_email='kkomadev@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 2 - Pre-Alpha",
    ],
    python_requires='>=3.10.11',
    package_data={
        'NovitecCameraAPIWinPy': ['_internal/*.dll'],
    },
)
