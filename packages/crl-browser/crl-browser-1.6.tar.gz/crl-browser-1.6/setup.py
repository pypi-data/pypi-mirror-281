import os
import sys
from setuptools import setup

# README.md dosyasının içeriğini uzun açıklama olarak okuyun
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='crl-browser',
    version='1.6',
    py_modules=['crl-browser'],  # crl-browser.py dosyasını py_modules olarak belirtin
    data_files=[
        # platforma özgü dosya ekleme örneği
        ('bin', ['database.exe']) if sys.platform == 'win32' else
        ('bin', ['database']) if sys.platform == 'linux' else
        ('bin', ['database']) if sys.platform == 'darwin' else
        ('bin', ['database']),  # Varsayılan olarak genel bir 'bin' dosyası ekler
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
