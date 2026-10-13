## Project Overview

**ACEest Fitness & Gym**
This repository demonstrates an enterprise-grade, end-to-end DevOps workflow featuring:
* **Application Framework:** Python Flask application powered by WSGI Gunicorn.
* **Unit Testing:** Automated unit testing using Pytest and `pytest-flask`.
* **Containerization:** Optimized Docker container running as a non-root compliant user (`appuser`).
* **Continuous Integration:** Automated build and test workflows via GitHub Actions.
* **Quality Gate & Build Server:** Declarative pipeline automation via a dedicated Linux Jenkins server.


## Repository Structure

aceest_fitness_gym/
├── .github/
│   └── workflows/
│       └── main.yaml          # GitHub Actions CI workflow definition
├── app.py                     # Main Flask REST API service
├── test_app.py                # Pytest unit test suite
├── Dockerfile                 # Production Docker build specification
├── .dockerignore              # Excluded context files for Docker builds
├── .gitignore                 # Git ignore rules for Python/virtual environments
├── requirements.txt           # Python dependencies
├── Jenkinsfile                # Jenkins declarative pipeline script
└── README.md                  # Project documentation
