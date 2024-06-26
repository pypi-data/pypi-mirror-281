from setuptools import setup, find_packages

setup(
    name='myguidlib',
    version='0.1',
    packages=find_packages(),
    description='A simple hello world library to generate GUIDs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/brainvs/myguidlib',
    author='brainvs',
    author_email='brainvs@brainvs.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
