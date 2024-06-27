import subprocess

def switch_git_user(username, email):
    subprocess.run(['git', 'config', '--global', 'user.name', username])
    subprocess.run(['git', 'config', '--global', 'user.email', email])
    print(f'Switched Git user to {username} <{email}>')
