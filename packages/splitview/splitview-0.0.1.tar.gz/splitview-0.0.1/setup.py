from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='splitview',
    version='0.0.1',
    author='Kenneth Leung',
    author_email='tbd@example.com',
    description='Simple tool for viewing the split text of your documents',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your-repo',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
