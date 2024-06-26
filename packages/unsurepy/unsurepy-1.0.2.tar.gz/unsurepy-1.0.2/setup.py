from setuptools import setup, find_packages

setup(
    name='unsurepy',
    version='1.0.2',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'requests',
    ],
    author='Meddah Abdallah',
    author_email='meddah.abdellah.spcx@gmail.com',
    description='A utility package that leverages the capabilities of llms to allow working with values with undertermined format',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MeddahAbdellah/py-unsure',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)