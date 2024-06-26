from setuptools import setup, find_packages

setup(
    name='kails',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'kails = kails.kails:main'
        ],
    },
    install_requires=[
        'watchdog',
        'pywebview'
    ],
        classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    author='hxoreyer',
    author_email='17396909632@163.com',
    description='a cli for pywebview',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hxoreyer/kails',
)
