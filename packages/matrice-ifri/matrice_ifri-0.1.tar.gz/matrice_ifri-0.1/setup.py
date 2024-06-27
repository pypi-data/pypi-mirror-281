from setuptools import setup, find_packages

setup(
    name='matrice_ifri',
    version='0.1',
    packages=find_packages(),
    description='Un simple package pour les calculs matriciels',
    author='TITO Lucien',
    author_email='titovlucien@gmail.com',
    url='https://github.com/mrcryptsie/matrice_ifri', 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
