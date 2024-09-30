try:
    import AutoRun
except ImportError as e:
    if "'AutoRun'" not in e.value:
        from lib.car import Car
        Car.Emergency_shutdown()
        raise
    # else just ignore it
except KeyboardInterrupt:
    raise
except:
    from lib.car import Car
    Car.Emergency_shutdown()
    raise
