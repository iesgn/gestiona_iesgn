% include('header.tpl',info=info)

 <h3>Borrar usuario</h3>
 <form action="/usuarios/borrar/{{info["uid"]}}" method="post" class="form-horizontal">
        <div class="form-group">
            <p>¿Estás seguro de borrar el usuario {{info["uid"]}}?</p>
        </div>
        
        <div class="form-group">
            <div class="col-xs-offset-2 col-xs-10">
                <button name="respuesta" value="si" type="submit" class="btn btn-primary">Si</button>
            </div>
            <div class="col-xs-offset-2 col-xs-10">
                <button name="respuesta" value="no" type="submit" class="btn btn-primary">No</button>
            </div>
        </div>
    </form>
    
 

 

	
% include('footer.tpl',info=info)