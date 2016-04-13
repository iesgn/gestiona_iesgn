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
      {{r.get_attr_values("gidnumber")[0]}}
      
    % end
    </table>

	
% include('footer.tpl',info=info)