from setuptools import setup

setup(
    name='autofig',
    version='0.0.1',
    description='Automization program for figures',
    author='KimGeonUng',
    author_email='saywooong@gmail.com',
    packages=[
        'autofig',
    ], 
    entry_points={
        'console_scripts': [
            'autofig=autofig.main:main',
        ],
    },
    include_package_data=True,
)
