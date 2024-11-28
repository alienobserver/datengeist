from setuptools import setup
import os

dir_name = os.path.dirname(__file__)
relative_path = 'requirements.txt'
reqs_filename = os.path.join(dir_name, relative_path)

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

with open(reqs_filename, 'r') as file:
    file_content = file.read()
    reqs = file_content.splitlines()

setup(
    name='datengeist',
    version='0.0.1',
    description='Application for easy understanding of unstructured data',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/alienobserver/datengeist',
    author='Narek Aristakesyan',
    author_email='aristakesyannarek11@gmail.com',
    license='Apache License 2.0',
    package_dir={"datengeist":"datengeist"},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'datengeist=datengeist.start:main',
        ]
    },
    install_requires=reqs,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.11',
    ],
)
