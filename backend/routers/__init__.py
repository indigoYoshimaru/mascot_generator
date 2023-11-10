def get_all_routers(): 
    from . import health, user
    all_routers = [health.router, user.router]
    return all_routers