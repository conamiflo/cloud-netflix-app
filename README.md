# Movie Management Web Application

This project involves developing a web application for storing and managing film content using AWS cloud services and cloud-native architecture. The application supports various user roles and functionalities, leveraging AWS services for scalability and reliability.

## Architecture

### Overview
- **Client Application**: A frontend web application allowing users to interact with the system. Developed using Angular.
- **Server Application**: A cloud-native application handling the business logic of the system. Built using AWS Lambda, S3, DynamoDB, SNS, and SQS.

### Key AWS Services
- **AWS Lambda**: Handles backend logic for content management and user interactions.
- **Amazon S3**: Stores film content and associated files.
- **Amazon DynamoDB**: Manages metadata and search functionality.
- **Amazon SNS**: Sends notifications to users about new content.
- **Amazon SQS**: Manages asynchronous communication between services.
- **AWS API Gateway**: Provides a RESTful API for client-server communication.
- **AWS CloudFormation / AWS CDK**: Manages infrastructure as code.

### Architecture Diagram
![Architecture Diagram]($diagram.drawio.png)

## Features

- **User Registration and Login**: Register and log in with AWS Cognito.
- **Content Management**: Upload, view, edit, and delete film content.
- **Content Search**: Find films by title, description, actors, and other metadata.
- **Content Download and Rating**: Download and rate films.
- **Subscription and Notifications**: Subscribe to content and receive updates.
- **Personalized Feed**: Get recommendations based on user interactions.
- **Transcoding**: Films are automatically transcoded into different resolutions.

## Setup and Usage

### Prerequisites
- AWS Account
- Node.js and npm
- Angular CLI

### Installation

1. **Clone the Repository and install backend dependencies**
   ```bash
   git clone https://github.com/conamiflo/netflix.git
   cd netflix-backend
   npm install -g aws-cdk
   npm install
2. **Deploy the backend stack**
   ```bash
   cdk deploy
2. **Install dependencies for frontend and run the application**
   ```bash
   cd netflix-frontend
   npm install
   ng serve

### Access the Application

1. Open your browser and navigate to `http://localhost:4200` to access the frontend application.

### User Registration and Login

1. Navigate to the registration or login page on the frontend application.
2. Follow the prompts to create a new account or log in to an existing one using AWS Cognito.

### Content Management

1. As an administrator, use the content management interface available on the frontend to:
   - **Upload**: Add new film content along with its metadata.
   - **View**: Browse and view details of available film content.
   - **Edit and Delete**: Modify or remove existing content as needed.

### Search and Browse Content

1. Use the search functionality provided on the frontend to find films by:
   - Title
   - Description
   - Actors
   - Other metadata

2. Browse the search results and view detailed information about selected films.

### Download and Rate Content

1. Select a film from the content list.
2. Use the download option to save the film content to your local device.
3. Provide a rating for the film based on your experience.

### Subscription and Notifications

1. Subscribe to content that interests you by using the subscription feature on the frontend.
2. Receive notifications about new content updates or changes via SNS.

### Personalized Feed

1. Access your personalized feed on the frontend, which is tailored based on your interactions and preferences.
2. View recommended films and content based on your past activity and subscriptions.

### Transcoding

1. The system automatically handles transcoding of films into different resolutions.
2. This process is managed in the background, and you can view films in your preferred resolution.

