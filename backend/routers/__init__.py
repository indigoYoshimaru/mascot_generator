def get_all_routers(): 
    from . import health
    all_routers = [health.router]
    return all_routers