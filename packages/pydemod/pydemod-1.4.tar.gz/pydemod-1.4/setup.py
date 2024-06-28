from setuptools import setup, find_packages # type: ignore

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
        name="pydemod",
        version="1.4",
        author="kuba201",
        description='Python modulation library',
        long_description=readme,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        url="https://flerken.zapto.org:1115/kuba/Pydemod",
        install_requires=[],
        project_urls={
            'Source': 'https://flerken.zapto.org:1115/kuba/Pydemod',
        },
        keywords=['radiodatasystem','rds','amss','am'],
        classifiers= [
            "Intended Audience :: Education",
            "Intended Audience :: Telecommunications Industry",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.10",
        ]
)