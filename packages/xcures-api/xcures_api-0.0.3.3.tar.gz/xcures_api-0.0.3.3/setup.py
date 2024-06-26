from setuptools import setup, find_packages

setup(
    name="xcures_api",
    version="0.0.3.3",
    packages=find_packages(),
    description="Python wrapper for the xcures REST api, found here https://partner.xcures.com/api-docs .",    
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",    
    author="John Major",
    author_email="iamh2o@gmail.com",
    license='MIT',
    url="https://github.com/RCRF/xcures_api",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10'
    ],
    scripts=[
    ],
    keywords="xcures api bioinformatics patient records",
    include_package_data=True,
    package_data={
    },
    python_requires=">=3.10",
    install_requires=["pytest", "requests", "yaml_config_day", "pytz", "ipython", "twine"], 
)
 
 
