% include('header.tpl',info=info)
% from gestiona import tipos
 <h3>Nuevo usuario</h3>
 <form action="/usuarios/add" method="post" class="form-horizontal">
        <div class="form-group">
            <label for="uid" class="control-label col-xs-2">Usuario:</label>
            <div class="col-xs-4">
                <input name="uid" type="text" class="form-control" id="uid" placeholder="Usuario" required autofocus>
            </div>
        </div>
        <div class="form-group">
            <label for="password" class="control-label col-xs-2">Contraseña:</label>
            <div class="col-xs-4">
                <input name="userpassword" type="password" class="form-control" id="password" placeholder="Password" required>
            </div>
        </div>
        <div class="form-group">
            <label for="email" class="control-label col-xs-2">Email:</label>
            <div class="col-xs-4">
                <input name="mail" type="email" class="form-control" id="email" placeholder="Email" required>
            </div>
        </div>
        <div class="form-group">
            <label for="nombre" class="control-label col-xs-2">Nombre:</label>
            <div class="col-xs-4">
                <input name="givenname" type="text" class="form-control" id="nombre" placeholder="" required>
            </div>
        </div>
         <div class="form-group">
            <label for="apellidos" class="control-label col-xs-2">Apellidos:</label>
            <div class="col-xs-4">
                <input name="sn" type="text" class="form-control" id="apellidos" placeholder="" required>
            </div>
        </div>
        <div class="form-group">
            <label for="ciudad" class="control-label col-xs-2">Ciudad:</label>
            <div class="col-xs-4">
                <input name="localityname" type="text" class="form-control" id="ciudad" placeholder="" required>
            </div>
        </div>
        <div class="form-group">
            <label for="ap" class="control-label col-xs-2">Grupo:</label>
            <div class="col-xs-4">
                <select name="gidnumber" class="form-control">
                    <option value="2001">Alumno</option>
                    <option value="2000">Profesor</option>
               
                </select>
                
        </div>
        </div>
        
        <div class="form-group">
            <label for="t" class="control-label col-xs-2">Tipo:</label>
            <div class="col-xs-4">
                <select name="description" class="form-control">
                % for i in xrange(0,9):
               
                  <option value="{{i}}">{{tipos(str(i))}}</option>
               
                % end
                </select>
                
        </div>
        </div>
        
        <div class="form-group">
            <div class="col-xs-offset-2 col-xs-10">
                <button type="submit" class="btn btn-primary">Aceptar</button>
            </div>
        </div>
    </form>
    
 

 

	
% include('footer.tpl',info=info)