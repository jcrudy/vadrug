from setuptools import setup, find_packages
import versioneer
setup(name='vadrug',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      author='Jason Rudy',
      author_email='jcrudy@gmail.com',
      url='https://github.com/jcrudy/vadrug',
      package_data={'vadrug': ['resources/*']},
      packages=find_packages(),
      requires=['pandas', 'xlrd', 'clinvoc']
     )