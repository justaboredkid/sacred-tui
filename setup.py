from setuptools import setup

with open("README.md", "r") as fh:
    setup(
        name='sacred_tui',
        version='0.2.1',
        long_description=fh.read(),
        long_description_content_type='text/markdown',
        description='Python library for ASCII art import and TUI development',
        url='https://github.com/justaboredkid/sacred',
        test_suite='tests',
        author='justaboredkid',
        author_email='29010153+justaboredkid@users.noreply.github.com',
        license='GNU GPLv3',
        packages=['sacred'],
        install_requires=['blessed', 'cursor'],
        classifiers=[
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Programming Language :: Python :: 3',
            'Topic :: Software Development :: User Interfaces',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
        zip_safe=False,
        entry_points={
            'console_scripts': ['asciigen = asciigen:main'],
        })
