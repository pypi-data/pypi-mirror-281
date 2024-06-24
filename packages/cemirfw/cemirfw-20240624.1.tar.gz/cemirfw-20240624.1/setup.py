from setuptools import setup, find_packages

setup(
    name='cemirfw',
    version='20240624.1',
    description='AllInOne Framework for Python/PyPy',
    author='MusluY.',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    author_email='musluyuksektepe@gmail.com',
    url='https://github.com/muslu/cemirfw',
    packages=find_packages(),
    install_requires=['tornado'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
