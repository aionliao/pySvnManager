��    �      �              �  �   �  J   1  �  |       >   )     h     l     {     �     �     �     �  #   �     �     �  	   �            5   .  	   d  K   n  1   �     �     
     (     G     ^  
   e     p     �     �  H   �     �  $        )     /     M     j  �   �  �        �     �     �  ,         -  @   ?  &   �     �     �     �     �     �  ,   �     )     >  L   Y  2   �  @   �          !  (   -     V     ^     u     �     �     �     �     �     �  
   	       )   #     M     e  #   j     �     �     �  #   �     �     �  }   �  �   p     4     @     X     ^     x  
     S   �     �     �     
          4     I     V     ^  F   f     �  &   �     �     �  	      	   
       7   $     \  
   l     w     �     �  +   �  B   �     !     :     F     M  	   Z  5   d  8   �  -   �       `        u     �     �     �     �     �     �     �        !   -      O      a      w   #   �      �      �   
   �      �      !  ,   !     E!     _!     p!     |!     �!     �!     �!     �!  %   �!     �!  (   �!  ^   &"     �"     �"     �"     �"     �"     �"  k   �"  "   G#  l   j#     �#  C   �#  (   '$     P$  X  k$     �%     �%  k   �%     d&  4   �&  "   �&  !   �&     �&     �&     '     #'     ;'     N'     g'     |'  9   �'     �'     �'  5   (  0   7(  3   h(  <   �(  /   �(  2   	)  ?   <)  D   |)  H   �)     
*     *  2   /*  
   b*     m*  	   s*     }*     �*     �*     �*     �*     �*     �*  ,   �*     �*     +  �  %+  �   �,  J   M-  �  �-     +0  >   E0     �0     �0     �0     �0     �0     �0     �0  #   �0     1     
1  	   1      1     51  5   J1  	   �1  K   �1  1   �1     2     &2     D2     c2     z2  
   �2     �2     �2     �2  H   �2     3  $    3     E3     K3     i3     �3  �   �3  �   34     �4     �4     5  ,   5     I5  @   [5  &   �5     �5     �5     �5     �5     �5  ,   6     E6     Z6  L   u6  2   �6  @   �6     67     =7  (   I7     r7     z7     �7     �7     �7     �7     �7     �7     8  
   %8     08  )   ?8     i8     �8  #   �8     �8     �8     �8  #   �8     �8     �8  }   9  �   �9     P:     \:     t:     z:     �:  
   �:  S   �:     �:     ;     &;     3;     P;     e;     r;     z;  F   �;     �;  &   �;     �;     <  	   <  	   &<     0<  7   @<     x<  
   �<     �<     �<     �<  +   �<  B   �<     ==     V=     b=     i=  	   v=  5   �=  8   �=  -   �=     >  `   0>     �>     �>     �>     �>     �>     ?     ?     ?     0?  !   I?     k?     }?     �?  #   �?     �?     �?  
   �?     
@     #@  ,   4@     a@     {@     �@     �@     �@     �@     �@     �@  %   �@     �@  (   A  ^   BA     �A     �A     �A     �A     �A     �A  k   �A  "   cB  l   �B     �B  C   �B  (   CC     lC  X  �C     �D     �D  k   E     �E  4   �E  "   �E  !   �E     F     F     .F     ?F     WF     jF     �F     �F  9   �F     �F     G  5   G  0   SG  3   �G  <   �G  /   �G  2   %H  ?   XH  D   �H  H   �H     &I     8I  2   KI  
   ~I     �I  	   �I     �I     �I     �I     �I     �I     �I     �I  ,   �I     J     +J   
%(heading)s
Access map on '%(repos)s' for user '%(user)s'
%(heading)s
  * Writable:
%(write)s
%(sep)s
  * Readable:
%(read)s
%(sep)s
  * Denied:
%(deny)s
%(sep)s
 
%(user)s => [%(repos)s]
%(sep)s
RW: %(write)s
RO: %(read)s
XX: %(deny)s

 
You must provide proper options to commit-email.pl using the
configuration form for this plugin.

You can simply just provide the email_addr as the options.

  [options] email_addr [email_addr ...]

But to be more versitile, you can setup a path-based email 
notifier.

  [-m regex1] [options] [email_addr ...]
  [-m regex2] [options] [email_addr ...] 
  ...

Options:

