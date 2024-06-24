from setuptools import setup, find_packages

setup(
    name='zfx',
    version='1.0.101',
    packages=find_packages(),
    include_package_data=False,
    author='zengfengxiang',
    author_email='424491679@qq.com',
    description='中国人自己的模块！ZFX是一个多功能的Python工具包,提供了各种实用工具和功能，包括网络请求、剪贴板操作、系统监控、网页自动化、系统操作、文本处理、文件操作等,无论是日常办公还是自动化脚本，ZFX都能为您提供便捷的解决方案，让您的编程体验更加愉快！',
    long_description="""
    免责声明:
    本模块是“按原样”提供的，没有任何明示或暗示的保证。在任何情况下，作者或版权持有者均不对因使用本模块而产生的任何索赔、损害或其他责任负责，无论是在合同、侵权或其他情况下。

    使用本模块即表示接受此免责声明。如果您不同意此免责声明的任何部分，请勿使用本模块。

    本模块仅供参考和学习用途，用户需自行承担使用本模块的风险。作者对因使用本模块而造成的任何直接或间接损害不承担任何责任。

    作者保留随时更新本免责声明的权利，恕不另行通知。最新版本的免责声明将在模块的最新版本中提供。
    """,
    url='',
    install_requires=[
        'requests',
        'pyperclip',
        'pystray',
        'psutil',
        'selenium',
        'mysql.connector',
        'pyinstaller',
        'openpyxl',
        'jsonpath',
        'extruct',
        'w3lib',
        'pyotp',
        # 添加其他依赖库
    ],
)
