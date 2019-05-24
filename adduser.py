#!/usr/bin/env python3
import sys

import sql
import auth
from models import User

if len(sys.argv) != 2:
    print("Usage: "+sys.argv[0]+" <username>")
    sys.exit(1)

sql.init_db()
email = sys.argv[1]+"@"+auth.domain
if auth.validemail(email) is None:
    print(email+" is not a valid email.")
    sys.exit(2)

input("Are you sure you want to add "+email+"? Press Ctrl+C to cancel,"
        "or anything else to continue")


u = User(id=email)
sql.add(u)
sql.commit()
print("Added "+email+" to the authorized users list.")
