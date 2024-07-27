# Docker MySQL Node.js React.js App

![App](https://raw.githubusercontent.com/kentik13/DevOPS/main/docker-mysql-nodejs-reactjs-app-reverseproxy/Thumbnail.png)

"Docker MySQL Node.js React.js Reverse Proxy App" is a complete example repository demonstrating the power of Docker and Docker Compose. This project emphasizes ease of use and effectiveness by showcasing how Docker containers can be used to deploy a full-stack application.

The repository includes a React.js frontend where users can input and submit their data. This data is securely sent to a Node.js backend server, which handles the processing and storage in a MySQL database. By leveraging Docker Compose, the entire application stack—comprising the frontend, backend, and database—can be seamlessly orchestrated and managed within isolated containers.

## Setup

To set up the project, follow the steps below:

### Prerequisites

Before running the project, make sure you have the following installed:

- Docker: [Download and Install Docker](https://docs.docker.com/get-docker/)

### Installation

1. Clone the repository:

   ```bash
   git clone [https://github.com/kentik13](https://github.com/kentik13/DevOPS.git)
   ```

2. Navigate to the project directory:

   ```bash
   cd project-directory && cd docker-mysql-nodejs-reactjs-app-reverseproxy
   ```

3. Run the following command to build and start the Docker containers:

   ```bash
   docker-compose up --build
   ```

4. Access the application by opening the following URL in your web browser:

   ```
   http://localhost:80
   ```

   This will take you to the ReactJS application interface where you can interact with the project.

## Usage

This example serves as a beginner-friendly resource to learn about full-stack Docker containerization in a practical application. It provides a simplified implementation of a full-stack application using React.js, Node.js, MySQL, and Reverse Proxy all orchestrated with Docker Compose.
