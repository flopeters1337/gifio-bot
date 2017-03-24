from setuptools import setup

setup(name='gifio-bot',
      version='0.1',
      description='A twitter bot that punctuates tweets with GIFs.',
      url='https://github.com/flopeters1337/gifio-bot',
      author='Florian Peters',
      author_email='fl0wryan@hotmail.com',
      license='MIT',
      packages=['gifio-bot'],
      install_requires=[
          'python-twitter'
          'giphypop'
      ],
      zip_safe=False)
