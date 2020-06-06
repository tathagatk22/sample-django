pipeline {
    environment {
        registry = "docker.io/tathagatk22/django-app"
        registryCredential = 'docker-tathagatk22'
        dockerImage = ''
        gitCredential = 'git-tathagatk22'
        githubRepo = "https://github.com/tathagatk22/sample-django.git"
        githubDeployRepo = "https://github.com/tathagatk22/sample-django-hpa.git"
    }
    agent any
    parameters {
		choice(
            choices: 
            [
                'branch', 
                'commit'
            ],
            description: 'Please select branch or commit to checkout from.', 
            name: 'selection'
        )
		string(
            description: 'Please insert valid input', 
            name: 'selection_value',
            trim: true,
            defaultValue: 'master',
        )
        choice(
            choices: 
            [
                'Ubuntu-based', 
                'CentOS-based'
            ],
            description: 'Please select base OS to build from.', 
            name: 'selection_os'
        )
        choice(
            choices:
            [
                'True',
                'False'
            ],
            description: 'Please select True to deploy this build on Kubernetes Cluster.',
            name: 'deployment_value'
        )
	}
    stages {
        stage('Git checkout from Branch') {
            when {
                expression { params.selection == 'branch' }
            }
            steps {
                script {
					if (params.selection_value == '') {
						currentBuild.result = 'ABORTED'
						error("Build failed because of blank input.")
					}
				}
                git url: "$githubRepo", branch: "${selection_value}", credentialsId: gitCredential
            }
        }
        stage('Git checkout from Commit') {
            when {
                expression { params.selection == 'commit' }
            }
            steps {
                script {
					if (params.selection_value == '') {
						currentBuild.result = 'ABORTED'
						error("Build failed because of blank input.")
					}
				}
                git url: "$githubRepo", credentialsId: gitCredential
                sh 'git checkout ' + "${selection_value}"
            }
        }
        stage('Building image CentOS') {
            when {
                expression { params.selection_os == 'CentOS-based' }
            }
            environment {
               COMMIT = sh(script: 'git rev-parse --short HEAD', , returnStdout: true).trim()
               BRANCH = sh(script: 'git rev-parse --abbrev-ref HEAD', , returnStdout: true).trim()
           }
            steps{
                script {
                    dockerImage = docker.build("$registry:${COMMIT}", "--build-arg COMMIT=${COMMIT}  --build-arg BRANCH=${BRANCH} -f Dockerfile-python-centos ." )
                }
            }
        }
        stage('Building image Ubuntu') {
            when {
                expression { params.selection_os == 'Ubuntu-based' }
            }
            environment {
               COMMIT = sh(script: 'git rev-parse --short HEAD', , returnStdout: true).trim()
               BRANCH = sh(script: 'git rev-parse --abbrev-ref HEAD', , returnStdout: true).trim()
           }
            steps{
                script {
                    dockerImage = docker.build("$registry:$BUILD_NUMBER", "--build-arg COMMIT=${COMMIT}  --build-arg BRANCH=${BRANCH} -f Dockerfile-python-ubuntu ." )
                }
            }
        }
        stage('Publish Image') {
            steps{
                script {
                    docker.withRegistry( '', registryCredential ) {
                        dockerImage.push()
                    }
                }
            }
        }
        stage('Delete Image') {
            steps{
                sh "docker rmi $registry:$BUILD_NUMBER"
            }
        }
        stage('Deploying on Kubernetes'){
            when {
                    expression { params.deployment_value == 'True' }
                }
            steps{
                script {
                    git url: "$githubDeployRepo" 
                    withCredentials([usernamePassword(credentialsId: "${registryCredential}", usernameVariable: 'username', passwordVariable: 'password')])
                    {
                        sh (script: "kubectl delete secret --ignore-not-found regcred")
                        sh (script: "kubectl apply secret docker-registry regcred --docker-server=docker.io --docker-username=$username --docker-password=\"$password\" ")
                        sh (script: "kubectl apply -f .")  
                        sh (script: "kubectl set image deployment/sample-django-deployment sample-django=$registry:$BUILD_NUMBER --record")
                    }                    
                }
            }
        }
    }
}
