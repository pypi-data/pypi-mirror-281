from setuptools import setup, find_packages

setup(
    name='batch_processor_custom',
    version='0.1.1',
    author='Vitor',
    author_email='',
    packages=find_packages(),
    description='Um pacote para processamento em lote usando MongoDB',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'pymongo',
        'uuid'
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
