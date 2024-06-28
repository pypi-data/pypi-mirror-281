from setuptools import setup, find_packages
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


with open("README.md", "r") as fh:
    long_desc= fh.read()

setup(
    name='lbx_toolkit',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'locale',
        'time',
        'threading',
        'logging',
        'pathlib',
        'psycopg2',
        'pandas',
        'numpy',
        'http.server',
        'urllib.parse',
        'msal',
        'requests',
        'selenium',
        'webdriver-manager'
    ],
    license='MIT License',
    description='Biblioteca de ferramentas LBX S/A',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author='Cristiano P. Ferrari',
    author_email='boxferrari@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
