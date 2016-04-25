<br/>
<div class="center-block btn-group-vertical" role="group" aria-label="...">
    <p class="text-center"><strong>Bienvenid@ {{info["login"]}}</strong></p>
    <p class="text-center"><strong>Menú</strong></p>
    % import sesion
    % if sesion.isprofesor():
 	<a class="btn btn-default" href="/usuarios" role="button">Usuarios</a>
  	<a class="btn btn-default" href="/ordenadores" role="button">Ordenadores</a>
  	% end
  	<a class="btn btn-default" href="/usuarios/modificar/{{info["login"]}}" role="button">Tu Perfil</a>
  	<a class="btn btn-default" href="/logout" role="button">Desconectar</a>
</div>
