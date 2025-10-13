from pydantic import BaseModel


class ContractData(BaseModel):
    contractNumber: str
    signingDate: str
    productTonnage: str
    unitPrice: str
    specialPrice: str
    companyName: str
    phoneNumber: str
    companyAddress: str
    taxId: str
    bankAddress: str
    bankAccount: str
    deliveryMethod: str
    legalRepresentative: str
    authorizedAgent: str
