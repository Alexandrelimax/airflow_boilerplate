from setuptools import setup

setup(
    name='dataflow-example',
    version='0.0.1',
    install_requires=[
        'apache-beam[gcp]==2.53.0',
    ],
    packages=['pipeline'],
    package_dir={'pipeline': 'pipeline'}
)
