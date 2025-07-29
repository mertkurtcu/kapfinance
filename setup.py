from setuptools import setup, find_packages

setup(
    name='kapfinance',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    author='Mert Kurtçu',
    author_email='mert@example.com',
    description='KAP verileriyle finansal analiz araçları',
    long_description='Uzun açıklama buraya gelecek.',
    long_description_content_type='text/plain',
    url='https://github.com/kullaniciadi/kapfinance',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',

    entry_points={
    'console_scripts': [
        'kapfinance=kapfinance.cli:main',
    ],
}, 
)