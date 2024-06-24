from setuptools import setup


def pre_install():
    # f = open('README.md', 'r')
    # text = f.read()
    text = "#Amoo Sina Lion Package"
    return text


setup(
    name="amoo_sina_lion",
    version="1.0.0",
    author="Sina Hosseini",
    description="A test package for pydeploy students",
    long_description=pre_install(),
    requires=[],
    author_email="sshosseinivaez@gmail.com",
    packages=["amoo_sina_lion"]
)
