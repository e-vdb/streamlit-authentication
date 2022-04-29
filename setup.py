import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

    name="streamlit-authentication",

    version="1.0.3",

    author="e-vdb",

    author_email="emelinevanderbeken@gmail.com",

    description="Manage a database to save user and password that can access streamlit web apps",

    long_description=long_description,

    long_description_content_type="text/markdown",

    url="https://github.com/e-vdb/streamlit-authentication",

    packages=setuptools.find_packages(),

    classifiers=[

        "Programming Language :: Python :: 3",

        "License :: OSI Approved :: MIT License",

        "Operating System :: OS Independent",

    ],
    install_requires=["pandas>=1.3.0", "SQLAlchemy>=1.4.35", "psycopg2-binary>=2.9.3", "passlib>=1.7.4", "streamlit>=1.7.0"],
    python_requires='>=3.9',

)
