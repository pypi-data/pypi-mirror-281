import os
from setuptools import setup

# README.md dosyasının içeriğini uzun açıklama olarak okuyun
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='crl-browser',
    version='0.1.5', 
    py_modules=['crl-browser'],  # crl-browser.py dosyasını py_modules olarak belirtin
    install_requires=[
        'requests',
        'psycopg2',
        'PyQt6',
        'crl-client',  # Burada crl-client modülünü ekledim
    ],
    entry_points={
        'console_scripts': [
            'crl-browser = crl_browser:run_app',  # crl_browser modülünde run_app fonksiyonunu giriş noktası olarak belirtin
        ],
    },
    package_data={},  # package_data boş olarak belirtilmiştir (veri dosyası yoksa)
    python_requires='>=3.10',  # Minimum Python sürümü belirtilmiştir
    description='CRL Browser - PyQt6 Based browser',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
