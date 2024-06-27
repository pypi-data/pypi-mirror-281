import setuptools

setuptools.setup(
    name="dp-launching-app",
    version="0.1.0-alpha.1",
    author="",
    author_email="",
    description="",
    long_description="",
    long_description_content_type="text/plain",
    url="",
    entry_points={
        "console_scripts": [
            "launching-app = dp.launching.cli.commands.launching:main",
        ]
    },
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.8",
    install_requires=[
        "fastapi",
        "uvicorn",
        "wcmatch",
        "colorama",
        "pydantic>=1.10.5",
        "pydantic-cli-pydantic-v2-compatible==4.4.0-alpha.1",
        "kubernetes>=28.1.0",
    ],
    extras_require={
        "dev": [
            "pytest",
        ],
    }
)
