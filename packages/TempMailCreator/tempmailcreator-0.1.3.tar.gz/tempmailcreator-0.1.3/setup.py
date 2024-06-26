from setuptools import setup, find_packages

setup(
    name='TempMailCreator',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'requests'

    ],
    author='70L0-0j0',
    author_email='70L0-0j0@lamia.xyz',
    description='Library for creating and managing temporary email accounts with mail.tm API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/70L0-0j0/Mailer',  # URL del repositorio del proyecto
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Versión mínima de Python
)
