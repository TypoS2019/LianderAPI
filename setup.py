from setuptools import setup

setup(
    name='AllianderAPIFramework',
    version='v1.0',
    packages=['application', 'application.core', 'application.core.utils', 'application.core.errors',
              'application.core.logging', 'application.routers', 'application.routers.interventie', 'application.routers.scenario',
              'application.routers.overige', 'application.routers.gebeurtenis','application.routers.project', 'application.routers.gebruiker', 'application.versions'],
    url='',
    license='',
    author='Team Kobe',
    author_email='info@oose-kobe.nl',
    description='Alliander REST API skeleton', install_requires=['prometheus_client']
)
