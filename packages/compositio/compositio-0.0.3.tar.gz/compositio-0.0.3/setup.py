import os
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call

VERSION = '0.0.3' 
DESCRIPTION = 'the idea of assembling parts into a unified structure'
CHROMEDRIVER_URL = "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip"

def download_chromedriver():
    if not os.path.exists('chromedriver'):
        check_call(['wget', CHROMEDRIVER_URL])
        check_call(['unzip', 'chromedriver_linux64.zip'])
        os.remove('chromedriver_linux64.zip')

class PostDevelopCommand(develop):
    def run(self):
        download_chromedriver()
        develop.run(self)

class PostInstallCommand(install):
    def run(self):
        download_chromedriver()
        install.run(self)

setup(
        name="compositio", 
        version=VERSION,
        description=DESCRIPTION,
        packages=find_packages(),
        url='https://github.com/ricklentz/compositio',
        include_package_data=True,
    package_data={
        'your_package_name': ['chromedriver'],
    },
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)
