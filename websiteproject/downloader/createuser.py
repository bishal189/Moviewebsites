import subprocess
import crypt
import random
import string

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + '#@$'
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def CreateUser(username,user):
    # Check if the user already exists
    existing_user_check = subprocess.run(["id", username], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if existing_user_check.returncode == 0:
        # User already exists, return their existing password (if needed)
        print('user already exists')
        return user.user_password
        # return "User already exists"
    else:
        # User does not exist, generate a random password
        random_password = generate_random_password()
        encrypted_password = crypt.crypt(random_password)
        user.user_password=random_password
        user.save()

        # Create the new user
        result_user = subprocess.run(["sudo", "useradd", "-m", username])
        result_pass = subprocess.run(["sudo", "usermod", "-p", encrypted_password, username])

        # Return the generated random password
        return random_password
