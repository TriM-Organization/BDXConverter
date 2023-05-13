# 有关 `BDX` 文件签名的说明
> 文档作者: [_@Inotart_](https://github.com/Inotart)

在编写本文档时，该扩展库不支持签名。
~~签名的实现可参考 <https://github.com/CMA2401PT/BDXWorkShop>~~ _[已失效/目标 API 总是返回空值]_
签名的实现可参考 [`func SignBDXNew(fileHash []byte, privateKeyString string, cert string) ([]byte, error)`](https://github.com/LNSSPsd/PhoenixBuilder/blob/main/fastbuilder/bdump/utils.go#L117)

FB的签名需要准备 `FBToken` ，即一个 `PhoenixBuilder` 账号的登录凭证。
