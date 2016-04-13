% include('header.tpl',info=info)
% from gestiona import tipos
 <h3>Nuevo usuario</h3>
 <form action="/usuarios/add" method="post" class="form-horizontal">
        <div class="form-group">
            <label for="nombre" class="control-label col-xs-2">Nombre:</label>
            <div class="col-xs-4">
                <input name="q" type="text" class="form-control" id="q" placeholder="Nombre...">
            </div>
        </div>
        <div class="form-group">
            <label for="inputPassword" class="control-label col-xs-2">Tipo:</label>
            <div class="col-xs-4">
                <select name="t" class="form-control">
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