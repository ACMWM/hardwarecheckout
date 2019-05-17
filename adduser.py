#!/usr/bin/env python3
import sys

import sql
from models import User

sql.init_db()
input("Are you sure you want to add "+sys.argv[1]+"? Press Ctrl+C to cancel,"
        "or anything else to continue")


u = User(name="", email=sys.argv[1])
sql.add(u)
sql.commit()
