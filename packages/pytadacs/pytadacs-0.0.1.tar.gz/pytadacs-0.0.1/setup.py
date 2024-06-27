from setuptools import setup, find_packages

setup(
    name="pytadacs",  # Replace with your package name
    version="0.0.1",  # Initial release version
    author="Rafael A. García",  # Replace with your name
    author_email="rafel.garcia@ecea.fr",  # Replace with your email
    description="pytadacs: Python for Tess Astroseismic and DynAmiC Studies",  # Short description
    classifiers=[  # Classifiers help users find your project by categorizing it
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify the Python versions you support
    install_requires=[  # List of dependencies
        "numpy",
    ],
)
