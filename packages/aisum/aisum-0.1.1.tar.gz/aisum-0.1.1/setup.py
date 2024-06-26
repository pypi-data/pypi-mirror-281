from setuptools import setup, find_packages

setup(
    name='aisum',
    version='0.1.1',
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
)
