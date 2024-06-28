from distutils.core import setup
from setuptools import find_packages
import sys

with open("README.rst", "r",encoding="utf-8") as f:
  long_description = f.read()

with open("license", "r") as f:
  license = f.read()

# 定义依赖项
install_requires = [
    # 所有平台通用的依赖
    'importlib_resources; python_version < "3.7"',  # 对Python版本小于3.7的用户，添加importlib_resources依赖
    'proxy_tools',
    'bottle',
    'cryptography',
]

# 根据平台条件添加依赖
if sys.platform == "win32":
    install_requires.append('pythonnet')

if sys.platform == "darwin":
    install_requires.extend([
        'pyobjc-core',
        'pyobjc-framework-Cocoa',
        'pyobjc-framework-Quartz',
        'pyobjc-framework-WebKit',
        'pyobjc-framework-Security',
    ])

if sys.platform in ("openbsd6", "linux"):
    install_requires.extend([
        'PyQt5',
        'pyqtwebengine',
        'QtPy',
    ])

setup(name='WebviewRevise',  # 包名
      version='0.0.2',  # 版本号
      description='这是一个 pywebview 修改版本',
      long_description=long_description,
      long_description_content_type='text/x-rst',
      author='CC',
      author_email='3204604858@qq.com',
      url='https://github.com/r0x0r/pywebview',
      install_requires=install_requires,
      license='BSD-3-Clause',
      packages= find_packages(),
      platforms=["win10","win11"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Topic :: Software Development :: Libraries'
      ],
      )
