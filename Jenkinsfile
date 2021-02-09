library "pipelineUtils"

def scaAgentZip

pipeline {
    parameters {
        booleanParam(name: 'releaseNewVersion', defaultValue: false, description: 'If "true", New release will occur in GitHub')
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
            VERSION = pipelineUtils.getSemanticVersion(0, 2)
    }
    stages{
        stage("Bundle") {
            when {
                expression {
                    return false
                }
            }
            steps {
                script{
                    scaAgentZip = "sca-agent.${VERSION}.zip"
                    sh(label: "Create bundle", script: "sh dev/bundle.sh ${scaAgentZip}")
                    archiveArtifacts artifacts: scaAgentZip
                }
            }
        }
        stage('Run E2E') {
            when {
                expression {
                    return false
                }
            }
            steps {
                script{
                    currentBuild.displayName = VERSION
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
                        sh(label: "Setup", script: "sh setup.sh")
                        sh("\$(aws ecr get-login --no-include-email --region eu-central-1)")
                        sh(label: "Run e2e", script: "sh dev/run-e2e.sh")
                    }
                }
            }
        }
        stage('Run Scenario Tests')
        {
            steps{
                script{

                    def testingScenarios = [:]

                    dir("tests"){

                        def files = findFiles(glob: '**/docker-compose*.yml')

                        testingScenarios["test-sometest"] = {
                            node("docker"){
                                sh("echo testComplete")
                            }
                        }

                        files.each {
                           testName = it.path.split('/')[0]
                           testingScenarios["test-${testName}"] = {
                                node("docker"){
                                    //sh("docker-compose -f ${WORKSPACE}/sca-agent/docker-compose.yml -f ${WORKSPACE}/sca-agent/tests/${it.path} up --abort-on-container-exit")
                                    sh("echo ${WORKSPACE}")
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