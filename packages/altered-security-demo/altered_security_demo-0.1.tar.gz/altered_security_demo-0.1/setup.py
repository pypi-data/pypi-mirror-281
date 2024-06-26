from setuptools import setup, find_packages

setup(
    name='altered_security_demo',  # Unique project name
    version='0.1',
    packages=find_packages(),
    description='A demonstration package for altered security',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://example.com',  # Replace this with a valid URL
    license='MIT',
    install_requires=[
        # List your package dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
