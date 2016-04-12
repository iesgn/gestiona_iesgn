<form action="/login" method="post" class="form-signin">
  <h4 class="form-signin-heading">Login</h4>
  % if info.has_key("error"):
    <h3 class="bg-danger">Error en login.</h3>
  % end
  <label for="inputEmail" class="sr-only">Usuario</label>
  <input type="text" name="username" id="inputText" class="form-control" placeholder="Usuario" required autofocus>
  <label for="inputPassword" class="sr-only">Password</label>
  <input type="password" name="password" id="inputPassword" class="form-control" placeholder="Password" required>
  <!--<div class="checkbox">
          <label>
            <input type="checkbox" value="remember-me"> Recuérdame
          </label>
        </div>-->
  <button class="btn btn-lg btn-primary btn-block" type="submit">Entrar</button>
</form>
