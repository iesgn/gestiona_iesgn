% include('header.tpl',info=info)
% from gestiona import tipos
 <h3>Búsqueda</h3>
 <form action="/usuarios" method="post" class="form-horizontal">
        <div class="form-group">
            <label for="nombre" class="control-label col-xs-2">Nombre:</label>
            <div class="col-xs-4">
                <input name="q" type="text" value="{{info["params"].get("q")}}" class="form-control" id="q" placeholder="Nombre...">
            </div>
        </div>
        <div class="form-group">
            <label for="inputPassword" class="control-label col-xs-2">Tipo:</label>
            <div class="col-xs-4">
                <select name="t" class="form-control">
                % for i in xrange(0,9):
                % if info["params"].get("t")==str(i):
                  <option selected="selected" value="{{i}}">{{tipos(str(i))}}</option>
                %else:
                  <option value="{{i}}">{{tipos(str(i))}}</option>
                % end
                % end
                </select>
                
        </div>
        </div>
        
        <div class="form-group">
            <div class="col-xs-offset-2 col-xs-10">
                <button type="submit" class="btn btn-primary">Buscar</button>
            </div>
        </div>
    </form>
    <hr/>
    <a href="/usuarios/add"><button type="submit" class="btn btn-primary">Nuevo usuario</button></a>
 

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
      <<!--<td><a href="usuarios/borrar/{{r.get_attr_values('uid')[0]}}"><span class="glyphicon glyphicon-remove-sign" aria-hidden="true"></span></a></td>-->
      <button type="button" class="btn btn-primary" data-toggle="modal" data-target=".bs-example-modal-sm"><span class="glyphicon glyphicon-remove-sign" aria-hidden="true"></span></button>
    </tr>
    % end
    </table>

	
% include('footer.tpl',info=info)