# Simple script to generate random users for test or development purposes. This utility will export the generated
# users to STDOUT. The output can be redirected to a file.
# It is standard LDIF which can be imported to any LDAP Directory
#
# Currently, this script requires the following modules to be installed:
# names==0.3.0
# pyasn1==0.4.7
# pyasn1-modules==0.2.7
# python-ldap==3.2.0
# six==1.12.0

from typing import List
from hashlib import sha1
from base64 import b64encode

import ldif
import sys
import names
import uuid
import random

# Configuration Constants - change these to get a different DIT
companyName = "GoodCo"

# Base DN for the directory
rootDn = "dc=corp, dc=good, dc=co"

# A dictionary with a list of departments. Users will be randomly assigned to one
companyStructure: List[str] = ['Technology',
                               'Sales',
                               'Accounting',
                               'Risk and Compliance',
                               'Business Operations']

# Number of user entries to create
numberOfEntries = 150

# Password string - all users are assigned the same initial password
password = "password"

# Global Variables

# Create the LDIFWriter to produce the ldif output
ld_writer = ldif.LDIFWriter(sys.stdout)

# Create Root Entry
dn = rootDn
entry = {
    "objectClass": [b"top", b"dcObject", b"organization"],
    "o": [companyName.encode()],
    "dc": [b"corp"]
}
ld_writer.unparse(dn, entry)

# Create 'people' OU to hold user information
dn = "ou=people, " + rootDn
entry = {
    "objectClass": [b"top", b"organizationalUnit"],
    "ou": [b"people"],
}
ld_writer.unparse(dn, entry)

# print(b64encode(("{SHA}" + sha1(password.encode()).hexdigest()).encode()))

for entry in range(0, numberOfEntries):
    givenName = names.get_first_name()
    surName = names.get_last_name()
    commonName = f"{givenName} {surName}"
    email = f"{givenName.lower()}.{surName.lower()}@good.co"
    userId = uuid.uuid4()
    department = random.choice(companyStructure)
    # This is not working. There may not be a way to provide a hashed password via ldif
    # passhash = b64encode(("{SHA}" + sha1(password.encode()).hexdigest()).encode())

    entry = {
        "objectClass": [b"top", b"person", b"organizationalPerson", b"inetOrgPerson"],
        "commonName": [commonName.encode()],
        "givenName": [givenName.encode()],
        "surName": [surName.encode()],
        "mail": [email.encode()],
        "userId": [str(userId).encode()],
        "organizationalUnitName": [str(department).encode()],
        "userPassword": [password.encode()]
    }
    dn = f"cn={commonName}, ou=people, {rootDn}"
    ld_writer.unparse(dn, entry)