-m regex              Regular expression to match committed path
--from email_address  Email address for 'From:' (overrides -h)
-r email_address      Email address for 'Reply-To:
-s subject_prefix     Subject line prefix
--diff n              Do not include diff in message (default: y)
 %s is referenced by [%s]. A pre-commit hook to detect case-insensitive filename clashes. ACL ACL management Account Add repository Admin user:  Administration logs Administrators: Alias %s is referenced by group %s. Alias: All modules All repos All users(with anon) Allow revprop change Allow user change commit-log or other rev-properties. Anonymous Apply plugin '%(plugin)s' on '%(repos)s' Failed. Error message:<br>
%(msg)s Apply plugin '%(plugin)s' on '%(repos)s' success. Are you sure to delete alias: Are you sure to delete group: Are you sure to delete module: Can not delete module  Cancel Change log Check Permissions Check commit log message Check permissions Check subversion client version. if version below 1.5.0, checkin denied. Clear message Click Ok to proceed, or click cancel Close Commit log check is disabled. Commit log check is enabled. Commit log size must > 0. Commit to the remote svn server, this repository is a readonly svn mirror.It is the svnsync admin's duty to synchronize svnsync server and mirror. Commit-log is the only rev-prop we allow to change. Because the changes of rev-prop can not be reverted back, administrator must setup email notification to record this irreversible action. Compare Compare revisions Compares between Conflict: plugin '%s' is modified by others. Create repository Create repository '%(repos)s' Failed. Error message:<br>
%(msg)s Create repository '%(repos)s' success. Current configuration Default Delete Delete alias failed: Delete alias successfully. Delete blank repository '%(repos)s' success. Delete group failed: Delete group successfully. Delete plugin '%(plugin)s' on '%(repos)s' Failed. Error message:<br>
%(msg)s Delete plugin '%(plugin)s' on '%(repos)s' success. Delete repository '%(repos)s' Failed. Error message:<br>
%(msg)s Denied Description Detect case-insensitive filename clashes Disable Email notify disabled. Email notify enabled. Enable Enable commit log check:  Enable email notify. Enable readonly mirror:  Enable trac post commit hook:  Error Traceback Exception: Fill this form Fixed ticket status (default is closed):  Fixed ticket's status:  Full Group %s is referenced by group %s. Group: Id Ignore recursive Input email notify configurations:  Install this plugin Installed hooks: Integrate subversion with trac: Commit log of subversion appends to trac tickets if subversion commit log contains ticket id. Integration Subversion with Mantis bugtracking. If commit-log has proper format (contains bugid), it will change bug status and append commint-log and code differ as comment of bug status change. Known users Loading, please wait... Login Login failed for user: %s Logout Loose mode Loose mode: permit checkin without svn:eol-style properity if no CRLF in text file. Mantis bugtracking integration Manual input Members list Minimal size of commit log:  Module %s not exist. Module Path: Module: Modules Must set svn:eol-style even if CRLF not in text file (in Unix format). Name Name (%s) contains invalid characters. Name is not given. Name is not string. New Alias New Group New alias name: New file must provide svn:eol-style if not binary file. New group name: New module New repository No module exist for %s:%s No path selected. No plugin has been deleted for '%(repos)s'. No rights selected! Please check proper rights for selected users. Not a valid username: %s Other users Page:  Parameters:  Password: Pattern which commit log must **NOT** match against:  Pattern which commit log must <b>NOT</b> match against:  Pattern which commit log must match against:  Permission denied. Permit checkin without svn:eol-style properity if is in Unix file format (no crlf in text file). Please choose... Please input module path. Please input repository name. Plugin name Plugin not fully implemented. ReadOnly Readonly Readonly mirror disabled. Readonly mirror enabled. Recursive group membership for %s Remove repository Remove selected hooks Repos %s already exists. Repos %s is not a blank repository. Repos management Repos root does not exist: %s Repository Repository %s not exist. Repository Name: Repository name in trac (default is blank):  Repository name in trac:  Repository name: Repository: Rev Role Management Role management Rollback Rollback failed: %s Rollback successfully to revision: %s Rollback to this revision Rollback to this revision, are you sure? SVN below 1.5.0 can not handle mergeinfo properly.It can mess up our automated merge tracking! Save Save failed. Select a role name: Select module Select repository Select username Send a notification email describing either a commit or a revprop-change action on a Subversion repository. Send email notify for commit event Some one maybe you, has modified the svn authz file by hands. Please save once to fix possible config error. Strict mode Strict mode: must have svn:eol-style even if not CRLF in text file. Subversion client version check (>1.5.0) Subversion readonly mirror Subversion services may host on a filename case-sensitive OS,
while client **may not** (Windows is case-insensitive). This may cause 'clash'.

