import typer
import os
import shutil
import stat

app = typer.Typer()

@app.callback()
def callback():
    """
    Awesome Portal Gun
    """


@app.command()
def init():
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    if not os.path.isdir('./.git/hooks/todo'):
        os.makedirs('./.git/hooks/todo')
    if not os.path.isdir('./.git/hooks/current'):
        os.makedirs('./.git/hooks/current')
    if not os.path.isdir('./.git/hooks/done'):
        os.makedirs('./.git/hooks/done')
    shutil.copyfile(f'{dir_path}/cat1.txt' ,'./.git/hooks/todo/cat1.txt')
    shutil.copyfile(f'{dir_path}/cat2.txt','./.git/hooks/todo/cat2.txt')
    shutil.copyfile(f'{dir_path}/runsticker.py', './.git/hooks/post-commit')
    st = os.stat('./.git/hooks/post-commit')
    os.chmod('./.git/hooks/post-commit', st.st_mode | stat.S_IEXEC)
    """
    Shoot the portal gun
    """
    typer.echo("setting up hook")

@app.command()
def addsticker(filepath):
    filename = filepath.split('/')[-1]
    os.popen(f'cp {filepath} ./.git/hooks/todo/{filename}')