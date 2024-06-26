from setuptools import setup, find_packages

setup(
    name='intellibot',
    version='0.5',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'requests',
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'intellibot=intellibot.cli:cli',
        ],
    },
    author="Pawan Pinsara",
    author_email="1pawanpinsara@gmail.com",
    description="A CLI tool for interacting with intellibot API",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/PinsaraPerera/intellihack_research_agent.git",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
