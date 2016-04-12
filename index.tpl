% include('header.tpl')
<h1>Gestiona</h1>
	<h4>IES Gonzalo Nazareno - Departamento de Informática</h4>
        <p class="text-justify">Esta aplicación Web permite a los usuarios de los servicios ofrecidos por el Deparatamento de Informática del IES Gonzalo Nazareno (alumnos y profesores de los Ciclos Formátivos de Informática) a gestionar los datos de las cuentas. Antes de continuar introduce tu nombre de usuario y contraseña.</p>
        
      </div>
	<div class="col-md-4">
	<form class="form-signin">
        <h2 class="form-signin-heading">Login</h2>
        <label for="inputEmail" class="sr-only">Usuario</label>
        <input type="text" id="inputText" class="form-control" placeholder="Usuario" required autofocus>
        <label for="inputPassword" class="sr-only">Password</label>
        <input type="password" id="inputPassword" class="form-control" placeholder="Password" required>
        <div class="checkbox">
          <label>
            <input type="checkbox" value="remember-me"> Recuérdame
          </label>
        </div>
        <button class="btn btn-lg btn-primary btn-block" type="submit">Entrar</button>
      </form>
% include('footer.tpl')