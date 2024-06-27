from setuptools import setup, find_packages

setup(
    name='bsodrop',
    version='0.0.2',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'bsodrop': ['bst.dll'],
    },
    install_requires=[],
    author='xinyc',
    author_email='csecinside@proton.me',
    description='A simple python repository for calling bsod inside your code.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ohmiu/bsod',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
    ],
    python_requires='>=3.6',
)
