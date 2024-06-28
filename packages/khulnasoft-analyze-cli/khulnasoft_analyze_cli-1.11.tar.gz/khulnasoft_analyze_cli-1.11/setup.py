import os

from setuptools import setup


def rel(*xs):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *xs)


with open(rel('khulnasoft_analyze_cli', '__init__.py'), 'r') as f:
    version_marker = '__version__ = '
    for line in f:
        if line.startswith(version_marker):
            _, version = line.split(version_marker)
            version = version.strip().strip("'")
            break
    else:
        raise RuntimeError('Version marker not found.')

install_requires = [
    'click==7.1.2',
    'khulnasoft-analyze-sdk>=1.15.2,<2'
]
tests_require = [
    'pytest==6.1.2',
    'responses==0.17.0'
]

with open('README.md') as f:
    long_description = f.read()

setup(
    name='khulnasoft-analyze-cli',
    version=version,
    description='Client library for Khulnasoft cloud service',
    author='Khulnasoft Labs ltd.',
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ],
    keywords='khulnasoft',
    packages=['khulnasoft_analyze_cli'],
    install_requires=install_requires,
    tests_require=tests_require,
    entry_points='''
        [console_scripts]
        khulnasoft-analyze=khulnasoft_analyze_cli.cli:main_cli
    ''',
    license='Apache License v2',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.8',
    zip_safe=False
)
