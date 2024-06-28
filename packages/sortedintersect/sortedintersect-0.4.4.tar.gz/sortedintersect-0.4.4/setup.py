from setuptools import setup, find_packages, Extension

ext_modules = [
    Extension("sortedintersect.sintersect",
              ["sortedintersect/sintersect.pyx"],
              language="c++",
              extra_compile_args=["-std=c++17"])
]

setup(
    version='0.4.4',
    name='sortedintersect',
    description="Interval intersection for sorted query and target intervals",
    author="Kez Cleal",
    author_email="clealk@cardiff.ac.uk",
    packages=find_packages(),
    ext_modules=ext_modules,
)