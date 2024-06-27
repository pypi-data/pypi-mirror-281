from setuptools import setup, find_packages

setup(
    name='SA_Framework',
    version='0.2',  # Incremented version number
    packages=find_packages(),
    install_requires=[
        'robotframework-seleniumlibrary',
        'seleniumlibrary',
        'pycryptodome',
        'pymongo',
        'robotframework-pabot',
        'pycrypto',
        'ratelimit'
    ],
    include_package_data=True,
    description="A Spotline's Framework",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Sukumar Kutagulla',
    author_email='your.email@example.com',
    url='https://github.com/Spotline-Inc/SA_Framework',  # Update with your project's URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
