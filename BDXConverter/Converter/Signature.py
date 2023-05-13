from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash.SHA256 import new
from Crypto.PublicKey import RSA
from io import BytesIO
from struct import pack, unpack
from .ErrorClassDefine import signatureError
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
# Generate a new public key to send a auth request to the romote server


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
                Note: You don't know what "Prove: str" is?
                If you go to the beginning of this file, 
                there's a comment there, then you will get 
                what you want. Same as follow
        `signer: str`
            Signer of this BDX file
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
        `BDXContentWithInsideHeader: io.BytesIO` [You need to provide this while only used to signing]
            The content of BDX file with inside file header
        """
        self.prove: str = ''
        self.signer: str = ''
        self.signature: bytes = b''

        self.signedOrNeedToSign: bool = False
        self.isLegacy: bool = False

        self.privateSigningKeyString: str = ''
        self.BDXContentWithInsideHeader: BytesIO = BytesIO(b'')

    def verificationProve(self) -> str:
        """
        Verify the validity of self.prove and return signer's name
        """
        constantServerKey = RSA.import_key('-----BEGIN RSA PUBLIC KEY-----\nMIIBCgKCAQEAzOoZfky1sYQXkTXWuYqf7HZ+tDSLyyuYOvyqt/dO4xahyNqvXcL5\n1A+eNFhsk6S5u84RuwsUk7oeNDpg/I0hbiRuJwCxFPJKNxDdj5Q5P5O0NTLR0TAT\nNBP7AjX6+XtNB/J6cV3fPcduqBbN4NjkNZxP4I1lgbupIR2lMKU9lXEn58nFSqSZ\nvG4BZfYLKUiu89IHaZOG5wgyDwwQrejxqkLUftmXibUO4s4gf8qAiLp3ukeIPYRj\nwGhGNlUfdU0foCxf2QwAoBV2xREL8/Sx1AIvmoVUg1SqCiIVMvbBkDoFfkzPZCgC\nLtmbkmqZJnpoBVHcBhBdUYsfyM6QwtWBNQIDAQAB\n-----END RSA PUBLIC KEY-----')
        verifier = PKCS1_v1_5.new(constantServerKey)
        # get publick key and verifier
        # note: this public key is provided from PhoenixBuilder code library
        splitResult: list[str] = self.prove.split('::')
        if len(splitResult) != 2:
            raise signatureError(
                f'failed to parse prove datas; self.prove = "{self.prove}"')
        # split prove into list
        # example:
        # splitResult: list[str] = [rsaPublicKeyWithHolder: str, signature: str]
        # note: rsaPublicKey is used to sign the BDX file
        findResult = splitResult[0].find('-----END RSA PUBLIC KEY-----')
        if findResult == -1:
            raise signatureError(
                f'the prove provided has not been verified and may be invalid; self.prove = "{self.prove}"')
        signer = splitResult[0][findResult+30:]
        # get signer's name
        result = verifier.verify(
            new(splitResult[0].encode()),
            bytes.fromhex(splitResult[1])
        )
        if result == False:
            raise signatureError(
                f'the prove provided has not been verified and may be invalid; self.prove = "{self.prove}"')
        # verification the prove
        return signer
        # return

    def loadPrivateKey(self) -> RSA.RsaKey:
        """
        Load privateKeyString:str into RSA.RsaKey and return it
        """
        successStates: bool = True
        try:
            return RSA.import_key(self.privateSigningKeyString)
        except:
            successStates = False
        if successStates == False:
            raise signatureError(
                f'the privateSigningKeyString provided is invalid; self.privateSigningKeyString = "{self.privateSigningKeyString}"')

    def Marshal(self, writer: BytesIO) -> None:
        if self.signedOrNeedToSign == False or self.isLegacy == True:
            return
        # check if need to sign this file or this is a legacy method
        # note: legacy method is officially deprecated so we cannot support this
        if not 'privateSigningKeyString' in self.__dict__:
            raise signatureError('self.privateSigningKeyString is not existed')
        # check the states of self.privateSigningKeyString
        self.signer = self.verificationProve()
        # verification the prove
        newWriter: BytesIO = BytesIO(b'')
        newWriter.write(b'\x00\x8b')
        newWriter.write(pack('<H', len(self.prove)))
        newWriter.write(self.prove.encode(encoding='utf-8'))
        newWriter.write(
            PKCS1_v1_5.new(
                self.loadPrivateKey()
            ).sign(
                new(
                    self.BDXContentWithInsideHeader.getvalue()
                )
            )
        )
        self.signature = newWriter.getvalue()
        # get sign content and sync datas
        writer.write(b'X')
        writer.write(self.signature)
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
        Note: We don't check the signature data
        """
        nowSeek = buffer.seek(0, 1)
        buffer.seek(-1, 2)
        if getByte(buffer, 1) != b'\x5a':
            self.signedOrNeedToSign = False
            buffer.seek(nowSeek, 0)
            return
        else:
            self.signedOrNeedToSign = True
        # check if need to sign this file
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
        # get sign content
        if getByte(signContent, 2) != b'\x00\x8b':
            self.isLegacy = True
            self.signature = signContent.getvalue()
            return
        else:
            proveLength: int = unpack('<H', getByte(signContent, 2))[0]
            self.prove = getByte(
                signContent, proveLength).decode(encoding='utf-8')
            self.signer = self.verificationProve()
            self.signature = getByte(signContent, signLength-proveLength-4)
        # sync datas
        buffer.seek(nowSeek, 0)
        # revert the pointer

    def Loads(self, jsonDict: dict) -> None:
        self.signer = jsonDict['Signer'] if 'Signer' in jsonDict else ''
        self.prove = jsonDict['Prove'] if 'Prove' in jsonDict else ''
        if 'Signature' in jsonDict:
            signBinaryContent: str = jsonDict['Signature']
            self.signature = bytes.fromhex(signBinaryContent)
        self.signedOrNeedToSign = jsonDict['Signed'] if 'Signed' in jsonDict else False
        self.isLegacy = jsonDict['Outdated'] if 'Outdated' in jsonDict else False

    def Dumps(self) -> dict:
        return {
            'Signer': self.signer,
            'Prove': self.prove,
            'Signature': self.signature.hex(),
            'Signed': self.signedOrNeedToSign,
            'Outdated': self.isLegacy
        }
