from pyngrok import ngrok

def connect_kth():
    ngrok.set_auth_token("2L8HAmFcPl5Hzx54YpW2MJxwxMA_69Tr2NsnvBowAhrQ71YsB")
    http_tunnel = ngrok.connect("student-shell.sys.kth.se:8013")
    ssh_tunnel = ngrok.connect(80, "tcp")
    return ssh_tunnel, http_tunnel