from setuptools import setup, find_packages

setup(
    name='greenreq',
    version='0.1.2',
    author='Tamim Ahmed',
    author_email='admin@teamgreenxd.com',
    description='A Python package for making HTTP requests',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mr-green-143/greenreq',
    license='MIT',
    packages=find_packages(),
    package_data={'greenreq': ['green_requests.so']},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[],
)
