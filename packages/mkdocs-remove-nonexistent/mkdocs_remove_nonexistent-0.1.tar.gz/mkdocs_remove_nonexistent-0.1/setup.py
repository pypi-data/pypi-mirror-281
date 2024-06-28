from setuptools import setup, find_packages

setup(
    name='mkdocs-remove-nonexistent',
    version='0.1',
    author="ziqinyeow",
    author_email="",
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'mkdocs-remove-nonexistent=src:RemoveNonExistentPagesPlugin'
        ]
    }
)