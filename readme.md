# Open Data Ghana API

## Description
This project is a Python-based API that provides endpoints for managing users, datasets and tags. It is built using FastAPI and SQLAlchemy for database interactions.

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/FrankE01/OpenDataGhana-Backend.git
    cd OpenDataGhana-Backend
    ```
2. Create and activate a virtual environment using [UV](https://astral.sh/blog/uv):
    ```sh
    poetry shell
    ```
3. Install the dependencies:
    ```sh
    poetry install
    ```
4. Set up the environment variables:
    ```sh
    cp sample.env .env
    # Edit .env file with appropriate values
    ```

## Usage
1. Start the API server:
    ```sh
    uvicorn main:app --reload --reload-exclude '.*log'
    ```
2. Access the API documentation at `http://127.0.0.1:8000/docs`.

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License
This project is licensed under the MIT License.