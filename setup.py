from distutils.core import setup

setup(name='finite-fault-product',
      version='0.1dev',
      description='USGS finite fault product creater.',
      include_package_data=True,
      author='Heather Schovanec',
      author_email='hschovanec@usgs.gov',
      url='',
      packages=['fault',
                'fault/io',
                'product'],
      scripts=['bin/deleteproduct',
               'bin/getproduct',
               'bin/sendproduct']
      )
