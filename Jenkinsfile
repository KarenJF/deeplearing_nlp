pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'building'

                //echo "PYTHONPATH is $PYTHONPATH"
                echo "1 HOME is: $HOME"
                echo "1 PATH is: $PATH"
                echo "1 Workspace is: $WORKSPACE"

                // JENKINSHOME is just a name to help readability
                withPythonEnv(
                    //['/Library/Frameworks/Python.framework/Versions/3.8/bin/python3.8+JENKINSHOME=/home/jenkins/bin']
                    //'/Users/pho/venv/bin/python'
                    //'/Library/Frameworks/Python.framework/Versions/3.8/bin/python3.8'
                    //'/Library/Frameworks/Python.framework/Versions/3.8/bin/python3'
                    //'/Library/Frameworks/Python.framework/Versions/3.8/bin'
                    //'../../venv/bin/python'
                    //"HOME=${env.WORKSPACE}"
                    //'${env.WORKSPACE}'+'/venv/bin/python' -- DOES NOT WORK
                    //'/Users/pho/.jenkins/workspace/SimplePipeline SCM/venv/bin/python'
                    '/usr/local/Cellar/python@3.9/3.9.6/bin/python3.9'
                    ){

                    echo "===== INSIDE 1 ====="

                    sh 'python --version'
                    sh 'python3 --version'

                    sh 'python3 -m venv env'
                    sh 'source ./env/bin/activate'
                    //sh 'python -m pip install requests'
                    //sh 'python -m pip install pandas'

                    //sh 'source Users/pho/.jenkins/workspace/SimplePipeline SCM/venv/bin/activate'
                    //sh 'source /venv/bin/activate'
                    sh 'python3 -m pip install requests'

                    //sh 'pip install --user -r requirements.txt'
                    //source flask/bin/activate

                    echo "===== INSIDE 2 ====="

                    echo "2 PATH is: $PATH"
                    echo "2 Workspace is: $WORKSPACE"

                    sh 'python ./services/caselaw/GetDataFromCaseLaw.py'

                    //sh 'source deactivate'
                }

                echo "===== OUTSIDE ====="
                sh 'python --version'
                sh 'python3 --version'

                // https://stackoverflow.com/questions/17309288/importerror-no-module-named-requests
                //sh 'python3 -m pip install requests'
                //sh '/usr/local/bin/pip3 install requests'
                // https://stackoverflow.com/questions/44629443/unable-to-use-pip-inside-jenkins
                // https://stackoverflow.com/questions/44378221/export-command-in-jenkins-pipeline/44380495#44380495
                //sh 'PATH=$PATH:/usr/local/bin'
                //echo "3 PATH is: $PATH"

                //sh 'pip install requests'
                //sh 'python3 ./services/caselaw/GetDataFromCaseLaw.py'
            }
        }
    }
}