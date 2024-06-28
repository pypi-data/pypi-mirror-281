import os


def create_structure(base_path):
    backend_path = os.path.join(base_path, 'backend')
    directories = [
        "api/controller",
        "client",
        "custom_enum",
        "dao",
        "db",
        "dto",
        "routes",
        "service",
        "utils",
        "vo"
    ]

    # Create the backend directory and add __init__.py to make it a package
    os.makedirs(backend_path, exist_ok=True)
    with open(os.path.join(backend_path, '__init__.py'), 'w') as f:
        pass  # create an empty __init__.py file

    # Create subdirectories inside the backend directory
    for directory in directories:
        path = os.path.join(backend_path, directory)
        os.makedirs(path, exist_ok=True)
        # with open(os.path.join(path, '__init__.py'), 'w') as f:
        #     pass  # create an empty __init__.py file


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate a backend project structure")
    parser.add_argument('path', nargs='?', default=os.getcwd(), help="The path where the structure will be created")
    args = parser.parse_args()

    base_path = args.path
    create_structure(base_path)
    print(f"Project structure created successfully at {base_path}")


if __name__ == "__main__":
    main()
