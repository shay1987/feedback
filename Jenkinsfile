node {

    //Define all variables
    def project = 'feisty-deck-351210'
    def appName = 'feedback'
    def serviceName = "${appName}"  
    def imageTag = "gcr.io/${project}/${appName}"
    def buildnum = "1.0.${env.BUILD_NUMBER}"

    //Checkout Code from Git
    checkout scm

    //stage 1 : connect to gcr.
    stage('connecting') {
        sh("gcloud auth activate-service-account  jenkins-198@feisty-deck-351210.iam.gserviceaccount.com  --key-file=/var/jenkins_home/key.json")
        sh("gcloud auth configure-docker")
    }
    
    //master : Build the docker image.
    stage('Build image') {
        env.BRANCH_NAME == 'master'
        sh("docker build -t ${imageTag}:latest .")
        }
    
    //master : E2E testing
    stage('E2E testing') {
        env.BRANCH_NAME == 'master'
         sh 'echo test'
        }

    //master : Push the image to docker registry
    stage('Push image to registry') {
        env.BRANCH_NAME == 'master'
        sh("docker push ${imageTag}:latest ")
        sh("git add -f ${imageTag}:latest")
        sh('git commit -m "latest"')
        sh("git push -u origin master")
        }

    //feature build and test
    stage('feature build and test') {
        env.BRANCH_NAME == 'feature'
        sh("docker build -t ${imageTag}:${buildnum} .")
        sh("docker run -d ${imageTag}:${buildnum}")
        sh("python3 test.py")
        }

    //dev build and test
        stage('feature or dev build and test') {
        env.BRANCH_NAME == 'dev'
        sh("docker build -t ${imageTag}/snapshot:${buildnum} .")
        sh("docker run -d ${imageTag}/snapshot:${buildnum}")
        sh("python3 test.py")
        }
}