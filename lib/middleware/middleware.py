import argparse

# specific middleware should not never modify args.middleware

def setup_middleware(parser : argparse.ArgumentParser):
    parser.set_defaults(middleware = [])

def add_middleware(parser : argparse.ArgumentParser, f):
    middleware = parser.get_default("middleware")
    assert(type(middleware) == list)
    middleware.append(f)
    parser.set_defaults(middleware = middleware)
