from setuptools import setup, find_package

setup(name='mail_noti',
      version='0.1',
      url='https://github.com/yellowfang/mail_noti.git',
      license='MIT',
      author='Lee JunYeol',
      author_email='shie44167@gmail.com',
      description='notify using mail',
      packages=find_packages(exclude=['tests']),
      zip_safe=False)
