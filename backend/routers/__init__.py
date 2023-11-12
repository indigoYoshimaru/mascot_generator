def get_all_routers(): 
    from . import health, user, txt2img
    all_routers = [health.router, user.router, txt2img.router]
    return all_routers