from setuptools import setup, find_packages

setup(
    name='givemehelp',
    version='0.71',
    packages=find_packages(),
    install_requires=[
        'openai',
        'boto3',
        'google-generativeai',
        'spacy'
    ], 
    entry_points={
        "console_scripts":[
            "givemehelp = givemehelp:retreiveSecretKey",
        ],
    },
)
