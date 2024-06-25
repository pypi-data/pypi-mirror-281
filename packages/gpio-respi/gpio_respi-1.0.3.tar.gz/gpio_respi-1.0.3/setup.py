import setuptools

package_name = "gpio_respi"

def upload():
    with open("README.md", "r") as fh:
        long_description = fh.read()
    with open('requirements.txt') as f:
        required = f.read().splitlines()

    setuptools.setup(
        name=package_name,
        version="1.0.3",
        author="zhubin",  # 作者名称
        author_email="zhu2000410@163.com",  # 作者邮箱
        description="respi_socket_gpio",  # 库描述
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://pypi.org/project/gpio_respi/",  # 库的官方地址
        packages=setuptools.find_packages(),
        data_files=["requirements.txt"],  # 库依赖的其他库
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
        install_requires=required,
    )


def main():
    try:
        upload()
        print("Upload success", )
    except Exception as e:
        raise Exception("Upload package error", e)


if __name__ == '__main__':
    main()