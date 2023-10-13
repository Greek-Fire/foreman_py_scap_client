from setuptools import setup, find_packages

setup(
    name='foreman_scap_client',
    version='0.1.0',  # your version
    packages=find_packages(),
    install_requires=[
        # your dependencies
    ],
    entry_points={
        'console_scripts': [
            'foreman_scap_client=foreman_scap_client.__main__:main',
        ],
    },
    # other metadata
    author='Your Name',
    author_email='your.email@example.com',
    description='A Python version of ForemanScapClient',
    # ...
)

