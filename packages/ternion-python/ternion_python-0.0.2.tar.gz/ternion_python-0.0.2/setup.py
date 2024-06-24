from setuptools import setup, find_packages

VERSION = "0.0.2"
DESCRIPTION = "Python packaged for Ternion board"
LONG_DESCRIPTION = "Python packaged for Ternion board"

setup(
    name="ternion_python",
    version=VERSION,
    author="Santi Nuratch",
    author_email="santi.inc.kmutt@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        "pyserial",
        "colorlog",
        "customtkinter",
    ],
    keywords=["python", "first package"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)

# from setuptools import setup, find_packages

# setup(
#     name="ternion_python",
#     version="0.0.1",
#     author="Santi Nuratch",
#     author_email="santi.inc.kmutt@gmail.com",
#     description="Python packaged for Ternion board",
#     packages=find_packages(),
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     python_requires=">=3.6",
# )
