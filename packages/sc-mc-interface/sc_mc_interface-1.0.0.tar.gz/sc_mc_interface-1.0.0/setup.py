from setuptools import setup,find_packages

setup(
    name='sc_mc_interface',
    version='1.0.0',
    description='mc查询会话conversation接口',
    author='dyy',
    packages=find_packages(),
    install_requires=["requests>=2.0.0"]
)