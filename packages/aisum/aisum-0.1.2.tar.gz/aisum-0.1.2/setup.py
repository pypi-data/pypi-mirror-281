from setuptools import setup, find_packages

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    name='aisum',
    version='0.1.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'requests',
        'openai'
    ],
    entry_points={
        'console_scripts': [
            'aisum = aisum.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
