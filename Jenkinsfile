pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "YOUR_DOCKERHUB_USERNAME/aceest-fitness"
        IMAGE_TAG = "${env.BUILD_ID}"
        SONARQUBE_SCANNER = tool 'SonarQubeScanner' // Ensure this tool is configured in Jenkins
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/YOUR_GITHUB_USERNAME/aceest_fitness_gym.git'
            }
        }

        stage('Unit Tests (Pytest)') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pytest -v
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQubeServer') { // Name of your SonarQube server in Jenkins config
                    sh "${SONARQUBE_SCANNER}/bin/sonar-scanner"
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Docker Build & Push') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-creds') {
                        def customImage = docker.build("${DOCKER_IMAGE}:${IMAGE_TAG}")
                        customImage.push()
                        customImage.push("latest") // Tag as latest for the stable K8s manifest
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    # Update the image tag in the deployment manifest dynamically
                    sed -i "s|YOUR_DOCKERHUB_USERNAME/aceest-fitness:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|g" k8s/deployment-rolling.yaml

                    # Apply configurations to cluster
                    kubectl apply -f k8s/deployment-rolling.yaml
                    kubectl apply -f k8s/service.yaml

                    # Check deployment rollout status
                    kubectl rollout status deployment/aceest-app-deployment
                '''
            }
        }
    }

    post {
        failure {
            echo "Pipeline failed. Rolling back Kubernetes deployment..."
            sh "kubectl rollout undo deployment/aceest-app-deployment"
        }
    }
}