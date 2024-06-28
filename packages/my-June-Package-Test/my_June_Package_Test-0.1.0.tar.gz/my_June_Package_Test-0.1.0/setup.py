from setuptools import setup, find_packages

setup(
    name='my_June_Package_Test',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List of dependencies
    ],
    author='Akash',
    author_email='your.email@example.com',
    description='A brief description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    #url='https://github.com/yourusername/my_package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
 
