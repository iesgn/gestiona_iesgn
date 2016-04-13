% include('header.tpl',info=info)
% from gestiona import tipos
 <h3>Búsqueda</h3>
 <form action="/usuarios" method="get" class="form-horizontal">
        <div class="form-group">
            <label for="nombre" class="control-label col-xs-2">Nombre:</label>
            <div class="col-xs-4">
                <input name="givenname" type="text" class="form-control" id="inputEmail" placeholder="Search...">
            </div>
        </div>
        <div class="form-group">
            <label for="inputPassword" class="control-label col-xs-2">Tipo:</label>
            <div class="col-xs-4">
                <select name="tipo" class="form-control">
                % for i in xrange(0,9):
                  <option value="{{i}}">{{tipos(i)}}</option>
                % end
                </select>
                
        </div>
        </div>
        
        <div class="form-group">
            <div class="col-xs-offset-2 col-xs-10">
                <button type="submit" class="btn btn-primary">Login</button>
            </div>
        </div>
    </form>

 

 <br/><h2>Usuarios</h2>

<table class="table table-bordered">
    <tr><td>N.</td><td>A/P</td><td>Usuario (Login)</td><td>Tipo</td><td>Mod.</td><td>Borrar</td></tr>
    <% 
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