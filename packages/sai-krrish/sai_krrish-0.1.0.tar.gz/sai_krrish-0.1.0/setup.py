from setuptools import setup, find_packages

setup(
    name='sai_krrish',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    author='Sai krrish',
    author_email='psaikrishnan99@gmail.com',
    description='A simple greeter library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/my_library',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
