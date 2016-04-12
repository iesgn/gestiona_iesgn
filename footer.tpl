<div class="col-md-4">
  <%
  a=False
  if a:
    include('login.tpl')
  else:
    include('menu.tpl')
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
    <script src="static/bootstrap/assets/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>
