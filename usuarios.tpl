% include('header.tpl',info=info)
 <form class="navbar-form navbar-left" role="search">
 	<div class="form-group">
    	<input type="text" class="form-control" placeholder="Search">
    </div>
    <button type="submit" class="btn btn-default">Submit</button>
</form>
<br/><h2>Usuarios</h2>
<table class="table table-bordered">
    <tr><td>N.</td><td>A/P</td><td>Uusario (Nombre de usuario) - Tipo</td><td>Mod.</td><td>Borrar</td></tr>
    % for r in info["resultados"]:
    <tr>
      <td></td>
      % if r.get_attr_values("uid")[0]=="2001":
        <td><span class="glyphicon glyphicon-user" aria-hidden="true"></td>
      % else:
        <td><span class="glyphicon glyphicon-education" aria-hidden="true"></td>
      % end  
      <td>{{r.get_attr_values("sn")+" "+r.get_attr_values("givenname") + " ("+r.get_attr_values("uid")+")"}}</td>

      <td><a href="usuarios/modificar/{{r.get_attr_values('uid')"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a></td>
      <td><a href="usuarios/borrar/{{r.get_attr_values('uid')"><span class="glyphicon glyphicon-remove-sign" aria-hidden="true"></span></a></td>
    </tr>
    % end
    </table>

	
% include('footer.tpl',info=info)