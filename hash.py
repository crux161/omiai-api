#!/usr/bin/env python

import bcrypt; 

print(bcrypt.hashpw(b'PASSWORD', bcrypt.gensalt()).decode())
