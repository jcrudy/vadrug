from setuptools import setup, find_packages

setup(name='vadrug',
      version='0.1',
      author='Jason Rudy',
      author_email='jcrudy@gmail.com',
      url='https://github.com/jcrudy/vadrug',
      package_data={'vadrug': ['resources/*']},
      packages=find_packages(),
      requires=['pandas', 'xlrd', 'clinvoc']
     )