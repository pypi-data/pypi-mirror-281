from setuptools import setup, find_packages

setup(
    name='AntiMALReverse',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'networkx',
        'scikit-learn',
        'torch',  # Ensure PyTorch is included
        'pefile',
    ],
    package_data={
        'AntiMALReverse': ['models/obfuscation_model.pth'],
    },
    author='Joy Mondal',
    author_email='contact.joymondal@gmail.com',
    description='A novel reverse engineering toolkit for detecting and analyzing malware.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/codewithjoymondal',  # Replace with your GitHub repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