- Detects new paths that 'clash' with existing, or other new, paths.
- Ignores existings paths that already 'clash'
- Exits with an error code, and a diagnostic on stderr, if 'clashes'
  are detected.
 Successfully delete module: Svnsync administrator:  This subversion repository is a svnsync readonly mirror. Nobody can checkin, except the svnsync admin user. Trac environment location:  Trac integration with subversion's post commit hook. Trac post commit hook is disabled. Trac post commit hook is enabled. Type Uninstalled hooks: Unknown rights:  Unknown rule format: %s Update ACL failed: Update ACL successfully. Update alias failed: Update alias successfully. Update failed! You are working on a out-of-date revision. Update group failed: Update group successfully. User %(user)s changed alias: %(alias)s. (rev:%(rev)s) User %(user)s changed authz rules. (rev:%(rev)s) User %(user)s changed group: %(grp)s. (rev:%(rev)s) User %(user)s delete alias: %(alias)s. (rev:%(rev)s,%(msg)s) User %(user)s delete authz rules. (rev:%(rev)s) User %(user)s delete group: %(grp)s. (rev:%(rev)s) User %(username)s can *NOT* access to module %(repos)s:%(path)s User %(username)s has Full (RW) rights for module %(repos)s:%(path)s User %(username)s has ReadOnly (RO) rights for module %(repos)s:%(path)s User %s logged in User %s logged out User must provide commit-log message when checkin. User name: User: Username: Users View history, revision Welcome When Who Why Wrong configuration. You can not delete yourself from admin list. mime-type and eol-style check repos '%s' not exist! Project-Id-Version: pysvnmanager 0.0.0
Report-Msgid-Bugs-To: EMAIL@ADDRESS
POT-Creation-Date: 2009-08-23 12:30+0800
PO-Revision-Date: 2010-06-03 20:45+0800
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language-Team: en <LL@li.org>
Plural-Forms: nplurals=2; plural=(n != 1)
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 0.9.5
 
%(heading)s
Access map on '%(repos)s' for user '%(user)s'
%(heading)s
  * Writable:
%(write)s
%(sep)s
  * Readable:
%(read)s
%(sep)s
  * Denied:
%(deny)s
%(sep)s
 
%(user)s => [%(repos)s]
%(sep)s
RW: %(write)s
RO: %(read)s
XX: %(deny)s

 
You must provide proper options to commit-email.pl using the
configuration form for this plugin.

You can simply just provide the email_addr as the options.

  [options] email_addr [email_addr ...]

But to be more versitile, you can setup a path-based email 
notifier.

  [-m regex1] [options] [email_addr ...]
  [-m regex2] [options] [email_addr ...] 
  ...

Options:

-m regex              Regular expression to match committed path
--from email_address  Email address for 'From:' (overrides -h)
-r email_address      Email address for 'Reply-To:
-s subject_prefix     Subject line prefix
--diff n              Do not include diff in message (default: y)
 %s is referenced by [%s]. A pre-commit hook to detect case-insensitive filename clashes. ACL ACL management Account Add repository Admin user:  Administration logs Administrators: Alias %s is referenced by group %s. Alias: All modules All repos All users(with anon) Allow revprop change Allow user change commit-log or other rev-properties. Anonymous Apply plugin '%(plugin)s' on '%(repos)s' Failed. Error message:<br>
