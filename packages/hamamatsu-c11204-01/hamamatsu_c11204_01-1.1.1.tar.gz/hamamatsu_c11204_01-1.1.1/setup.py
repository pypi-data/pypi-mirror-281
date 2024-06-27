import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'hamamatsu_c11204_01',
    version = '1.1.1',
    author = 'Martín Galan <mng94@live.com.ar>, Cesar Moreno <morenocesar.0098@gmail.com>',
    description = 'Package created to work with a power supply module for MPPC Hamamatsu C11204-01',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://gitlab.ahuekna.org.ar/labo_6y7/2024/galan_moreno/software.git',
    install_requires = [
        'pyserial'
    ],
    packages = setuptools.find_packages(include=['hamamatsu_c11204_01','hamamatsu_c11204_01.*']),
    include_package_data = True,
    python_requires='>=3.6'
)