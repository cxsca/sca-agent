library "pipelineUtils"

def scaAgentZip

pipeline {
    parameters {
        booleanParam(name: 'releaseNewVersion', defaultValue: false, description: 'Create a public GitHub release')
    }
    agent {
        node {
            label 'docker'
        }
    }
    options {
        timestamps()
        disableConcurrentBuilds()
    }
    environment {
            VERSION = pipelineUtils.getSemanticVersion(0, 3)
    }
    stages{
        stage("Bundle") {
            steps {
                script{
                    scaAgentZip = "sca-agent.${VERSION}.zip"
                    sh label: "Create bundle", script: "sh dev/bundle.sh ${scaAgentZip}"
                    archiveArtifacts artifacts: scaAgentZip
                }
            }
        }
        stage('Test') {
            when {
                expression {
                    return false
                }
            }
            steps {
                script{
                    dir("setup") {
                        currentBuild.displayName = VERSION
                        sh label: "Install the agent", script: "unzip ${WORKSPACE}/${scaAgentZip} && sh ./setup.sh"
                        e2eSecrets = pipelineUtils.getSCAAgentParams()
                        withEnv([
                            "JENKINS_NODE_COOKIE=dontkillMe",
                            "AUTHENTICATIONTOKENSOURCE=" + e2eSecrets.resource,
                            "SCOPE=" + e2eSecrets.scope,
                            "GRANT_TYPE=" + e2eSecrets.grantType,
                            "ACCESSCONTROLCLIENTID=" + e2eSecrets.clientId,
                            "SCATENANT=" + e2eSecrets.tenant,
                            "SCAUSERNAME=" + e2eSecrets.username,
                            "SCAPASSWORDSECRET=" + e2eSecrets.password,
                            "E2E_IMAGE_URL=" + e2eSecrets.e2eImageUrl]) {
                            sh label: "Login to ECR", script: "\$(aws ecr get-login --no-include-email --region eu-central-1)"
                            sh label: "Run E2E", script: "cp -r ../dev . && sh dev/run-e2e.sh"
                        }
                    }
                }
            }
        }
        stage('Scenario Tests')
        {
            steps{
                script{

                    stash includes: "${scaAgentZip}", name: "bundle"

                    def testingScenarios = [:]

                    dir("tests"){

                        def files = findFiles(glob: '**/docker-compose*.yml')

                        files.each {
                           def (testName, composeFile) = it.path.split('/')
                           stash includes: "${WORKSPACE}/tests/${it.path}/*", name: "${testName}"

                           testingScenarios["test-${testName}"] = {
                                node("docker"){
                                        unstash 'bundle'
                                        sh "mkdir bundle && mkdir bundle/tests && unzip -d bundle ${scaAgentZip}"

                                        dir("bundle/tests"){
                                            unstash "${testName}"
                                        }

                                        dir("bundle"){
                                            sh label: "setup", script: "sh ./setup.sh"

                                            sh "docker-compose -f docker-compose.yml -f tests/${composeFile} up -d && docker-compose down"
                                        }
                                }
                            }
                        }
                    }

                   parallel testingScenarios
                }
            }
        }
        stage("Release") {
            when {
                expression {
                    return params.releaseNewVersion
                }
            }
            steps {
                script {
                    scaAgentZipRelease = "sca-agent.zip"
                    sh "cp ${WORKSPACE}/${scaAgentZip} ${WORKSPACE}/${scaAgentZipRelease}"
                    pipelineUtils.releaseNewVersion(VERSION, "${WORKSPACE}/${scaAgentZipRelease}")
                }
            }
        }
    }
    post {
        success {
            script {
                if (env.BRANCH_NAME == "master") {
                    attachments = ["${WORKSPACE}/${scaAgentZip}"]
                    pipelineUtils.sendBuildStatusMail(null, attachments)
                }
            }
        }
    }
}
