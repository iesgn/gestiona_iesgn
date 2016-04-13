% include('header.tpl',info=info)
 <h3>Búsqueda</h3>
 <form action="/pruebas" method="post" class="form-horizontal">
        % for field in info["form"]:
        <div class="form-group">
            
            {{field.label}}
            <div class="col-xs-4">
                {{field(class_="form-control")}}
            </div>
        </div>
        % end

        
        <div class="form-group">
            <div class="col-xs-offset-2 col-xs-10">
                <button type="submit" class="btn btn-primary">Login</button>
            </div>
        </div>
    </form>

 

 <br/><h2>Prueba</h2>


	
% include('footer.tpl',info=info)