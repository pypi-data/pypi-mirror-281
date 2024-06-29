from setuptools import setup, find_packages

setup(
    name='ponytail-agents',
    version='0.1.8',
    description='ponytAIl: Polymorphic Orchestration of Networked Youthful, Adaptable Intelligence with Language.',
    author='The Pioneer',
    url='https://github.com/thepioneerjp/ponytAIl',
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'openai',
        'anthropic',
        'google-generativeai',
        'python-dotenv',
        'pytest',
        'flute-llm'
    ],
    package_data={
        '': ['*.txt', '*.md', '*.json', '*.csv', '*.yaml', '*.yml', "LICENSE"],
        'ponytAIl': ['**/*'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        "console_scripts": [
            "ponytail=ponytAIl.main:main",
        ],
    },
)