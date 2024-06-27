from setuptools import setup, find_packages

setup(
    name='ANTIMALONE',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'keras',
        'networkx',
        'scikit-learn',
    ],
    author='Joy mondal',
    author_email='contact.joymondal@gmail.com',
    description='A novel antivirus engine with advanced static analysis algorithms.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/codewithjoymondal',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
