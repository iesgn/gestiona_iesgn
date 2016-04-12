% include('header.tpl',info=info)
 <form class="navbar-form navbar-left" role="search">
 	<div class="form-group">
    	<input type="text" class="form-control" placeholder="Search">
    </div>
    <button type="submit" class="btn btn-default">Submit</button>
</form>
<br/><h2>Alumnos</h2>
<table class="table table-bordered">
    <tr><td>N.</td><td>A/P</td><td>Uusario (Nombre de usuario) - Tipo</td><td>Mod.</td><td>Borrar</td></tr>
    <tr>
      <td>1</td><td><span class="glyphicon glyphicon-user" aria-hidden="true"></td><td>Álvarez Moreno Josué (zozue49) - 1º ASIR
</td><td><a href="modificar.php?uid=zozue49"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>
</td><td><a href="borrar.php?uid=zozue49"><span class="glyphicon glyphicon-remove-sign" aria-hidden="true"></span></a>
</td>
  </tr>
    <tr>
      <td>2</td><td><span class="glyphicon glyphicon-education" aria-hidden="true"></td><td>Muñoz Rodríguez José Domingo - Profesor
</td><td><a href="modificar.php?uid=zozue49"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>
</td><td><a href="borrar.php?uid=zozue49"><span class="glyphicon glyphicon-remove-sign" aria-hidden="true"></span></a>
</td>
  </tr>
</table>

	
% include('footer.tpl',info=info)