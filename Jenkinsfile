def buildClosure = {
  stage('Install')
  // sh 'virtualenv -p `which python3` venv --always-copy'
  // sh 'source venv/bin/activate'
  // sh 'pip3 install -r requirements.txt'

  // Do tests
  // Todo: implement
}

def buildParameterMap = [:]
buildParameterMap['appName'] = 'sampleApplication'
buildParameterMap['buildClosure'] = buildClosure
buildParameterMap['namespaces'] = ['app-dev']
buildParameterMap['namespacesWithApproval'] = ['app-prd']

buildAndDeployGeneric(buildParameterMap)