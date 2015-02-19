def get_auth_token():
	auth = open('auth.txt', 'r')
	a = auth.read()
	return a