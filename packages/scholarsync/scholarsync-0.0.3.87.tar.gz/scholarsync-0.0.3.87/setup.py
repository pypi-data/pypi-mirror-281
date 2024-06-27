from setuptools import setup, find_packages
setup(
    name='scholarsync',
    version='0.0.3.87',
    packages=find_packages(),
    author='Amit',
    author_email='idonthaveemail@mail.com',
    description='The Literature mining and processing utility',
    long_description=open('README.md').read(),
    package_data={'scholarsync': ['data/*']},
  # include_package_data=True,  # Include all package data

    install_requires=[
        'biopython',
        'requests',
        'beautifulsoup4',
        'PyPDF2',
	'numpy',
	'plotly',
	'lxml',
	'spacy>=3.7.5',  # Adjust version as necessary
        'beautifulsoup4',  # bs4 is part of beautifulsoup4 package
        'pandas',
	'scikit-learn',
	
	
    ],
    entry_points={
        'console_scripts': [
            'scholarsync = scholarsync.aio:main',
        ],
    },
)
