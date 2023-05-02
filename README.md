<h1 align="center">BDX Converter</h1>
<h3 align="center">一个免费开源的 BDX 文件解析器</h3>
<br/>
<p align="center">
<img src="https://forthebadge.com/images/badges/built-with-love.svg">
<p>

[GitHub: Happy2018new]: https://img.shields.io/badge/GitHub-Happy2018new-00A1E7?style=for-the-badge
[python]: https://img.shields.io/badge/python-3.8-AB70FF?style=for-the-badge
[release]: https://img.shields.io/github/v/release/EillesWan/Musicreater?style=for-the-badge
[license]: https://img.shields.io/badge/LICENSE-MIT-228B22?style=for-the-badge

[![][GitHub: Happy2018new]](https://github.com/Happy2018new)<br/>
[![][python]](https://www.python.org/)<br/>
[![][license]](LICENSE)<br/>





# `BDX Converter`
`BDX Converter` 是一个轻量化的实现，它提供了基本的 `BDX` 解析、反解析、`JSON` 可视化和反可视化功能。 

# 快速上手
您可以利用 [`BDXConverter/Converter/Converter.py`](https://github.com/TriM-Organization/BDXConverter/blob/main/BDXConverter/Converter/Converter.py) 中已提供的 `4` 个函数来完成 `BDX` 文件和 `JSON` 文件的相关操作。 
使用下述命令快速安装吧
```shell
pip install BDXConverter
```
> 我们建议您在 Python 3.10及其以上版本使用他,3.7及其以下版本Python不再维护更新

# 项目依赖
本项目使用了 `brotli` 和 `nbtlib` 总计 `2` 个第三方库，您可以通过在 `终端` 逐一地执行以下命令以安装它们。

```
pip install brotli
pip install nbtlib
```

# 项目特性
您可以从 [`BDXConverter/General/Pool.py`](https://github.com/TriM-Organization/BDXConverter/blob/main/BDXConverter/General/Pool.py) 查看本项目已支持的全部 `BDX` 操作符。

实际上，我们将每一个操作符都转换为了 `Python` 下已被实例化的类，并且每个类都有以下属性。 

```python
class GeneralClass:
    """
    Any Operation eration of the BDX file will inherit this class
    """

    def __init__(self) -> None:
        self.operationNumber: int
        self.operationName: str

    def Marshal(self, writer: BytesIO) -> None:
        """
        Marshal GeneralClass into the writer
        """
        ...

    def UnMarshal(self, buffer: BytesIO) -> None:
        """
        Unmarshal the buffer(io object) into GeneralClass
        """
        ...

    def Loads(self, jsonDict: dict) -> None:
        """
        Convert jsonDict:dict into GeneralClass
        """
        ...

    def Dumps(self) -> dict:
        """
        Convert GeneralClass into basic dictionary
        """
        return self.__dict__
```

因此，通过 `Marshal` 和 `UnMarshal` 函数，`BDX Converter` 可以自由的将 `二进制数据` 转换为 `Python Class` ，亦或转换回去。 <br/>
而 `Loads` 和 `Dumps` 分别支持了把只带有基本数据类型的字典转换为 `Python Class` 亦或转换回去的功能。 

目前 `BDX Converter` 支持了所有的操作符(不含签名功能)，包括但不限于 `Operation 5, Operation 13, Operation 40` 和 `Operation 41` 。 

# 待办列表
- [ ] `API` 文档
- [ ] 支持与 `签名` 有关的功能
- [ ] 可以将得到的 `Python Class` 进一步解析为建筑结构
- [ ] 可以自由地转换 `BDX` 和其他建筑文件格式

# 其他
本项目依照 [`MIT LICENSE`](./LICENSE) 许可证进行许可和授权。
