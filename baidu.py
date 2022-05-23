import rsa

pubkey='B3C61EBBA4659C4CE3639287EE871F1F48F7930EA977991C7AFE3CC442FEA49643212E7D570C853F368065CC57A2014666DA8AE7D493FD47D171C0D894EEE3ED7F99F6798B7FFD7B5873227038AD23E3197631A8CB642213B9F27D4901AB0D92BFA27542AE890855396ED92775255C977F5C302F1E7ED4B1E369C12CB6B1822F'

rsaPublickey = int(pubkey, 16)

key = rsa.PublicKey(rsaPublickey, 65537)

strc=key.save_pkcs1()
#pkcs1 pkcs8 openssl rsa -RSAPublicKey_in -in baidu.pem -pubout -out baidu_rsa_public_pkcs8.pem
with open('baidu.pem','w+') as f:
    f.write(strc)