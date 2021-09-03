import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="carma-schema",
    version="0.3.0",
    author="Brian Miles",
    author_email="brian.miles@louisiana.edu",
    description="CARMA schema tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/watershedfloodcenter/carma-schema/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'jsonschema',
        'dataclasses-json==0.5.4'
    ],
    tests_require=[
    ],
    entry_points={
        'console_scripts': [
            'carma-validator=carma_schema.cmd.validator:main',
    ]},
    include_package_data=True,
    zip_safe=False
)
