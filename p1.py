###Authentication###For authenticating into your sharepoint site###
ctx_auth = AuthenticationContext(url_shrpt)
if ctx_auth.acquire_token_for_user(username_shrpt, password_shrpt):
  ctx = ClientContext(url_shrpt, ctx_auth)
  web = ctx.web
  ctx.load(web)
  ctx.execute_query()
  print('Authenticated into sharepoint as: ',web.properties['Title'])

else:
  print(ctx_auth.get_last_error())
############################
  