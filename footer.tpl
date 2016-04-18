</div>
<div class="col-md-4">
  <%
  import sesion 
  if not sesion.islogin():
    include('login.tpl',info=info)
  else:
    include('menu.tpl',info=info)
  end
  %>
	</div>
	</div>
      

      <!-- Site footer -->
      <footer class="footer">
        <p>&copy; 2016 IESGN (dit)</p>
      </footer>

    </div> <!-- /container -->


    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="/static/bootstrap/assets/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>
