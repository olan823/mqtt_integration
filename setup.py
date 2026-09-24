from setuptools import find_packages, setup


setup(
    name="mqtt_integration",
    version="0.1.4",
    description="ERPNext Desk entry point for the Starchart MQTT web console",
    author="Skychip",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[],
)
