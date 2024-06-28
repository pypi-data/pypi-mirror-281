from setuptools import setup, find_packages

setup(
    name="arifETS",  # Ensure the name is unique
    version="0.1.1",
    author="Arif Mustafa",
    author_email="arifmustafa75@gmail.com",
    description="A simple expense tracking package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/arifETS",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=[
        'matplotlib',
    ],
     entry_points={
        'console_scripts': [
            'arifETS=arifETS.expense_management:main',
        ],
    },
    python_requires='>=3.6',
)
