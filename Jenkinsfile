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

                    stash includes: "${scaAgentZip}", name: "agent-zip"

                    def testingScenarios = [:]

                    dir("tests"){

                        def files = findFiles(glob: '**/docker-compose*.yml')

                        files.each {

                           def (testName, composeFile) = it.path.split('/')
                           def testComposeFilePath = "tests/${testName}/${composeFile}"
                           stash includes: "**", name: "tests"

                           testingScenarios["test-${testName}"] = {
                                node("docker"){
                                    ws("${testName}-workspace"){

                                        unstash 'agent-zip'

                                        sh label: "Create Directories", script: "mkdir agent && mkdir agent/tests"
                                        sh label: "Unzip Bundle", script: "unzip -d agent ${scaAgentZip}"

                                        dir("agent/tests"){
                                            unstash "tests"
                                        }

                                        dir("agent"){

                                            def bundleOverridesDir = "tests/${testName}/bundle-overrides/"

                                            if (fileExists("${bundleOverridesDir}"))
                                            {
                                                sh label:"Copy Bundle Overrides", script: "cp -a ${bundleOverridesDir}. ./"
                                            }

                                            sh label: "Setup", script: "sh ./setup.sh"

                                            if (fileExists(".env.overrides"))
                                            {
                                                sh label: "Apply Environment Variables", script: "echo -e \"\\n\" >> .env; for line in \$(cat .env.overrides); do echo \"\$line\" >> .env; done"
                                            }

                                            sh label: "Run Agent", script: "docker-compose -f docker-compose.yml up -d"
                                            sh label: "Run Test", script: "docker-compose -f ${testComposeFilePath} up --build --abort-on-container-exit"

                                            sh label: "Shutdown Test", script: "docker-compose -f ${testComposeFilePath} down --remove-orphans"
                                            sh label: "Shutdown Agent", script: "docker-compose -f docker-compose.yml down"
                                        }
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
