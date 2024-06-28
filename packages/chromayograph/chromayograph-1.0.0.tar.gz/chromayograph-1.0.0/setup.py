from setuptools import setup, find_packages

setup(
    name='chromayograph',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'Flask',  # 根据你的项目需求添加依赖项
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'chromayograph=main:main',  # main.py 的入口函数
        ],
    },
    author='Zhao Xin Yue',
    author_email='zhaoxinyue@pku.edu.cn',
    description='A brief description of your project',
    url='https://github.com/yue000103/Chromatograph.git',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)
