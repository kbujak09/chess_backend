def validate_register(username, password, confirm_password):
  if len(username) < 4:
    return 'Username must be at least 4 characters'
  if len(username) > 16:
    return "Username can't be longer than 16 characters"
  if len(password) <= 6:
    return "Password must be at least 6 characters"
  if password != confirm_password:
    return "Passwords doesn't match"
  return True  