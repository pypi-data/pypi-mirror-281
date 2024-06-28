from setuptools import setup, find_packages

setup(
    name='meta-llama-3-yarn',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        # Add your project's dependencies here
        # e.g., 'numpy', 'requests'
        "transformers==4.41.2"
    ],
    url="https://github.com/MeetKai/meta-llama-3-yarn",
    author="Jeffrey Fong",
    author_email="jeffrey.fong@meetkai.com",
    description="YaRN Implementation compatible with HuggingFace Transformers",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)