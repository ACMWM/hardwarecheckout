#!/usr/bin/env python3

import sys

import sql
import models

sql.init_db()

if len(sys.argv) > 3:
    c = sys.argv[3]
else:
    c = None
if len(sys.argv) > 2:
    q = int(sys.argv[2])
else:
    q = 1
h = models.HW(name=sys.argv[1], quantity=q, available=q, category=c)

sql.add(h)
