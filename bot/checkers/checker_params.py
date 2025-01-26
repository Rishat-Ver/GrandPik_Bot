def chek_params_integer(params):
    try:
        int(params)
        return True
    except:
        return False