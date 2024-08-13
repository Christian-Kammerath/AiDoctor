import subprocess


# Created a Docker container with its own app from the extensions folder,
# which is used to ensure that access can only go through the server
def build_docker_image(image_name, dockerfile_path, sudo_password):
    try:
        result = subprocess.run(
            ['sudo', '-S', 'docker', 'build', '-t', image_name, '-f', dockerfile_path, '.'],
            input=sudo_password + '\n',
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"Successfully built Docker image: {image_name}")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while building Docker image: {e}")
        print("Standard output:", e.stdout)
        print("Error output:", e.stderr)
        return False
    return True


# starts the docker container
def run_docker_container(image_name, port_mapping, sudo_password):
    try:
        result = subprocess.run(
            ['sudo', '-S', 'docker', 'run', '-d', '-p', port_mapping, image_name],
            input=sudo_password + '\n',
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"Successfully started Docker container from image: {image_name}")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running Docker container: {e}")
        print("Standard output:", e.stdout)
        print("Error output:", e.stderr)
        return False
    return True
