from setuptools import setup, find_packages

setup(
    name='rnaernie',
    version='0.1.4',
    packages=find_packages(exclude=['ss_token/']),
    install_requires=[
        # List your package dependencies here
        # 'somepackage>=1.0',
    ],
    include_package_data=True,
    description='RNAErnie2',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/CatIIIIIIII/RNAErnie2',  # Replace with your repo URL
    author='WANG Ning',
    author_email='wangning.roci@gmail.com',
    license='MIT',  # Choose your license
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
