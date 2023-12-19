# bofpy
Python companion lib based on c++ BofStd

bofpy/
|-- bofpy/
|   |-- __init__.py
|   |-- module1.py
|   |-- module2.py
|-- setup.py
|-- README.md
|-- LICENSE
|-- .gitignore
|-- other_files...

setup.py:
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

.gitignore:
__pycache__
dist/
build/
*.egg-info/
*.pyc
*.pyo
*.pyd

tagging release:
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0


C:\pro\github\bofpy> pip install git+https://github.com/onbings/bofpy.git@v0.1.0

https://adamj.eu/tech/2019/03/11/pip-install-from-a-git-repository/#:~:text=It's%20quite%20common%20to%20want,install%20it%20directly%20via%20Git.

Yes, you can host a personal Python package on GitHub and use `pip` to install it. Here's a general guide on how to do it:

1. **Create a GitHub Repository:**
   - Create a new repository on GitHub where you will host your Python package. Initialize it with a README if you want.

2. **Create Your Python Package:**
   - Organize your Python code into a package with the necessary structure, including a `setup.py` file. The `setup.py` file is crucial for packaging and distribution.

   ```python
   from setuptools import setup

   setup(
       name='your-package-name',
       version='0.1.0',
       packages=['your_package'],
       install_requires=[
           # List your dependencies here
       ],
   )
   ```

3. **Commit and Push:**
   - Commit your code to the GitHub repository and push it.

4. **Tagging Releases:**
   - Create releases on GitHub and tag them with version numbers (e.g., v0.1.0). This step is essential for pip to be able to install specific versions.

5. **Install Your Package Using Pip:**
   - Install your package using `pip` by specifying the GitHub repository and the version you want to install.

   ```bash
   pip install git+https://github.com/your-username/your-repo.git@v0.1.0
   ```

   Alternatively, you can install the latest version directly from the main branch:

   ```bash
   pip install git+https://github.com/your-username/your-repo.git
   ```

   If you want to install directly from the master branch, you can use:

   ```bash
   pip install git+https://github.com/your-username/your-repo.git@master
   ```

Remember to replace `your-username`, `your-repo`, and other placeholders with your actual GitHub username, repository name, and package details.

Keep in mind that if your package becomes more widely used, you may want to consider publishing it to the Python Package Index (PyPI) for easier installation by the broader Python community.


python setup.py sdist
pip install path/to/your-library-name-1.0.0.tar.gz