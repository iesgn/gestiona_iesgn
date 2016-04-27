% include('header.tpl',info=info)
% from gestiona import tipos
 <h3>Asignación masiva de tipo de usuarios</h3>
 <form action="/usuarios/tipo/" method="post" class="form-horizontal">
<div class="form-group">
            <label for="t" class="control-label col-xs-2">Tipo:</label>
            <div class="col-xs-4">
                <select name="description" class="form-control">
                % for i in xrange(0,9):
                <!--%   if str(i)==info["description"][0]:-->
                % if True:
                  <option value="{{i}}" selected>{{tipos(str(i))}}</option>
                     % else:
                  <option value="{{i}}">{{tipos(str(i))}}</option>
                      % end
               
                % end
                </select>
                
        </div>
 		<div class="form-group">
        
                <button type="submit" class="btn btn-primary">Seleccionar</button>
        
        </div>
     </div>
    </form>
    <hr/>
<form action="/usuarios/tipo/guardar" method="post" class="form-inline">
	<div class="form-group">
		
			<strong>Usuarios no asignados</strong><br/>
			<select  name="alu" id="alu" size="40">
				% for usu in info["no_asignado"]:
					<option value={{usu.split(",")[1]}}>{{usu.split(",")[0]}}</option>
				% end
			</select>
		
	</div>
		
		<div class="form-group">
			<input type="button" onclick=pasar(); value=">>">
		<br/><br/><br/>
		<input type="button" onclick=nopasar(); value="<<">
		</div>	
		
			
		
		<div class="form-group">
		
				<strong>1º ASIR</strong><br/>	
				<select  name="grup" id="grup" size="40">
				<option>Muñoz Rodríguez José Domingo</option>
			</select>
		
		</div>
			
		
	
</form>
% include('footer.tpl',info=info)
