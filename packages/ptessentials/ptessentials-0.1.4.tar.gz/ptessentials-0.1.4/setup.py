from setuptools import setup, find_packages

setup(
    name='ptessentials',
    version='0.1.4',
    description='A PixelTycoons Dev Best Friend.',
    url='https://github.com/funkaclau',
    author='funkaclau',
    packages=find_packages(),
    install_requires=[
        "waxnftdispatcher==0.3.5",
        "waxtion>=0.1.5",
        "waxfetcher",
        "pyntelope",
        "aanft"
    ],
    include_package_data=True
)
