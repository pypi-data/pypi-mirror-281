from setuptools import setup, find_packages

setup(
    name="EZ_project_creator",
    version="1.0.3",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "project_creator=project_creator.main:main",
        ],
    },
    author="Mark Friese",
    author_email="mark.friese.meng@gmail.com",
    description="A tool to create project structures with virtual environments and package installations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Mark-Friese/project_creator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
