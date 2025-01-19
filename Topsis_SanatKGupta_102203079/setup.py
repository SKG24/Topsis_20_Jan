from setuptools import setup, find_packages

setup(
    name='Topsis_SanatKGupta_102203079',
    version='0.1.0',
    author="Sanat Kumar Gupta",
    author_email="your-email@example.com",  # Replace with your email
    description="A Python library for TOPSIS method for MCDM problems",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SKG24/Topsis_20_Jan",  # Replace with your GitHub repo
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
    ],
    entry_points={
        'console_scripts': [
            'topsis = Topsis_SanatKGupta_102203079.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)