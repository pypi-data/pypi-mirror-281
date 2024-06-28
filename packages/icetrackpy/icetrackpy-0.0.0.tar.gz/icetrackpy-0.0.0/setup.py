import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='icetrackpy',
    author='Martin THIRIET',
    author_email='martin.thiriet1@gmail.com',
    description='particule tracking module for elmer ice output files and post treatment',
    keywords='ice_modeling, elmer_ice, particule_tracking',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gricad-gitlab.univ-grenoble-alpes.fr/mecaiceige/internship/stage_matin_2024/',
    project_urls={
        'Documentation': 'https://gricad-gitlab.univ-grenoble-alpes.fr/mecaiceige/internship/stage_matin_2024/',
        'Bug Reports':
        'https://gricad-gitlab.univ-grenoble-alpes.fr/mecaiceige/internship/stage_matin_2024/',
        'Source Code': 'https://gricad-gitlab.univ-grenoble-alpes.fr/mecaiceige/internship/stage_matin_2024/',
        # 'Funding': '',
        # 'Say Thanks!': '',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    # install_requires=['Pillow'],
    extras_require={
        'dev': ['check-manifest'],
        # 'test': ['coverage'],
    },
    # entry_points={
    #     'console_scripts': [  # This can provide executable scripts
    #         'run=examplepy:main',
    # You can execute `run` in bash to run `main()` in src/examplepy/__init__.py
    #     ],
    # },
)