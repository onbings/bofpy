from setuptools import setup, find_packages

setup(
    name='BofPy',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
        'tkhtmlview>=0.2.0',
    ],
    entry_points={
        'console_scripts': [
            'BofPy=BofPy.Bof_Init:main',  # Optional: If you have command-line scripts
        ],
    },
    author='onbings',
    author_email='onbings@gmail.com',
    description='BofPy is a python fork of BofStd C++ library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/onbings/bofpy',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
)
