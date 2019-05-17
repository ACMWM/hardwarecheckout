#!/usr/bin/env python3
import sys

import sql
from models import User

if len(sys.argv) != 2:
    print("Usage: "+sys.argv[0]+" <email>")
    sys.exit(1)

sql.init_db()
input("Are you sure you want to add "+sys.argv[1]+"? Press Ctrl+C to cancel,"
        "or anything else to continue")


u = User(email=sys.argv[1])
sql.add(u)
sql.commit()
print("Added "+sys.argv[1]+" to the authorized users list.")