%(msg)s Apply plugin '%(plugin)s' on '%(repos)s' success. Are you sure to delete alias: Are you sure to delete group: Are you sure to delete module: Can not delete module  Cancel Change log Check Permissions Check commit log message Check permissions Check subversion client version. if version below 1.5.0, checkin denied. Clear message Click Ok to proceed, or click cancel Close Commit log check is disabled. Commit log check is enabled. Commit log size must > 0. Commit to the remote svn server, this repository is a readonly svn mirror.It is the svnsync admin's duty to synchronize svnsync server and mirror. Commit-log is the only rev-prop we allow to change. Because the changes of rev-prop can not be reverted back, administrator must setup email notification to record this irreversible action. Compare Compare revisions Compares between Conflict: plugin '%s' is modified by others. Create repository Create repository '%(repos)s' Failed. Error message:<br>
%(msg)s Create repository '%(repos)s' success. Current configuration Default Delete Delete alias failed: Delete alias successfully. Delete blank repository '%(repos)s' success. Delete group failed: Delete group successfully. Delete plugin '%(plugin)s' on '%(repos)s' Failed. Error message:<br>
%(msg)s Delete plugin '%(plugin)s' on '%(repos)s' success. Delete repository '%(repos)s' Failed. Error message:<br>
%(msg)s Denied Description Detect case-insensitive filename clashes Disable Email notify disabled. Email notify enabled. Enable Enable commit log check:  Enable email notify. Enable readonly mirror:  Enable trac post commit hook:  Error Traceback Exception: Fill this form Fixed ticket status (default is closed):  Fixed ticket's status:  Full Group %s is referenced by group %s. Group: Id Ignore recursive Input email notify configurations:  Install this plugin Installed hooks: Integrate subversion with trac: Commit log of subversion appends to trac tickets if subversion commit log contains ticket id. Integration Subversion with Mantis bugtracking. If commit-log has proper format (contains bugid), it will change bug status and append commint-log and code differ as comment of bug status change. Known users Loading, please wait... Login Login failed for user: %s Logout Loose mode Loose mode: permit checkin without svn:eol-style properity if no CRLF in text file. Mantis bugtracking integration Manual input Members list Minimal size of commit log:  Module %s not exist. Module Path: Module: Modules Must set svn:eol-style even if CRLF not in text file (in Unix format). Name Name (%s) contains invalid characters. Name is not given. Name is not string. New Alias New Group New alias name: New file must provide svn:eol-style if not binary file. New group name: New module New repository No module exist for %s:%s No path selected. No plugin has been deleted for '%(repos)s'. No rights selected! Please check proper rights for selected users. Not a valid username: %s Other users Page:  Parameters:  Password: Pattern which commit log must **NOT** match against:  Pattern which commit log must <b>NOT</b> match against:  Pattern which commit log must match against:  Permission denied. Permit checkin without svn:eol-style properity if is in Unix file format (no crlf in text file). Please choose... Please input module path. Please input repository name. Plugin name Plugin not fully implemented. ReadOnly Readonly Readonly mirror disabled. Readonly mirror enabled. Recursive group membership for %s Remove repository Remove selected hooks Repos %s already exists. Repos %s is not a blank repository. Repos management Repos root does not exist: %s Repository Repository %s not exist. Repository Name: Repository name in trac (default is blank):  Repository name in trac:  Repository name: Repository: Rev Role Management Role management Rollback Rollback failed: %s Rollback successfully to revision: %s Rollback to this revision Rollback to this revision, are you sure? SVN below 1.5.0 can not handle mergeinfo properly.It can mess up our automated merge tracking! Save Save failed. Select a role name: Select module Select repository Select username Send a notification email describing either a commit or a revprop-change action on a Subversion repository. Send email notify for commit event Some one maybe you, has modified the svn authz file by hands. Please save once to fix possible config error. Strict mode Strict mode: must have svn:eol-style even if not CRLF in text file. Subversion client version check (>1.5.0) Subversion readonly mirror Subversion services may host on a filename case-sensitive OS,
while client **may not** (Windows is case-insensitive). This may cause 'clash'.

- Detects new paths that 'clash' with existing, or other new, paths.
- Ignores existings paths that already 'clash'
- Exits with an error code, and a diagnostic on stderr, if 'clashes'
  are detected.
 Successfully delete module: Svnsync administrator:  This subversion repository is a svnsync readonly mirror. Nobody can checkin, except the svnsync admin user. Trac environment location:  Trac integration with subversion's post commit hook. Trac post commit hook is disabled. Trac post commit hook is enabled. Type Uninstalled hooks: Unknown rights:  Unknown rule format: %s Update ACL failed: Update ACL successfully. Update alias failed: Update alias successfully. Update failed! You are working on a out-of-date revision. Update group failed: Update group successfully. User %(user)s changed alias: %(alias)s. (rev:%(rev)s) User %(user)s changed authz rules. (rev:%(rev)s) User %(user)s changed group: %(grp)s. (rev:%(rev)s) User %(user)s delete alias: %(alias)s. (rev:%(rev)s,%(msg)s) User %(user)s delete authz rules. (rev:%(rev)s) User %(user)s delete group: %(grp)s. (rev:%(rev)s) User %(username)s can *NOT* access to module %(repos)s:%(path)s User %(username)s has Full (RW) rights for module %(repos)s:%(path)s User %(username)s has ReadOnly (RO) rights for module %(repos)s:%(path)s User %s logged in User %s logged out User must provide commit-log message when checkin. User name: User: Username: Users View history, revision Welcome When Who Why Wrong configuration. You can not delete yourself from admin list. mime-type and eol-style check repos '%s' not exist! 