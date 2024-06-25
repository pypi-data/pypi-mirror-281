from setuptools import setup, find_packages

setup(
    name='green_lib',
    version='1.0.0',
    description='A Python package for making HTTP requests using green_requests.so',
    author='Tamim Ahmed',
    author_email='admin@teamgreenxd.com',
    url='https://github.com/MR-GREEN-143/green_lib',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
