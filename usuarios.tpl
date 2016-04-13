% include('header.tpl',info=info)
 <form action="/usuarios" method="post" class="navbar-form navbar-left" role="search">
 	<div class="form-group">
    	<input name="search" type="text" class="form-control" placeholder="Search">
    </div>
    <button type="submit" class="btn btn-default">Submit</button>
</form>
<br/><h2>Usuarios</h2>

<table class="table table-bordered">
    <tr><td>N.</td><td>A/P</td><td>Usuario (Login)</td><td>Tipo</td><td>Mod.</td><td>Borrar</td></tr>
    <% from gestiona import tipos
    cont=0
    for r in info["resultados"]:
    cont=cont+1 %>
    <tr>
      <td>{{cont}}</td>
      % if r.get_attr_values("gidnumber")[0]=="2001":
        <td><span class="glyphicon glyphicon-user" aria-hidden="true"></td>
      % else:
        <td><span class="glyphicon glyphicon-education" aria-hidden="true"></td>
      % end  
      <td>{{r.get_attr_values("sn")[0]+" "+r.get_attr_values("givenname")[0]}} ({{r.get_attr_values("uid")[0]}})</td>
      <td>{{tipos(r.get_attr_values("description")[0])}}</td>
      <td><a href="usuarios/modificar/{{r.get_attr_values('uid')[0]}}"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a></td>
      <td><a href="usuarios/borrar/{{r.get_attr_values('uid')[0]}}"><span class="glyphicon glyphicon-remove-sign" aria-hidden="true"></span></a></td>
    </tr>
    % end
    </table>

	
% include('footer.tpl',info=info)