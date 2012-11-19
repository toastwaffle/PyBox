from distutils.core import setup

setup(
    name='PyBox',
    version='0.1a',
    author='Samuel Littley',
    author_email='samuel.littley@toastwaffle.com',
    packages=['libpybox', 'pybox_daemon', 'pybox_server'],
    scripts=['bin/pyboxd', 'bin/pyboxsd'],
    url='https://www.toastwaffle.com/pybox',
    license='LICENSE.txt',
    description='An open-source, self hosted dropbox replacement.',
    long_description=open('README.txt').read(),
    install_requires=[
        "watchdog >= 0.6.0",
        "boto >= 2.6.0",
        "path.py >= 2.4.1",
        "sqlalchemy >= 0.8.0"
    ]
)
