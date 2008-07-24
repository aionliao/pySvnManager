#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from pysvnmanager.tests import *
from pysvnmanager import model
from pysvnmanager.model.svnauthz import *
import StringIO
from pprint import pprint

class TestModels(TestController):
    
    def __init__(self, *args):
        self.authz = SvnAuthz()
        super(TestModels, self).__init__(*args)

    def setUp(self):

        buff = '''
# version = 0.1.1
# admin : / = root, &admin
# admin : repos1 = @admin
# admin : repos2 = admin2
# admin : repos3 = admin3
# admin : reposx = 

[groups]
admins=&admin,&007
admin=&admin, admin1, admin2, admin3
team1=user1,user11, @team2
team2=user2,user22,@team3,
# Wrong configuration: cyclic dependancies
#   team1->team2->team3->team1->...
# We can detect and fix.
team3=user3,user33,@team1
all=@team1,user3,user4

[aliases]
admin=jiangxin
007=james


[repos1:/trunk/src]
user1=
&007 = r

[/trunk/src]
user1=r
user2=r

[repos1:/trunk]
user1=r
user2=

[/trunk]
user2=

[repos1:/]
user3=
@admins=rw

[/]
user3=r
user4=r

[/branches]
$authenticated = r
@admins = rw

[/tags]
* = 
@all = r
@admins = rw
        '''

        file = StringIO.StringIO(buff)
        self.authz.load(file)

    def tearDown(self):
        pass
    
    def testUser(self):
        user1 = User('Tom')
        self.assert_(str(user1) == 'Tom')
        self.assertRaises(Exception, User, "")
        user2 = User('Jerry')
        user3 = User('Zeb')
        self.assert_(user2<user1<user3)
        self.assert_('tom' in user1)
        self.assert_(user1 in user1)
        self.assert_(not 'Tom' in user2)
        alias1 = Alias('Tom')
        self.assert_(not alias1 in user1)
        alias1.user = user2
        self.assert_(alias1 in user2)
        self.assert_(not alias1 in user3)
        self.assert_(not None in user3)
        
    def testAlias(self):
        user1 = User('Tom')
        alias1=Alias('admin')
        alias1.user = user1
        self.assert_(str(alias1) == 'admin = Tom', str(alias1))
        alias2=Alias('manager', user1)
        self.assert_(str(alias2) == 'manager = Tom', str(alias1))

        self.assert_('&Manager' in alias2)
        self.assert_(not 'manager' in alias2)
        self.assert_('tom' in alias2)
        self.assert_(alias1 in alias2)
        self.assert_(user1 in alias2)
        self.assert_(not None in alias2)
        
        try:
            alias1.user=""
        except:
            pass
        else:
            fail("alias user point to User object, not others.")
        
        self.assertRaises(Exception, Alias, 'admin', 'Tom')
        self.assertRaises(Exception, Alias, '')
        self.assertRaises(Exception, Alias, '&admin')
        

    def testGroup(self):
        self.assertRaises(Exception, Group, '')
        self.assertRaises(Exception, Group, '@admin')
        user1 = User('user1')
        user2 = User('user2')
        user3 = User('user3')
        group2 = Group('team2')
        alias = Alias('admin')
        alias.user = user3
        self.assert_(group2.membernames == [])

        group1 = Group('team1')
        self.assert_(group1.name == 'team1')
        self.assert_(group1.uname == '@team1')
        group1.append([user1, user2])
        self.assert_(group1.membernames == ['user1','user2'], group1.membernames)

        group1.append([group2, alias])
        self.assert_(str(group1) == 'team1 = &admin, @team2, user1, user2', str(group1))
        self.assert_([m.uname for m in group1] == ['user1', 'user2', '@team2', '&admin'], [m.uname for m in group1])
        
        group1.remove('user1, &admin')
        self.assert_(group1.membernames == ['@team2', 'user2'], group1.membernames)
        group1.append(user1, alias)
        self.assert_(group1.membernames == ['&admin', '@team2', 'user1', 'user2'], group1.membernames)
        group1.remove([user2, '@team2', 'noexist'])
        self.assert_(group1.membernames == ['&admin', 'user1'], group1.membernames)
        group1.append(user2, group2)
        self.assert_(group1.membernames == ['&admin', '@team2', 'user1', 'user2'], group1.membernames)
        
        self.assertRaises(Exception, group2.append, group1, alias)
        group2.append(group1, alias, user1, autodrop=True)
        self.assert_([m.uname for m in group2] == ['&admin', 'user1'], [m.uname for m in group2])
        
        self.assert_(not 'admin' in group1)
        self.assert_('&admin' in group1)
        self.assert_(alias in group1)
        self.assert_('user3' in group1)
        self.assert_(user3 in group1)
        group1.append(Group('$authenticated'))
        self.assert_('nobody' in group1)
        group1.remove('$authenticated')
        self.assert_(not 'nobody' in group1)
        group1.append(Group('$anonymous'))
        self.assert_('*' in group1)
        self.assert_(not 'nobody' in group1)
        group1.remove('$anonymous')
        self.assert_(not '*' in group1)
        group1.append(Group('*'))
        self.assert_('*' in group1)
        self.assert_('nobody' in group1)
        self.assert_(not None in group1)
        self.assert_(not "  " in group1)
        
        group1.remove_all()
        self.assert_(group1.membernames == [], group1.membernames)
        
        g = Group('$authenticated')
        self.assert_(str(g) == "# Built-in group: $authenticated")

    def testIsValidName(self):
        self.assert_(is_valid_name('jiang"xin')=="Name contains invalid characters.")
        self.assert_(is_valid_name('jiang xin')=="Name contains invalid characters.")
        self.assert_(is_valid_name('jiang"xin')=="Name contains invalid characters.")
        self.assert_(is_valid_name('')=="Name is not given.")
        self.assert_(is_valid_name(User('user'))=="Name is not string.")
        self.assert_(is_valid_name('my repos', "repos")=="Name contains invalid characters.")
        self.assert_(is_valid_name('/', "repos")=="")
        
    def testUserList(self):
        ulist = UserList()
        self.assert_(list(ulist) == [])
        user1 = ulist.get_or_set('jiangxin')
        self.assert_(user1.name == 'jiangxin')
        self.assert_(user1.uname == 'jiangxin')
        self.assert_(list(ulist) == [user1])
        user2 = ulist.get_or_set('user2')
        self.assert_(user2.name == 'user2')
        self.assert_(user2.uname == 'user2')
        self.assert_(list(ulist) == [user1, user2])
        user3 = ulist.get('user3')
        self.assert_(user3==None)
        user3 = User('user3')
        self.assertRaises(Exception, ulist.get, user3)
        self.assert_([u.uname for u in ulist] == ['jiangxin', 'user2'], [u.uname for u in ulist])
        self.assert_(ulist.get_or_set('  ')==None)
        self.assertRaises(Exception, ulist.get_or_set, '&alias1')
        self.assertRaises(Exception, ulist.get_or_set, '@team1')
        self.assertRaises(Exception, ulist.get_or_set, '$anonymous')
        self.assertRaises(Exception, ulist.get_or_set, 'jiang xin')

    def testAliasList(self):
        alist = AliasList()
        self.assert_(list(alist) == [])
        alias1 = alist.get_or_set('admin')
        self.assert_(alias1.name == 'admin')
        alias1 = alist.get('admin')
        self.assert_(alias1.uname == '&admin')
        self.assert_(list(alist) == [alias1])
        alias2 = alist.get_or_set('&root')
        self.assert_(alias2.name == 'root')
        self.assert_(alias2.uname == '&root')
        self.assert_(list(alist)== [alias1, alias2])
        self.assert_([a.uname for a in alist] == ['&admin', '&root'], [a.uname for a in alist])

        self.assert_(str(alist)=="[aliases]\nadmin = \nroot = \n", repr(str(alist)))
        
        self.assert_(alist.get_or_set('')==None)
        self.assert_(alist.get_or_set('  ')==None)
        self.assert_(alist.get('noexist')==None)
        self.assertRaises(Exception, alist.get_or_set, 'admin user')
        
        assert alist.remove(alias1)==True
        self.assert_([a.uname for a in alist] == ['&root'], [a.uname for a in alist])
        alias1 = alist.get_or_set('admin')
        assert alist.remove('&admin')==True
        self.assert_([a.uname for a in alist] == ['&root'], [a.uname for a in alist])
        assert alist.remove('notexist')==False
        

    def testGroupList(self):
        user1 = User('user1')
        user2 = User('user2')
        alias = Alias('admin')
        alias.user=user1
        
        glist = GroupList()
        self.assert_(list(glist) == [])
        g1 = glist.get_or_set('team1')
        self.assert_(g1.name == 'team1')
        self.assert_(g1.uname == '@team1')
        self.assert_(list(glist) == [g1])
        g2 = glist.get_or_set('team2')
        self.assert_(g2.name == 'team2')
        self.assert_(g2.uname == '@team2')
        self.assert_(list(glist) == [g1, g2])

        g1.append(user1, g2)
        g2.append(user2, alias)

        self.assert_([g.uname for g in glist] == ['@team1', '@team2'], [g.uname for g in glist])

        self.assert_(str(glist)=="[groups]\nteam1 = @team2, user1\nteam2 = &admin, user2\n", repr(str(glist)))
        
        self.assert_(glist.get_or_set('')==None)
        self.assert_(glist.get_or_set('  ')==None)
        self.assert_(glist.get('noexist')==None)
        self.assertRaises(Exception, glist.get, 'admin user')
        
        glist.remove(g1)
        self.assert_([g.uname for g in glist] == ['@team2'], [g.uname for g in glist])
        g1 = glist.get_or_set('team1')
        g1.append(user1, g2)
        self.assertRaises(Exception, glist.remove, '@team2')
        self.assertRaises(Exception, glist.remove, g2)
        self.assert_(str(glist)=='[groups]\nteam1 = @team2, user1\nteam2 = &admin, user2\n', repr(str(glist)))
        glist.remove('@team2',force=True)
        glist.remove('notexist')
        self.assert_(str(glist)=="[groups]\nteam1 = user1\n", repr(str(glist)))
        
    def testRules(self):
        user1 = User('user1')
        user2 = User('user2')
        user3 = User('user3')
        alias = Alias('admin')
        alias.user=user2
        group1 = Group('group1')
        group1.append(user1,alias)
        rule1 = Rule(group1)
        self.assert_(rule1.uname == '@group1', rule1.uname)
        self.assert_(rule1.rights == RIGHTS_NONE)
        rule1.rights = 'rw'
        self.assert_(rule1.rights == RIGHTS_ALL)
        rule1.rights = RIGHTS_ALL
        self.assert_(rule1.rights == RIGHTS_R|RIGHTS_W)
        self.assert_(str(rule1)=='@group1 = rw', repr(str(rule1)))
        self.assert_(rule1.get_permission(group1) == (RIGHTS_ALL, RIGHTS_NONE))
        self.assert_(rule1.get_permission(user1) == (RIGHTS_ALL, RIGHTS_NONE))
        self.assert_(rule1.get_permission(user2) == (RIGHTS_ALL, RIGHTS_NONE))
        self.assert_(rule1.get_permission('user2') == (RIGHTS_ALL, RIGHTS_NONE))
        self.assert_(rule1.get_permission(user3) == (RIGHTS_NONE, RIGHTS_NONE))
        
        group0 = Group('group0')
        rule0 = Rule(group0)
        rulelist = [rule1, rule0]
        rulelist.append('@choose...')
        self.assert_([str(r) for r in rulelist]==['@group1 = rw', '@group0 = ', '@choose...'], [str(r) for r in rulelist])
        self.assert_([str(r) for r in sorted(rulelist)]==['@group0 = ', '@group1 = rw', '@choose...'], [str(r) for r in sorted(rulelist)])
        

    def testModule(self):
        module = Module('/', '/trunk')
        self.assert_(module.path == '/trunk')
        self.assert_(module.fullname == '/:/trunk')
        self.assert_(str(module)=='')
        
        obj = Group('* ')
        module.update_rule(obj,'')
        obj = Group('admins')
        module.update_rule(obj, 'rw')
        obj = Group('* ')
        module.update_rule(obj, 'r')
        obj = User(' jiang ')
        module.update_rule(obj, '')
        obj = Group(' $authenticated ')
        module.update_rule(obj, 'r')
        self.assert_(str(module) == 
'''[/trunk]
$authenticated = r
* = r
@admins = rw
jiang = 
''', repr(str(module)))
        self.assert_([str(r) for r in module]==['* = r', '@admins = rw', 'jiang = ', '$authenticated = r'], [str(r) for r in module])
        self.assert_([str(r) for r in module.rules]==['* = r', '@admins = rw', 'jiang = ', '$authenticated = r'], [str(r) for r in module.rules])
        
        module.del_rule('@admins= rw')
        self.assert_([str(r) for r in module]==['* = r', 'jiang = ', '$authenticated = r'], [str(r) for r in module])
        
        module = Module('myrepos', '')
        groupstar = Group('* ')
        module.update_rule(groupstar,'r')
        group1 = Group(' team1 ')
        module.update_rule(group1,'rw')
        groupstr = Group('*')
        module.update_rule(groupstr,'')
        user1 = User(' jiang ')
        module.update_rule(user1,'')
        groupauth = Group('$authenticated')
        module.update_rule(groupauth,'r')
        self.assert_(str(module) == '''[myrepos:/]
$authenticated = r
* = 
@team1 = rw
jiang = 
''', repr(str(module)))
        self.assert_(module.get_permit_bits(user1)==(RIGHTS_R, RIGHTS_ALL),module.get_permit_bits(user1))
        self.assert_(module.get_permit_str(user1)=='r',module.get_permit_str(user1))
        self.assert_(module.get_permit_str('@team1')=='rw',module.get_permit_str('@team1'))
        self.assert_(module.access_is_determined(user1))
        self.assert_(module.access_is_granted(user1,'r'))
        self.assert_(module.access_is_granted(user1,RIGHTS_R))
        self.assert_(module.access_is_granted(user1,'rw')==False)
        module.del_rule(('$authenticated = r','*='))
        self.assert_(module.access_is_determined(User("jiang")))
        self.assert_(module.access_is_granted(user1,''))
        self.assert_(module.access_is_determined(User("nobody"))==False)
        self.assertRaises(Exception, module.del_rule, None)
        
        module.clean_rules()
        self.assert_([str(r) for r in module]==[], [str(r) for r in module])

        self.assert_(Module('repos1', '/trunk')>Module('repos0', '/trunk'))
        self.assert_(Module('repos1', '/trunk')<"choice...")

    def testRepos(self):
        user1=User('user1')
        user2=User('user2')
        user3=User('user3')
        alias1=Alias('alias1')
        alias1.user=user1
        group1=Group('group1')
        group2=Group('group2')
        
        repos1=Repos("myrepos1")
        self.assert_(repos1.name=="myrepos1")
        repos1.name="repos1"
        self.assert_(repos1.name=="repos1")
        self.assert_(repos1.is_blank()==True)

        self.assert_(repos1.admins=='')
        repos1.admins=[user1, alias1, group1]
        self.assert_(repos1.admins=='&alias1, @group1, user1', repos1.admins)
        self.assert_(repos1.is_blank()==False)
        repos1.del_admin([user1,])
        self.assert_(repos1.admins=='&alias1, @group1', repos1.admins)
        self.assertRaises(Exception, repos1.del_admin, '@group1')
        
        try:
            repos1.admins='user1'
        except:
            pass
        else:
            fail("repos admins set to user/group/alias object, not name.")
            
        mod1 = repos1.add_module('/trunk')
        self.assert_(mod1 == repos1.add_module('/trunk'))
        self.assert_(mod1 == repos1.get_module('/trunk'))
        self.assert_(None == repos1.get_module('/nothing'))
        mod2 = repos1.add_module('/tags')
        mod3 = repos1.add_module('/trunk/src')
        repos1.add_module('/wrong')
        mod4 = repos1.add_module('/branches')
        mod5 = repos1.del_module('/wrong')
        self.assert_([m.path for m in repos1]==['/trunk', '/tags', '/trunk/src', '/branches'], [m.path for m in repos1])
        self.assert_(repos1.path_list == ['/trunk', '/tags', '/trunk/src', '/branches'], repos1.path_list)

        mod1.update_rule(user1,'r')
        mod2.update_rule(alias1,'rw')

        self.assert_(str(repos1)=='[repos1:/tags]\n&alias1 = rw\n\n[repos1:/trunk]\nuser1 = r\n\n', repr(str(repos1)))
        
        repos1.del_all_modules()
        self.assert_(repos1.path_list == [], repos1.path_list)
        
        self.assert_(Repos('repos1') > Repos('repos0'))
        self.assert_(Repos('repos1') < 'astring')

    def testReposList(self):
        user1 = User('user1')
        user2 = User('user2')
        alias = Alias('admin')
        alias.user=user1
        
        rlist = ReposList()
        self.assert_([r.name for r in rlist] == ['/'], [r.name for r in rlist])
        r0 = rlist.get('/')

        r1 = rlist.get_or_set('repos1')
        self.assert_(r1.name == 'repos1')
        self.assert_(list(rlist) == [r0, r1])
        r2 = rlist.get_or_set('repos2')
        r2.add_module('/')
        module=r2.add_module('/trunk')
        module.update_rule(user1, 'r')
        self.assert_(r2.name == 'repos2')
        self.assert_(list(rlist) == [r0, r1, r2])

        self.assert_([r.name for r in rlist] == ['/', 'repos1', 'repos2'], [r.name for r in rlist])

        self.assert_(rlist.get('noexist')==None)
        self.assertRaises(Exception, rlist.get, 'wrong repos')
        
        self.assert_(str(rlist)=='[repos2:/trunk]\nuser1 = r\n\n', repr(str(rlist)))
        
        self.assert_([r.name for r in rlist] == ['/', 'repos1', 'repos2'], [r.name for r in rlist])
        rlist.remove(r1)
        self.assert_([r.name for r in rlist] == ['/', 'repos2'], [r.name for r in rlist])
        rlist.remove(r2)
        self.assert_([r.name for r in rlist] == ['/', 'repos2'], [r.name for r in rlist])
        rlist.remove(r2, recursive=True)
        self.assert_([r.name for r in rlist] == ['/'], [r.name for r in rlist])
        self.assertRaises(Exception, rlist.remove, 'notexist')
        rlist.remove('/', recursive=False)
        rlist.remove('/', recursive=True)
        self.assert_([r.name for r in rlist] == ['/'], [r.name for r in rlist])
          
    def testReposAdmin(self):
        authz = SvnAuthz()
        u1=authz.add_user('u1')
        u2=authz.add_user('u2')
        u3=authz.add_user('u3')
        u4=authz.add_user('u4')
        u5=authz.add_user('u5')
        u6=authz.add_user('u6')
        u7=authz.add_user('u7')
        admin = authz.add_alias('admin', 'u1')
        team1 = authz.add_group('team1', 'u2, u3, u4')
        repos1 = authz.add_repos('repos1')
        
        authz.set_admin('&admin, u7')
        authz.set_admin('@team1', 'repos1')
        self.assert_(authz.get_repos('/').admins == '&admin, u7')
        self.assert_(authz.get_repos('/repos1').admins == '@team1')
        authz.set_admin(', @team1, ', 'repos1')
        self.assert_(authz.get_repos('repos1').admins == '@team1')
        authz.set_admin(['&admin', 'u6'])
        self.assert_(authz.get_repos('/').admins == '&admin, u6')
        authz.set_admin([admin, u5])
        self.assert_(authz.get_repos('/').admins == '&admin, u5')

        authz.set_admin('')
        self.assert_(authz.get_repos('/').admins == '')
        authz.set_admin([])
        self.assert_(authz.get_repos('/').admins == '')
        authz.set_admin(None)
        self.assert_(authz.get_repos('/').admins == '')

    def testAuthzConfAcl(self):
        rl = self.authz.reposlist
        self.assert_(rl.get('/').name == '/')
        self.assert_(rl.get('/').admins == '&admin, root', rl.get('/').admins)
        self.assert_(rl.get('repos1').name == 'repos1')
        self.assert_(rl.get('repos1').admins == '@admin', rl.get('repos1').admins)
        self.assert_(rl.get('repos2').name == 'repos2', 'name: %s' % rl.get('repos2').name)
        self.assert_(rl.get('repos2').admins == 'admin2', rl.get('repos2').admins)
        self.assert_(self.authz.compose_acl() == 
'''# admin : / = &admin, root
# admin : repos1 = @admin
# admin : repos2 = admin2
# admin : repos3 = admin3
''', self.authz.compose_acl())
        pass

    def _testAuthzConfAliases(self):
        al = self.authz.aliaslist
        self.assert_(al.get('admin').username == 'jiangxin', str(al.get('admin')))
        self.assert_(str(al) == '[aliases]\n007 = james\nadmin = jiangxin\n', repr(str(al)))
        pass

    def testAuthzConfGroups(self):
        gl = self.authz.grouplist
        self.assert_(sorted(gl.get('admins').membernames) == ['&007', '&admin'],
                     sorted(gl.get('admins').membernames))
        self.assert_(sorted(gl.get('team1').membernames) == 
                     ['@team2', 'user1', 'user11'],
                     sorted(gl.get('team1').membernames))
        self.assert_(sorted(gl.get('all').membernames) == 
                     ['@team1', 'user3', 'user4'],
                     sorted(gl.get('all').membernames))
        self.assert_(str(gl) == 
            '''[groups]
admin = &admin, admin1, admin2, admin3
admins = &007, &admin
all = @team1, user3, user4
team1 = @team2, user1, user11
team2 = @team3, user2, user22
team3 = user3, user33
''', repr(str(gl)))
        pass

    def testAuthzConfRepos(self):
        # blank configuration
        self.authz.load()
        # add_repos
        self.assert_(isinstance(self.authz.add_repos('repos1'), Repos))
        self.assert_(isinstance(self.authz.add_repos('repos2'), Repos))
        self.assert_(','.join(map(lambda x:x.name, self.authz.reposlist)) ==
                     '/,repos1,repos2', ','.join(map(lambda x:x.name,
                                                     self.authz.reposlist)))
        # add_admin
        self.assert_(self.authz.set_admin('admin1,admin2') == True)
        self.assert_(self.authz.is_admin('admin1','/') == True)
        self.assert_(self.authz.set_admin('adminx', 'repos1') == True)
        self.assert_(self.authz.is_admin('adminx', 'repos1') == True)
        self.assert_(self.authz.is_super_user('admin1') == True)
        self.assert_(self.authz.is_super_user('adminx') == False)

        self.assert_(self.authz.get_manageable_repos_list('admin1') == ['/', 'repos1', 'repos2'], self.authz.get_manageable_repos_list('admin1'))
        self.assert_(self.authz.get_manageable_repos_list('adminx') == ['repos1'], self.authz.get_manageable_repos_list('adminx'))
        self.assert_(self.authz.get_manageable_repos_list('adminxyz') == [])
        self.assert_(self.authz.get_manageable_repos_list('') == [])
        # add_module (repos = /)
        self.assert_(isinstance(self.authz.add_module('/', '/trunk///'), Module))
        m = self.authz.get_module('/', '/trunk/')
        self.assert_(isinstance(m, Module))
        self.assert_(m.path == '/trunk')
        self.assert_(m.repos == '/')
        # add_module (path = /)
        self.assert_(isinstance(self.authz.add_module('repos1', '/'), Module))
        m = self.authz.get_module('repos1', '')
        self.assert_(m.repos+':'+m.path == 'repos1:/')
        self.assert_(','.join(map(lambda x:x.repos+':'+x.path,
                                  self.authz.modulelist())) ==
                     '/:/trunk,repos1:/', ','.join(map(lambda
                                                       x:x.repos+':'+x.path,
                                                       self.authz.modulelist())))

        # add_alias
        user = self.authz.add_user('jiangxin')
        self.assert_(isinstance(self.authz.add_alias('superuser', user), Alias))
        self.assert_(isinstance(self.authz.add_alias('root', user), Alias))
        self.assert_(str(self.authz.aliaslist) == '[aliases]\nroot = jiangxin\nsuperuser = jiangxin\n', repr(str(self.authz.aliaslist)))
        self.assert_(','.join(map(lambda x:x.name, self.authz.aliaslist)) ==
                     'superuser,root', ','.join(map(lambda x:x.name,
                                                    self.authz.aliaslist)))

        # add_group
        self.assert_(str(self.authz.grouplist) == '[groups]\n', repr(str(self.authz.grouplist)))
        self.assert_(isinstance(self.authz.add_group('myteam','user1'), Group))
        self.assert_(str(self.authz.grouplist) == '[groups]\nmyteam = user1\n', repr(str(self.authz.grouplist)))
        self.assert_(isinstance(self.authz.add_group_member('myteam','user2,user3'), Group))
        self.assert_(isinstance(self.authz.add_group_member('myteam','user2,user3'), Group))
        self.assert_(str(self.authz.grouplist) == '[groups]\nmyteam = user1, user2, user3\n', repr(str(self.authz.grouplist)))
        self.assert_(','.join(map(lambda x:x.name, self.authz.grouplist)) ==
                     'myteam', ','.join(map(lambda x:x.name,
                                            self.authz.grouplist)))
        self.assert_(isinstance(self.authz.add_group_member('team1','@team2'),Group))
        self.assert_(isinstance(self.authz.add_group_member('myteam','@team1, @team2, *, $authenticated'),Group))
        self.assert_(isinstance(self.authz.add_group_member('team2','$authenticated,*'),Group))
        self.assert_(isinstance(self.authz.add_group_member('team3','@team4'),Group))
        self.assert_(isinstance(self.authz.add_group_member('team4','@myteam'),Group))
        self.assertRaises(Exception, self.authz.add_group_member, 'myteam','@team3, @team4, @team5')
        self.assert_(str(self.authz.grouplist.get('@myteam')) == 
                     'myteam = $authenticated, *, @team1, @team2, user1, user2, user3', 
                     repr(str(self.authz.grouplist.get('@myteam')))) 
        self.assert_(isinstance(self.authz.add_group_member('myteam','@team3, @team4, @team5', True),Group))
        self.assert_(str(self.authz.grouplist.get('@myteam')) == 
                     'myteam = $authenticated, *, @team1, @team2, @team5, user1, user2, user3', 
                     repr(str(self.authz.grouplist.get('@myteam')))) 
        self.assertRaises(Exception, self.authz.del_group, '@team2')
        self.assert_(str(self.authz.grouplist.get('@team2')) == 'team2 = $authenticated, *', 
                     self.authz.grouplist.get('@team2'))
        self.authz.del_group('@team2',force=True)
        self.assert_(self.authz.grouplist.get('@team2') == None, 
                     str(self.authz.grouplist.get('@team2')))
        self.assert_(str(self.authz.grouplist.get('@myteam')) == 
                     'myteam = $authenticated, *, @team1, @team5, user1, user2, user3',
                     repr(str(self.authz.grouplist.get('@myteam')))) 
        self.assert_(str(self.authz.grouplist.get('@team1')) == 'team1 = ',
                     repr(str(self.authz.grouplist.get('@team1')))) 

        # add_rule 
        module = self.authz.get_module('/', '/trunk/')
        tmpstr = "%s" % module
        self.assert_(tmpstr =='', tmpstr)
        self.authz.set_rules('/', '/trunk', 'user1=r\nuser1 = rw\n user2 =\n')
        tmpstr = "%s" % module
        self.assert_(tmpstr ==u'[/trunk]\nuser1 = rw\nuser2 = \n', repr(tmpstr))
        self.authz.set_rules('/', '/trunk', '')
        tmpstr = "%s" % module
        self.assert_(tmpstr ==u'', repr(tmpstr))

        self.assert_(self.authz.add_rules('/', '/trunk/', '&superuser=rw') == True, self.authz.add_rules('/', '/trunk/', '&superuser=rw'))
        self.assert_(self.authz.add_rules('repos1', '/', '*=r') == True, self.authz.add_rules('repos1', '/', '*=r'))
        self.assert_(str(self.authz.get_module('repos1', '/')) == '[repos1:/]\n* = r\n', repr(str(self.authz.get_module('repos1', '/'))))
        self.assert_(self.authz.add_rules('repos1', '/', ['*=', '@team1=rw']) == True)
        self.assert_(str(self.authz.get_module('repos1', '/')) == '[repos1:/]\n* = \n@team1 = rw\n', repr(str(self.authz.get_module('repos1', '/'))))
        self.assert_(','.join(map(lambda x:str(x), self.authz.rulelist())) ==
                     '&superuser = rw,* = ,@team1 = rw', ','.join(map(lambda
                                                                      x:str(x),
                                                                      self.authz.rulelist())))
        self.assertRaises(Exception, self.authz.chk_grp_ref_by_rules, '*')
        self.assertRaises(Exception, self.authz.chk_grp_ref_by_rules, '@team1')
        self.authz.chk_grp_ref_by_rules('@team2')

        self.assert_(self.authz.del_rule('repos1', '/', ['*=rw']) == True)
        self.assert_(str(self.authz.get_module('repos1', '/')) == '[repos1:/]\n@team1 = rw\n', repr(str(self.authz.get_module('repos1', '/'))))
        self.assert_(','.join(map(lambda x:x.name, self.authz.grouplist)) ==
                     'myteam,team1,*,$authenticated,team3,team4,team5',
                     ','.join(map(lambda x:x.name, self.authz.grouplist)))

        # del_alias
        self.authz.chk_alias_ref_by_rules('&root')
        self.authz.del_alias('&root')
        self.assertRaises(Exception, self.authz.chk_alias_ref_by_rules, '&superuser')
        self.assertRaises(Exception, self.authz.del_alias, '&superuser')
        self.assert_(','.join(map(lambda x:x.name, self.authz.aliaslist)) ==
                     'superuser', ','.join(map(lambda x:x.name,
                                               self.authz.aliaslist)))

        # del_group
        self.assertRaises(Exception, self.authz.chk_grp_ref_by_rules,'@team1')
        self.assertRaises(Exception, self.authz.del_group,'@team1')
        self.authz.chk_grp_ref_by_rules('myteam')
        self.assertRaises(Exception, self.authz.del_group,'@myteam')
        self.assert_(','.join(map(lambda x:x.name, self.authz.grouplist)) ==
                     'myteam,team1,*,$authenticated,team3,team4,team5',
                     ','.join(map(lambda x:x.name, self.authz.grouplist)))
        self.assert_(self.authz.del_group('@myteam',force=True) == True)
        self.assert_(','.join(map(lambda x:x.name, self.authz.grouplist)) ==
                     'team1,*,$authenticated,team3,team4,team5',
                     ','.join(map(lambda x:x.name, self.authz.grouplist)))

        # remove
        self.assert_(isinstance(self.authz.add_group_member('myteam','user1,user2,user3'),Group))
        self.assert_(self.authz.del_group_member('myteam','user1,user3') == True)
        self.assert_(str(self.authz.grouplist) == 
                     '[groups]\nmyteam = user2\nteam1 = \nteam3 = @team4\nteam4 = \nteam5 = \n',
                     repr(str(self.authz.grouplist)))

        # del_module
        self.assert_(self.authz.del_module('repos2', '/') == False)
        self.assert_(self.authz.del_module('repos1', '/') == True)
        self.assert_(self.authz.get_module('repos1', '/') == None)

        # del_repos
        #self.assert_(str(self.authz) == '', str(self.authz))
        self.assert_(self.authz.get_repos('/').is_blank() == False)
        self.assert_(self.authz.get_repos('repos2').is_blank() == True)
        self.assert_(self.authz.get_repos('repos1').is_blank() == False)
        self.assert_(self.authz.del_repos('/') == False)
        self.assert_(self.authz.del_repos('/', recursive=True) == True)
        self.assert_(self.authz.get_repos('/').is_blank() == False)
        self.assert_(self.authz.del_repos('repos2') == True)
        self.assert_(self.authz.del_repos('repos1') == False)
        self.assert_(self.authz.del_repos('repos1',recursive=True) == True)

        # output config from __str__
        self.assert_(str(self.authz) == 
                     '# version : 0.1.0\n# admin : / = admin1, admin2\n\n[groups]\nmyteam = user2\nteam1 = \nteam3 = @team4\nteam4 = \nteam5 = \n\n[aliases]\nsuperuser = jiangxin\n\n', 
                     repr(str(self.authz)))

    def testAuthzConfDefault(self):
        # is_admin()
        self.assert_(self.authz.is_admin('jiangxin') == True)
        self.assert_(self.authz.is_admin('root') == True, self.authz.is_admin('root'))
        self.assert_(self.authz.is_super_user('jiangxin') == True)
        self.assert_(self.authz.is_admin('&admin') == True)
        self.assert_(self.authz.is_admin('admin1') == False)
        self.assert_(self.authz.is_admin('admin1','repos1') == True)
        self.assert_(self.authz.is_admin('admin4','repos1') == False)
        self.assert_(self.authz.is_admin('admin1','repos2') == False)
        self.assert_(self.authz.is_admin('admin2','repos2') == True)
        self.assert_(self.authz.is_admin('admin10','repos2') == False)
        self.assert_(self.authz.is_admin('','repos3') == False)
        self.assert_(self.authz.is_admin('jiangxin','repos123') == True)

        # add_admin() test
        self.authz.set_admin('admin1,admin2')
        self.authz.set_admin(['admin1','admin2'],'repos1')
        # reposx does not exist.
        self.authz.set_admin('admin2','reposx')
        self.assert_(self.authz.is_admin('admin1','repos2') == True)


        # SvnAuthz __str__ test
        self.authz.update_revision()
        self.assert_(str(self.authz) ==
"""# version : 0.1.2
# admin : / = admin1, admin2
# admin : repos1 = admin1, admin2
# admin : repos2 = admin2
# admin : repos3 = admin3

[groups]
admin = &admin, admin1, admin2, admin3
admins = &007, &admin
all = @team1, user3, user4
team1 = @team2, user1, user11
team2 = @team3, user2, user22
team3 = user3, user33

[aliases]
007 = james
admin = jiangxin

[/]
user3 = r
user4 = r

[/branches]
$authenticated = r
@admins = rw

[/tags]
* = 
@admins = rw
@all = r

[/trunk]\nuser2 = 

[/trunk/src]
user1 = r
user2 = r

[repos1:/]
@admins = rw
user3 = 

[repos1:/trunk]
user1 = r
user2 = 

[repos1:/trunk/src]
&007 = r
user1 = 

""", (repr(str(self.authz))))

        self.assert_(self.authz.check_rights('user1','repos1','/trunk/src/test','r') == False)
        self.assert_(self.authz.check_rights('user1','GLOBAL','/trunk/src/test','r') == True)
        self.assert_(self.authz.check_rights('user2','repos1','/trunk/src/test','r') == True)
        self.assert_(self.authz.check_rights('user2','repos1','/trunk','r') == False)
        self.assert_(self.authz.check_rights('user2','GLOBAL','/trunk','r') == False)
        self.assert_(self.authz.check_rights('user3','repos1','/trunk','r') == False)
        self.assert_(self.authz.check_rights('user4','repos1','/trunk','r') == True)
        self.assert_(self.authz.check_rights('user4','GLOBAL','/trunk','r') == True)
        self.assert_(self.authz.check_rights('user5','GLOBAL','/trunk','r') == False, self.authz.check_rights('user5','GLOBAL','/trunk','r'))

        self.assert_(self.authz.check_rights('user5','GLOBAL','/branches/a/b/c','r') == True)

        self.assert_(self.authz.get_access_map("", "reposnoexist", descend=False)==None,
                     self.authz.get_access_map("", "reposnoexist", descend=False))
         
        self.assert_(self.authz.get_access_map_msgs('jiangxin', 'reposnoexist') == 
["""
==================================================
Access map on 'reposnoexist' for user 'jiangxin'
==================================================
  * Writable:
    /branches
    /tags
----------------------------------------
  * Readable:
    
----------------------------------------
  * Denied:
    /
    /trunk
    /trunk/src
----------------------------------------
"""], repr(self.authz.get_access_map_msgs('jiangxin', 'reposnoexist')))


        self.assert_(self.authz.get_access_map_msgs('  ', abbr=True) == 
["""
* => [/]
----------------------------------------
RW: 
RO: 
XX: /, /branches, /tags, /trunk, /trunk/src

""", 
"""
* => [repos1]
----------------------------------------
RW: 
RO: 
XX: /, /branches, /tags, /trunk, /trunk/src

""",
"""
* => [repos2]
----------------------------------------
RW: 
RO: 
XX: /, /branches, /tags, /trunk, /trunk/src

""",
"""
* => [repos3]
----------------------------------------
RW: 
RO: 
XX: /, /branches, /tags, /trunk, /trunk/src

"""]
, repr(self.authz.get_access_map_msgs('  ', abbr=True)))

        self.assert_(self.authz.get_path_access_msgs('jiangxin', 'repos2', '/trunk/src/mod1') == ['User jiangxin can *NOT* access to module repos2:/trunk/src/mod1'],
                     self.authz.get_path_access_msgs('jiangxin', 'repos2', '/trunk/src/mod1'))

        self.assert_(self.authz.get_path_access_msgs(' ', '*', '/trunk/src/mod1', abbr=True) == 
                     [u'[/:/trunk/src/mod1] * =', u'[repos1:/trunk/src/mod1] * =', u'[repos2:/trunk/src/mod1] * =', u'[repos3:/trunk/src/mod1] * ='],
                     self.authz.get_path_access_msgs(' ', '*', '/trunk/src/mod1', abbr=True))

if __name__ == '__main__': 
    import unittest
    unittest.main()

