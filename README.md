<h1 align="center">BDX Converter</h1>
<h3 align="center">一个免费开源的 BDX 文件解析器</h3>
<br/>
<p align="center">
<img src="https://forthebadge.com/images/badges/built-with-love.svg">
<p>

[GitHub: Happy2018new]: https://img.shields.io/badge/GitHub-Happy2018new-00A1E7?style=for-the-badge
[GitHub: Inotart]: https://img.shields.io/badge/GitHub-Inotart-00A1E7?style=for-the-badge
[Bilibili: EillesWan]: https://img.shields.io/badge/Bilibili-%E5%87%8C%E4%BA%91%E9%87%91%E7%BE%BF-00A1E7?style=for-the-badge
[python]: https://img.shields.io/badge/python-3.9-AB70FF?style=for-the-badge
[release]: https://img.shields.io/github/v/release/EillesWan/Musicreater?style=for-the-badge
[license]: https://img.shields.io/badge/LICENSE-MIT-228B22?style=for-the-badge

[![][GitHub: Happy2018new]](https://github.com/Happy2018new)<br/>
[![][GitHub: Inotart]](https://github.com/Inotart)<br/>
[![][Bilibili: EillesWan]](https://space.bilibili.com/397369002/)<br/>
[![][python]](https://www.python.org/)<br/>
[![][license]](LICENSE)<br/>







# 目录
- [目录](#目录)
- [`BDX Converter`](#bdx-converter)
- [注意事项](#注意事项)
  - [兼容性](#兼容性)
  - [签名](#签名)
- [快速上手](#快速上手)
- [🐍 Pypi Packages](#-pypi-packages)
- [第三方依赖](#第三方依赖)
- [特性](#特性)
- [什么是 `BDX` 文件](#什么是-bdx-文件)
- [关于 `PhoenixBuilder`](#关于-phoenixbuilder)
- [待办列表](#待办列表)
- [其他](#其他)





# `BDX Converter`
`BDX Converter` 是一个轻量化的纯 `Python` 实现，它提供了基本的 `BDX` 解析、反解析、`JSON` 可视化和反可视化功能。 





# 注意事项
## 兼容性
- 版本 `1.1.14` 不兼容之前的所有版本
- 版本 `1.1.11` 在签名功能上不兼容之前的版本
- 版本 `1.1.0` 不兼容之前的所有版本
- 版本 `1.0.16` 在可视化和反可视化字典方面不兼容之前的版本



## 签名
- `BDX` 文件格式是由 `PhoenixBuilder` 所定义，签名 `BDX` 文件则必须具备 `PhoenixBuilder` 账户
- 由于一些原因，您需要自行获取 `签名` 时的 `Prove` 和 `PrivateSigningKey` ，以下展示了获取方法。有关本项目实现的签名功能，请见 [`BDXConverter/Converter/Signature.py`](https://github.com/TriM-Organization/BDXConverter/blob/main/BDXConverter/Converter/Signature.py)

  ```python
  """
  import ecdsa
  
  peer = ecdsa.SigningKey.generate(ecdsa.NIST384p)
  verifyingKey = peer.get_verifying_key()
  publicKey = verifyingKey.to_string().hex()
  
  print(publicKey)
  # publicKey(...)
  """
  # Generate a new public key to send an auth request to the PhoenixBuilder Auth server
  
  
  """
  The address of PhoenixBuilder Auth server is wss://api.fastbuilder.pro:2053
  """
  # Address of PhoenixBuilder Auth server
  
  
  """
  Golang Structure
  type AuthRequest struct {
      Action         string `json:"action"`
      ServerCode     string `json:"serverCode"`
      ServerPassword string `json:"serverPassword"`
      Key            string `json:"publicKey"`
      FBToken        string
  }

  Python Dictionary
  {
      'action': 'phoenix::login',
      'serverCode': ...,
      'serverPassword': ...,
      'publicKey': ...,
      'FBToken': ...
  }
  """
  # Send an auth request to the PhoenixBuilder Auth server
  # Note: Must use GZIP to compress data when sending


  """
  Python Dictionary
  {
      'chainInfo': ...,
      'code': ...,
      'message': ...,
      'privateSigningKey': ...,
      'prove': ...
  }
  """
  # The response of the PhoenixBuilder Auth server when the request succeeds
  ```
  - `PhoenixBuilder Auth Server` 使用了 `Cloudflared` 来代理(加速)它的 `Websocket` 服务器，因此您无法直接使用 `Python` 的 `Websocket` 库来连接此服务器。目前尚且未找到对应的解决办法，一个替代方案是使用 `Golang` 下的 `Websocket` 库与 `PhoenixBuilder Auth Server` 建立连接
    - 其他帮助信息另见 https://github.com/huashengdun/webssh/issues/141





# 快速上手
您可以利用 [`BDXConverter/Converter/FileOperation.py`](https://github.com/TriM-Organization/BDXConverter/blob/main/BDXConverter/Converter/FileOperation.py) 中已提供的 `4` 个函数来完成 `BDX` 文件和 `JSON` 文件的相关操作。 





# 🐍 Pypi Packages
我们已将此存储库以 `BDXConverter` 的名字上载到 `Pypi` ，您可以通过 `pip install BDXConverter` 快速安装。

访问 [📦 BDXConverter on Pypi](https://pypi.org/project/BDXConverter) 以了解有关此库的更多信息。

我们配置了自动化 `CD/CI 工作流` ，因此如果您是本项目的 `协作者` ，您可以通过更改 `version` 文件或通过手动触发的方式启动工作流，它会自动编译本项目并将将其上载到 `Pypi` 中。

_[注：我们建议您在 `Python 3.10` 及以上的版本使用本项目，`3.7` 及以下的版本已不再受到 `Python` 的维护和更新]_





# 第三方依赖
本项目使用了 `brotli, nbtlib` 和 `pycryptodome` 总计 `3` 个第三方库，您可以通过在 `终端` 逐一地执行以下命令以安装它们。

```
pip install brotli
pip install nbtlib
pip install pycryptodome
```





# 特性
您可以从 [`BDXConverter/General/Pool.py`](https://github.com/TriM-Organization/BDXConverter/blob/main/BDXConverter/General/Pool.py) 查看本项目已支持的全部 `BDX` 操作符。

实际上，我们将每一个操作符都转换为了 `Python` 下已被实例化的类，并且每个类都有以下属性。 

```python
class GeneralClass:
    """
    Any operation of the BDX file will inherit this class
    """

    def __init__(self) -> None:
        self.operationNumber: int
        self.operationName: str

    def Marshal(self, writer: BytesIO) -> None:
        """
        Marshal Self@GeneralClass into the writer(io object)
        """
        ...

    def UnMarshal(self, buffer: BytesIO) -> None:
        """
        Unmarshal the buffer(io object) into Self@GeneralClass
        """
        ...

    def Loads(self, jsonDict: dict) -> None:
        """
        Load data from jsonDict:dict
        """
        ...

    def Dumps(self) -> dict:
        """
        Convert Self@GeneralClass into the basic dictionary
        """
        ...
```

因此，通过 `Marshal` 和 `UnMarshal` 函数，`BDX Converter` 可以自由的将 `二进制数据` 转换为 `Python Class` ，亦或转换回去。 <br/>
而 `Loads` 和 `Dumps` 分别支持了把只带有基本数据类型的字典转换为 `Python Class` 亦或转换回去的功能。 

目前 `BDX Converter` 支持了所有的操作符，包括但不限于 `Operation 5, Operation 13, Operation 40` 和 `Operation 41` ，当前也包含 `签名` 相关的功能。





# 什么是 `BDX` 文件
`PhoenixBuilder` 是一个用于 `网易我的世界中国版 · 基岩版租赁服` 的商业化快速建造器，而 `BDX` 文件则是此建造器用于存储 `Minecraft` 建筑结构的 `私有文件格式` 。

如果您希望解析 `BDX` 文件，敬请参阅 [`bdump-cn.md`](https://github.com/LNSSPsd/PhoenixBuilder/blob/main/doc/bdump/bdump-cn.md) 。





# 关于 `PhoenixBuilder`
- 您可以通过此链接访问 `PhoenixBuilder` 的存储库
   - [`PhoenixBuilder`](https://github.com/LNSSPsd/PhoenixBuilder/)
- 您可以通过下述链接访问 `PhoenixBuilder` 的相关网站
   - [`用户中心`](https://uc.fastbuilder.pro/)
   - [`官方网站`](https://fastbuilder.pro/)





# 待办列表
- [ ] `API` 文档
- [x] 支持与 `签名` 有关的功能
- [ ] 可以将得到的 `Python Class` 进一步解析为建筑结构
- [ ] 可以自由地转换 `BDX` 和其他建筑文件格式





# 其他
本项目依照 [`MIT LICENSE`](./LICENSE) 许可证进行许可和授权。