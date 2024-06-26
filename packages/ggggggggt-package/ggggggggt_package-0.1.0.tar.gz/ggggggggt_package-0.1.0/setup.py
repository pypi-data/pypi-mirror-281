from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    install_requires = [line.strip() for line in f if line.strip()]

setup(
    name='ggggggggt_package',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A description of your package',
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=install_requires,
    classifiers=[  # 分类器，用于描述项目
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11.9',  # 支持的 Python 版本
    include_package_data=True,  # 包含包中的静态文件
    package_data={  # 包含特定包的静态文件
        '': ['*.json', '*.md'],
    }
)
