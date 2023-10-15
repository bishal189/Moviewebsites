import subprocess
import crypt

def CreateUser(username):
    username=username
    password=username
    encrypted_password=crypt.crypt(password)
    resultuser= subprocess.run(["sudo","useradd","-m",username])
    resultpass=subprocess.run(['sudo','usermod','-p',encrypted_password,username])

