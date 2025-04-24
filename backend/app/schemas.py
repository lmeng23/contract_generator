from pydantic import BaseModel


class ContractData(BaseModel):
    contractNumber: str
    signingDate: str
    companyName: str
    productTonnage: str
    unitPrice: str
    specialPrice: str
    phoneNumber: str
    companyAddress: str
    legalRepresentative: str
    authorizedAgent: str
    taxId: str
    bankAddress: str
    bankAccount: str
