from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='opai2',
    version='0.0.1',
    author='Eugene Evstafev',
    author_email='chigwel@gmail.com',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/chigwell/opai',
    packages=find_packages(),
    install_requires=[
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)