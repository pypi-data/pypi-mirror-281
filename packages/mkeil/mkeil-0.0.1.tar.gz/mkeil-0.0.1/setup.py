from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='mkeil',
  version='0.0.1',
  description='a library for send email',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Mehran Karimi',
  author_email='axelox9@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='email sender',
  packages=find_packages(),
  install_requires=['smtplib']
)
