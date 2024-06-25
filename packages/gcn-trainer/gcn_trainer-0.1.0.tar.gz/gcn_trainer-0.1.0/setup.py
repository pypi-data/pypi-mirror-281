from setuptools import setup, find_packages

setup(
    name='gcn_trainer',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'torch',
        'torchmetrics',
        'tqdm',
    ],
    author='Ye Yuan',
    author_email='yuanyuan125@icloud.com',
    description='A package for training GCN models with regularization following https://github.com/Zaehyeon2/FDGNN-Fraud-Address-Detection-on-Ethereum-using-Graph-Neural-Network',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yuanye126/FDGNNImplementation',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
