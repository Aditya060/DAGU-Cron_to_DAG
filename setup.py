from setuptools import setup, find_packages

setup(
    name='dagu-cron',
    version='0.1.0',
    description='A tool to convert CRONTAB jobs to DAGU DAGs',
    author='Aditya Thapliyal',
    author_email='adityathapliyal0607@example.com',
    license='MIT',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'click>=8.0',
        'pyyaml>=5.4',
    ],
    entry_points={
        'console_scripts': [
            'dagu-cron = dagu_cron_Aditya07.main:cli'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    project_urls={
        'Homepage': 'https://github.com/Aditya060/DAGU-Cron_to_DAG',
        'Repository': 'https://github.com/Aditya060/DAGU-Cron_to_DAG',
        'Documentation': 'https://github.com/Aditya060/DAGU-Cron_to_DAG/wiki',
    },
)
