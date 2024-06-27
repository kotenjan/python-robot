![Project Screenshot](datafiles/Screenshot_2024-06-27_102719.png)


# Python Robot

This project leverages Docker Compose to build an environment that communicates with the Pepper robot, manufactured by SoftBank Robotics. The robot's primary function is to build a tower from objects placed in front of it.

## Features

- **Tower Building:** The robot uses its arm to construct towers from objects.
- **Simulation:** A simulator for robotic arm manipulation is available in a Jupyter Notebook [Demo](testing.ipynb).
- **Video Demonstration:** [Watch the demo video](datafiles/demo.mp4).

## Requirements

- **Naoki SDK:** You need the full version of the Naoki SDK, named `python-sdk.tar.gz`, placed in the `.devcontainer/builder` directory.

## Installation

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/kotenjan/python-robot.git
    cd python-robot
    ```

2. **Setup Docker Environment:**
    Ensure Docker and Docker Compose are installed on your system. Follow the [Docker installation guide](https://docs.docker.com/get-docker/) if needed.

3. **Add Naoki SDK:**
    Place the `python-sdk.tar.gz` file into the `.devcontainer/builder` directory.

4. **Build and Start the Docker Containers:**
    ```bash
    docker-compose up --build
    ```

## Usage

- **Running the Simulator:**
    Open the `testing.ipynb` Jupyter Notebook to interact with the robotic arm simulator.

- **Scripts Overview:**
    - `camera.py`: Handles camera input and processing.
    - `chess_board.py`: Manages chessboard recognition and interactions.
    - `constants.py`: Stores constant values used across the project.
    - `controller.py`: Controls the robot's movements and actions.
    - `get_names.py`: Retrieves object names.
    - `get_position.py`: Computes the positions of objects.
    - `hello.py`: Initial test script.
    - `image_recognition.ipynb`: Notebook for image recognition tasks.
    - `image_recognition.py`: Script for image recognition.
    - `matrices.py`: Handles matrix computations.
    - `metric.py`: Computes various metrics.
    - `movement.py`: Manages the robot's movements.
    - `position_computation_genetic.py`: Computes positions using genetic algorithms.
    - `positions.py`: Handles position-related computations.

## Contributing

Contributions are welcome! Please create a new branch for your feature or bug fix and submit a pull request for review.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
