from typing import List

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
    "objectClass": [b"organizationalUnit"],
    "ou": [b"people"],
}
ld_writer.unparse(dn, entry)

for entry in range(0, numberOfEntries):
    givenName = names.get_first_name()
    surName = names.get_last_name()
    commonName = f"{givenName} {surName}"
    email = f"{givenName.lower()}.{surName.lower()}@good.co"
    userId = uuid.uuid4()
    department = random.choice(companyStructure)

    entry = {
        "objectClass": [b"top", b"person", b"organizationalPerson", b"inetOrgPerson"],
        "commonName": [commonName.encode()],
        "givenName": [givenName.encode()],
        "surName": [surName.encode()],
        "mail": [email.encode()],
        "userId": [str(userId).encode()],
        "organizationalUnitName": [str(department).encode()]
    }
    dn = f"cn={commonName}, ou=people, {rootDn}"
    ld_writer.unparse(dn, entry)
