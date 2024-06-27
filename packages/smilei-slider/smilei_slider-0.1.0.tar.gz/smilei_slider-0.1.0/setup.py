from setuptools import setup

setup(
    name='smilei_slider',
    version='0.1.0',
    py_modules=['smilei_slider'],
    install_requires=[
        'ipywidgets',
        'ipython',
        'matplotlib',
        'numpy',
    ],
    author='Ziming Huang',
    author_email='zh2422@ic.ac.uk',
    description='A package for showing sliders for smilei',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/mypackage',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)