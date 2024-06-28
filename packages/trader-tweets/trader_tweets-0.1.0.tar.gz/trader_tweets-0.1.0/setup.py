from setuptools import setup, find_packages

setup(
    name='trader_tweets',
    version='0.1.0',
    author='Will H-S',
    author_email='whardwicksmith@gmail.com',
    description='A module for processing and analyzing trader tweets.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourgithub/trader_tweets',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
    install_requires=[
        'openai~=0.18.1',
        'requests~=2.27.1',
        'setuptools~=62.3.2',
        'google-cloud==0.34.0',
        'google-cloud-logging==3.9.0',
        'google-cloud-secret-manager==2.11.1',
        'google-cloud-firestore==2.6.0',
        'google-api-python-client~=2.50.0',
        'pytest~=5.4.1',
        'parameterized~=0.8.1',
        'diskcache~=5.4.0',
        'requests_oauthlib~=1.3.1',
        'backtrader~=1.9.76',
        'pandas~=1.5.3',
        'python-binance~=1.0.12',
        'pytz~=2022.7.1',
        'functions-framework==3.*',
        'twscrape~=0.11.1'
    ]
)