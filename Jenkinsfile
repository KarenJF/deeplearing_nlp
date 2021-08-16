// This is the configuration file for Jenkins, ie Jenkins will perform actions according to this file
// Articles:
// https://www.vogella.com/tutorials/Jenkins/article.html
// https://mightywomble.medium.com/jenkins-pipeline-beginners-guide-f3868f715ed9
// https://www.jenkins.io/doc/pipeline/examples/
// https://www.jenkins.io/doc/pipeline/tour/hello-world/
// https://gitlab.com/nanuchi/techworld-js-docker-demo-app/-/blob/dev/Jenkinsfile
// https://github.com/patebija/simple-python-pyinstaller-app/blob/master/Jenkinsfile

pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'building stage'

                echo "1 HOME is: $HOME"
                echo "1 PATH is: $PATH"
                echo "1 Workspace is: $WORKSPACE"

                // NOTES on how to configure python environment
                // https://github.com/jenkinsci/pyenv-pipeline-plugin
                // https://stackoverflow.com/questions/56006353/using-jenkins-environment-variable-in-pipeline-sh-script
                // https://stackoverflow.com/questions/21103727/how-to-tell-jenkins-to-use-a-particular-virtualenv-python/42650694
                // https://stackoverflow.com/questions/39176832/how-to-fix-python-module-import-errors-in-jenkins
                // https://gist.github.com/jubel-han/0e669dbbfa9e966f0b79a91730edc806
                withPythonEnv(
                    //'/Users/pho/venv/bin/python'
                    //'/Library/Frameworks/Python.framework/Versions/3.8/bin/python3.8'
                    '/usr/local/Cellar/python@3.9/3.9.6/bin/python3.9'
                    ){

                    echo "===== INSIDE 1 ====="

                    // confirm python version
                    sh 'python --version'
                    sh 'python3 --version'

                    // use the python command of "-m venv" to make a new a virtual environment called "env"
                    sh 'python3 -m venv env'

                    // activate this the virtual environment called "env"
                    sh 'source ./env/bin/activate'

                    // install the packages the python scripts need on the Jenkins machine
                    sh 'pip install -r requirements.txt'
                    //sh 'python -m pip install requests'
                    //sh 'python -m pip install pandas'
                    sh 'python3 -m pip install requests'

                    echo "===== INSIDE 2 ====="

                    echo "2 PATH is: $PATH"
                    echo "2 Workspace is: $WORKSPACE"

                    // python script to pull data from CaseLaw
                    //sh 'python ./services/caselaw/GetSampleDataFromCaseLaw.py'
                    sh 'python services/caselaw/GetSampleDataFromCaseLaw.py'
                    //sh 'python ./services/caselaw/GetFullTextDataFromCaseLaw.py'

                }

                echo "===== OUTSIDE ====="
                sh 'python --version'
                sh 'python3 --version'

            }

        }

    }

}