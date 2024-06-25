from setuptools import setup

setup(name='ons_sds_publisher_demo',
      version='0.0.1',
      description='A demo of GCP publisher service',
      url='',
      author='Isaiah Lai',
      author_email='isaiah.lai@ons.gov.uk',
      license='MIT',
      packages=['ons_sds_publisher_demo'],
      install_requires=[
          'google-cloud-pubsub',
      ],
      zip_safe=False)