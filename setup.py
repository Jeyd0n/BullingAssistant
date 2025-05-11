from setuptools import setup, find_packages
from typing import List


def parse_requirements(filename: str) -> List[str]:
    '''
    
    '''
    with open(filename, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    

setup(
    name='OCR_Unistroy',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[parse_requirements('requirements.txt')],
    entry_points={
        'console_scripts': [
            'process_document=main:main',
        ],
    },
    author='v.polukhin',
    description='CLI-инструмент для обработки документов с OCR и классификацией',
    python_requires='>=3.11.9',
)
