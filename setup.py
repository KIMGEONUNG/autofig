from setuptools import setup

setup(
    name='autofig',
    version='0.0.1',
    description='Automatic gridy image figure generator',
    author='KimGeonUng',
    author_email='saywooong@gmail.com',
    packages=[
        'autofig',
    ], 
    entry_points={
        'console_scripts': [
            'aufig=autofig.main:main',
        ],
    },
    include_package_data=True,
)
