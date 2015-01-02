from . import *


#class UserAdd(Command):
#    "adds users"
# 
#    def run(self):
#        uid = raw_input("uid: ")
#        email = raw_input("email: ")
#        password = raw_input("password: ")
#        admin = raw_input("admin (y/n): ")
#        nuser = user_service.create(username=uid,password=password,email=email,active=True)
#        if admin.lower() in ['y', 'j', 'ja', 'yes']:
#            # put user in group 'admin'
#            g = group_service.first(groupname='admin')
#            if g is None:
#                g = group_service.create(groupname='admin')
#            g.members += [nuser]
#            group_service.save(g)
