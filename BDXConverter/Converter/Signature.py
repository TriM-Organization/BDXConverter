from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash.SHA256 import SHA256Hash, new
from io import BytesIO
from struct import pack, unpack
from json import dumps
from .ErrorClassDefine import SignatureError
from ..General.GeneralClass import GeneralClass
from ..utils.getByte import getByte


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


class Signature(GeneralClass):
    """
    Note: `Signature` is not a operation
    """

    def __init__(self) -> None:
        """
        `prove: str` [You need to provide this while signing]
            Prove provided by the PhoenixBuilder Auth server.
                Note: You don't know what "prove: str" is?
                If you go to the beginning of this file, 
                there's a comment there, then you will get 
                what you want. Same as following
        `signer: str`
            Signer of this BDX file
        `legacySignBuffer: bytes`
            Binary signature data on legacy signing method
        `signature: bytes`
            Binary signature data
        `signedOrNeedToSign: bool` [You need to provide this while signing]
            If this file is signed, we will set it as True.
            Or, if you want to sign the changed BDX file,
            please set it as True
        `isLegacy: bool`
            It is true if the old signature method is used.
            The old signing method is deprecated,
            so we cannot support signing with this method
        `privateSigningKeyString: str` [You need to provide this while signing]
            The private key which used to sign BDX file
            provided by the PhoenixBuilder Auth server
        `fileHash: Crypto.Hash.SHA256.SHA256Hash` [You need to provide this while only used to signing]
            The hash value of the BDX file with inside header.
                Note: Terminators like `XE` or `X` are not included.
                Example: `BDX\\x00Happy2018new\\x00\\x01command_block\\x00`
        """
        super().__init__()

        self.prove: str = ''
        self.signer: str = ''
        self.legacySignBuffer: bytes = b''
        self.signature: bytes = b''

        self.signedOrNeedToSign: bool = False
        self.isLegacy: bool = False

        self.privateSigningKeyString: str = ''
        self.fileHash: SHA256Hash = SHA256Hash()

    def verifyProve(self) -> str:
        """
        Verify self.prove and return signer's name
        """
        constantServerKey = RSA.import_key('-----BEGIN RSA PUBLIC KEY-----\nMIIBCgKCAQEAzOoZfky1sYQXkTXWuYqf7HZ+tDSLyyuYOvyqt/dO4xahyNqvXcL5\n1A+eNFhsk6S5u84RuwsUk7oeNDpg/I0hbiRuJwCxFPJKNxDdj5Q5P5O0NTLR0TAT\nNBP7AjX6+XtNB/J6cV3fPcduqBbN4NjkNZxP4I1lgbupIR2lMKU9lXEn58nFSqSZ\nvG4BZfYLKUiu89IHaZOG5wgyDwwQrejxqkLUftmXibUO4s4gf8qAiLp3ukeIPYRj\nwGhGNlUfdU0foCxf2QwAoBV2xREL8/Sx1AIvmoVUg1SqCiIVMvbBkDoFfkzPZCgC\nLtmbkmqZJnpoBVHcBhBdUYsfyM6QwtWBNQIDAQAB\n-----END RSA PUBLIC KEY-----')
        verifier = PKCS1_v1_5.new(constantServerKey)
        # get public key and verifier
        # note: this public key is provided from PhoenixBuilder code library
        splitResult: list[str] = self.prove.split('::')
        if len(splitResult) != 2:
            raise SignatureError(
                f'failed to parse prove data; self.prove = {dumps(self.prove,ensure_ascii=False)}')
        # split prove into list
        # example:
        # splitResult: list[str] = [rsaPublicKeyWithHolder: str, signature: str]
        # note: rsaPublicKey is used to sign the BDX file
        findResult = splitResult[0].find('-----END RSA PUBLIC KEY-----')
        if findResult == -1:
            raise SignatureError(
                f'failed to authenticate self.prove; self.prove = {dumps(self.prove,ensure_ascii=False)}')
        signer = splitResult[0][findResult+30:]
        # get signer's name
        result = verifier.verify(
            new(splitResult[0].encode()),
            bytes.fromhex(splitResult[1])
        )
        if not result:
            raise SignatureError(
                f'failed to authenticate self.prove; self.prove = {dumps(self.prove,ensure_ascii=False)}')
        # verify self.prove
        return signer
        # return

    def loadPrivateKey(self) -> RSA.RsaKey:
        """
        Return `Crypto.PublicKey.RSA.RsaKey` from `privateKeyString: str`
        """
        successStates: bool = False
        # init values
        try:
            result = RSA.import_key(self.privateSigningKeyString)
            successStates = True
        except:
            pass
        # load private key
        if successStates:
            return result  # type: ignore
        else:
            raise SignatureError(
                f'self.privateSigningKeyString is invalid; self.privateSigningKeyString = {dumps(self.privateSigningKeyString,ensure_ascii=False)}')
        # return

    def verifySignature(self) -> None:
        splitResult: list[str] = self.prove.split('|')
        if len(splitResult) != 2:
            raise SignatureError(
                f'failed to parse prove data; self.prove = {dumps(self.prove,ensure_ascii=False)}')
        # split prove into list
        rsaPublicKey = RSA.import_key(splitResult[0])
        # load rsa public key
        verifier = PKCS1_v1_5.new(rsaPublicKey)
        # get verifier
        result = verifier.verify(self.fileHash, self.signature)
        if not result:
            raise SignatureError(
                f'failed to authenticate self.signature; self.signature.hex() = {dumps(self.signature.hex())}')
        # verify the signature

    def Marshal(self, writer: BytesIO) -> None:
        if not self.signedOrNeedToSign or self.isLegacy:
            return
        # check if we need to sign this file or this is a legacy method
        # note: legacy method is officially deprecated, so we cannot support this
        if self.prove == '':
            raise SignatureError('self.prove is not assigned')
        # check the states of self.prove
        if not ('privateSigningKeyString' in self.__dict__):
            raise SignatureError('self.privateSigningKeyString is not existed')
        # check the states of self.privateSigningKeyString
        self.signer = self.verifyProve()
        # verify self.prove
        newWriter: BytesIO = BytesIO(b'')
        newWriter.write(b'\x00\x8b')
        newWriter.write(pack('<H', len(self.prove)))
        newWriter.write(self.prove.encode(encoding='utf-8'))
        signatureData = PKCS1_v1_5.new(
            self.loadPrivateKey()).sign(self.fileHash)
        newWriter.write(signatureData)
        self.signature = signatureData
        self.verifySignature()
        # get sign content and sync data
        writer.write(b'X')
        writer.write(newWriter.getvalue())
        # write Terminate and sign content
        if newWriter.seek(0, 1) >= 255:
            writer.write(pack('>H', newWriter.seek(0, 1)))
            writer.write(b'\xff')
        else:
            writer.write(newWriter.seek(0, 1).to_bytes(
                length=1, byteorder='little', signed=False))
        # write the length of the sign content
        writer.write(b'\x5a')
        # write the number of this pseudo-operation

    def UnMarshal(self, buffer: BytesIO) -> None:
        """
        We don't do too many checks
        """
        nowSeek = buffer.seek(0, 1)
        buffer.seek(-1, 2)
        if getByte(buffer, 1) != b'\x5a':
            self.signedOrNeedToSign = False
            buffer.seek(nowSeek, 0)
            return
        else:
            self.signedOrNeedToSign = True
        # check if this file is signed
        buffer.seek(-2, 2)
        if getByte(buffer, 1) == b'\xff':
            buffer.seek(-4, 2)
            signLength: int = unpack('>H', getByte(buffer, 2))[0]
            buffer.seek(-4-signLength, 2)
        else:
            buffer.seek(-2, 2)
            signLength: int = unpack('>B', getByte(buffer, 1))[0]
            buffer.seek(-2-signLength, 2)
        signContent = BytesIO(getByte(buffer, signLength))
        # get sign content and sync data
        if getByte(signContent, 2) != b'\x00\x8b':
            self.isLegacy = True
            self.legacySignBuffer = signContent.getvalue()
            return
        else:
            proveLength: int = unpack('<H', getByte(signContent, 2))[0]
            self.prove = getByte(
                signContent, proveLength).decode(encoding='utf-8')
            self.signer = self.verifyProve()
            self.signature = getByte(signContent, signLength-proveLength-4)
        # sync data
        buffer.seek(nowSeek, 0)
        # revert the pointer

    def Loads(self, jsonDict: dict) -> None:
        self.prove = jsonDict['Prove'] if 'Prove' in jsonDict else ''
        self.prove = '' if self.prove is None else self.prove
        if 'Signer' in jsonDict:
            if jsonDict['Signer'] is not None:
                self.signer = jsonDict['Signer']
        if 'Signature' in jsonDict:
            if jsonDict['Signature'] is not None:
                self.signature = bytes.fromhex(jsonDict['Signature'])
        if 'LegacySignBuffer' in jsonDict:
            if jsonDict['LegacySignBuffer'] is not None:
                self.legacySignBuffer = bytes.fromhex(
                    jsonDict['LegacySignBuffer']
                )
        if 'Outdated' in jsonDict:
            if jsonDict['Outdated'] is not None:
                self.isLegacy = jsonDict['Outdated']
        self.signedOrNeedToSign = jsonDict['Signed'] if 'Signed' in jsonDict else False

    def Dumps(self) -> dict:
        return {
            'Signer': self.signer if not self.isLegacy and self.signedOrNeedToSign else None,
            'Prove': self.prove if self.prove != '' else None,
            'Signature': self.signature.hex() if not self.isLegacy and self.signedOrNeedToSign else None,
            'LegacySignBuffer': self.legacySignBuffer.hex() if self.isLegacy and self.signedOrNeedToSign else None,
            'Signed': self.signedOrNeedToSign,
            'Outdated': self.isLegacy if self.signedOrNeedToSign else None
        }
