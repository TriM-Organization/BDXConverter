# 有关 `BDX` 文件签名的说明
> 文档作者: [_@Inotart_](https://github.com/Inotart)

~~签名的实现可参考 <https://github.com/CMA2401PT/BDXWorkShop>~~ _[已失效/目标 API 总是返回空值]_

本扩展库现已支持与 `签名` 相关的功能。 

如果您打算实现相同的功能，另见 [`func SignBDXNew(fileHash []byte, privateKeyString string, cert string) ([]byte, error)`](https://github.com/LNSSPsd/PhoenixBuilder/blob/main/fastbuilder/bdump/utils.go#L117)

FB的签名需要准备 `FBToken` ，即一个 `PhoenixBuilder` 账号的登录凭证。
