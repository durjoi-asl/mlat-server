from app import *
# print(dir(Users))

# print(sqlDB.session.query(Users).count())

permissionList = [
    'super',
    'read',
    'write'
]

roleList = [
    'super-admin',
    'admin',
    'customer',
    'worker',
    'manager'
]

userList = [
    ['name','password'],
    ['name1','password'],
    ['name2','password'],
    ['name3','password'],
    ['name4','password'],
    ['name5','password'],
    ['name6','password']
]

#create users
def createUsers():
    for usr in userList:
        # print('aha')
        # print(usr[0])
        # print(usr[1])
        hashed_password = generate_password_hash(usr[1], method='sha256')
        new_user = Users(public_id=str(uuid.uuid4()), name=usr[0], password=hashed_password, admin=True)
        sqlDB.session.add(new_user)
        sqlDB.session.commit()
    
    print(Users.query.all())

#create roles
def createRoles():
    for rl in roleList:
        print(rl)
        
        new_role = Role(role=rl)
        sqlDB.session.add(new_role)
        sqlDB.session.commit()
    print(Role.query.all())

#add role
def addRole():
    person1 = Users.query.all()[3]
    Role.query.all()[0].append(person1)
# role0.persons.append(person3)


#CREATE permissions
def createPermissions():
    for pm in permissionList:
        print(pm)
        dir(Permission)
        new_permission = Permission(permission=pm)
        sqlDB.session.add(new_permission)
        sqlDB.session.commit()
    print(Permission.query.all())

# print(Users.query.all())

if __name__ == "__main__":
    createUsers()
    createRoles()
    createPermissions()

    # print(Role.query.all()[0].role)
    pass