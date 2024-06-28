from setuptools import setup, find_packages

setup(
    name='SA_Framework',
    version='0.5',  # Incremented version number
    packages=find_packages(include=['SA_Framework', 'SA_Framework.*']),
    install_requires=[
        'robotframework-seleniumlibrary >=6.1.1',
        'pycryptodome >=3.19.0',
        'pymongo >=4.5.0',
        'robotframework-pabot >=2.16.0',
        'ratelimit >=2.2.1'
    ],
    package_data={
        'SA_Framework': ['Framework_Common_Resources/*.robot'],
        'SA_Framework': ['Custom_Library/*.py'],
        'SA_Framework': ['CustomeKeywords/*.py'],
        'SA_Framework': ['HubConfiguration/*.robot'],
        'SA_Framework': ['VaultUtilities/*.robot'],
        'SA_Framework': ['VeevaWorkFlowPreReqAPIs/*.py'],
    },
    description="A Spotline's Framework",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Sukumar Kutagulla',
    author_email='sukumar@spotline.com',
    url='https://github.com/Spotline-Inc/SA_Framework',  # Update with your project's URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
