from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='GraphToMermaid',
    version='0.1.2',
    author='huynd2210',
    description='Convert any graph like structure to a mermaid and vice versa',
    long_description_content_type='text/markdown',
    url='https://github.com/huynd2210/GraphToMermaid',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'mermaid-builder',
        're'
        # add other dependencies
    ],
)
