## -*- coding: utf-8 -*-
<%inherit file="/base.mako" />

<%def name="head_tags()">
    <title>${_("Check Permissions")}</title>
</%def>

<%
userlist = [[_("Please choose..."), '...'], 
            [_("All users(with anon)"), '*'], 
            [_("Known users"), '$authenticated'], 
            [_("Anonymous"), '$anonymous'],]
for i in c.userlist:
    if i == '*' or i =='$authenticated' or i == '$anonymous':
        continue
    if i[0] == '@':
        userlist.append([_("Group:")+i[1:], i])
    elif i[0] == '&':
        userlist.append([_("Alias:")+i[1:], i])
    else:
        userlist.append([i, i])

reposlist = [[_("Please choose..."), '...'], [_("All repos"), '*']]
if '/' in c.reposlist:
	reposlist.append([_("Default"), '/'])
for i in c.reposlist:
    if i == '/':
        continue
    reposlist.append([i, i])

pathlist = [[_("All modules"), '*'],]
for i in c.pathlist:
    pathlist.append([i, i])
%>

<SCRIPT LANGUAGE="JavaScript">
function edit_username(form)
{
    form.userinput[1].checked = true;
}
function select_username(form)
{
    form.userinput[0].checked = true;
}
function edit_repos(form)
{
    form.reposinput[1].checked = true;
}
function select_repos(form)
{
    form.reposinput[0].checked = true;
}
function edit_path(form)
{
    form.pathinput[1].checked = true;
}
function select_path(form)
{
    form.pathinput[0].checked = true;
}
function update_path(form)
{
    var repos = "";
    var path = "";
    var type = "";
    if (form.reposinput[0].checked) {
        repos = form.reposselector.options[form.reposselector.selectedIndex].value;
    } else {
        repos = form.reposname.value;
    }
    if (form.pathinput) {
        if (form.pathinput[0].checked) {
        	if (form.pathselector.selectedIndex > -1)
            	path = form.pathselector.options[form.pathselector.selectedIndex].value;
            type = 'select';
        } else {
            path = form.pathname.value;
            type = 'manual';
        }
    }
    var params = {repos:repos, path:path, type:type};
    showNoticesPopup();
    new Ajax.Updater(
        'path', 
        '${h.url_for(controller="check", action="get_path_options")}', 
        {asynchronous:true, evalScripts:true, parameters: params});
    hideNoticesPopup();
}
</SCRIPT>

<h2>${_("Check Permissions")}</h2>

## Classic Form
##     ${h.form(h.url(action='permission'), method='post')}

## AJAX Form
<% 
    context.write( 
        h.form_remote_tag(
            html={'id':'checkform'}, 
            url=h.url(action='access_map'), 
            update=dict(success="acl_msg", failure="acl_error"), 
            method='post', before='showNoticesPopup()',
            complete='hideNoticesPopup();'+h.visual_effect("Highlight", "acl_msg", duration=1),
        )
    ) 
%>

<table>
<tr>
    <th>${_("Account")}</th>
    <th>${_("Repository")}</th>
    <th>${_("Modules")}</th>
</tr>

<tr>
    <td>
        <input type="radio" name="userinput" value="select" Checked>
            ${_("Select username")}
            <select name="userselector" size="1" onFocus="select_username(this.form)">
                ${h.options_for_select(userlist, c.selected_username)}
            </select><br/>
        <input type="radio" name="userinput" value="manual">
            ${_("Manual input")}
            <input type="text" name="username" size=15 maxlength=80 value="${c.typed_username}" 
                onFocus="edit_username(this.form)">
    </td>

    <td>
        <input type="radio" name="reposinput" value="select" Checked onClick="update_path(this.form)">
            ${_("Select repository")}
            <select name="reposselector" size="0" onFocus="select_repos(this.form)" 
                onChange="update_path(this.form)">
                ${h.options_for_select(reposlist, c.selected_repos)}
            </select><br/>
        <input type="radio" name="reposinput" value="manual"> 
            ${_("Manual input")}
            <input type="text" name="reposname" value="${c.typed_repos}" 
                onFocus="edit_repos(this.form)"
                onBlur="update_path(this.form)">
    </td>

    <td>
        <div id="path">
        ## classic form: ${c.path_options}
        </div>
    </td>
</tr>
</table>

<input type="submit" name="submit" value='${_("Check Permissions")}'>

${h.end_form()}

<hr size='0'>

## classic form: ${c.access_map_msg}

<div id='acl_msg'></div>
<div id='acl_error'></div>
