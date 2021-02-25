# Scenario Testing

This section will give an understanding on scenario testing in the SCA Agent

---
####Fast Facts
    Each Test is :
    - A dockerized application
    - An isolated and has its own instance of a running SCA Agent
    - Runs in parallel
    - Runs in its own Jenkins node
___

## Tests Structure
All the tests are located in the `tests` folder and each have its own sub-directory with the **unique** test name.
Next we call such a directory a `{test directory}`
---
### Basic Structure
Each `test folder` has its own `docker-compose.yml` , which contain an information about how to run the test

```
|--tests/
   |--{test directory}/
      |--bundle-overrides/    # Optional directory
      |--docker-compose.yml   # Mandatory
      |--...
```

___
### Override Defaults
If you need to override default agent's files or configs, simple put them in `bundle-overrides/` directory.
Keep in mind, that `bundle-override` directory is agent's root directory, so that if you need to change environment 
variables, and some configuration for volumes you should process like this:
```
|--tests/
   |--{test directory}/
      |--bundle-overrides/
         |--volumes/
            |--traefik/
               |--http/
                  |--...
         |--.env
         |--docker-compose.yml
         |--...
      |--...
```

Files and directories inside the `bundle-overrides` will simply replace original SCA Agent's files during the runtime

#### Override Environment Variables
Environment Variables can be overwritten by adding `.env.overrides` files in the root of `bundle-overrides`. 
That will simply overwrite the values specified in `.env` by adding them to the bottom of the file. This will simply make
the runtime work with new values.
___

### Test Scenario docker-compose.yml

```yml
services:
  %scenario-name%-test:
    image: %scenario-name%-check-agent
    build: ../src/%path-to-tests%
    network_mode: host
    environment:
      RUN_TEST_MODULES: health_tests, identity_tests, presignedurl_tests
```
The test's `docker-compose.yml` must share the host network to do the requests to the running agent.
To specify which tests to run simply add Environment Variable with the comma-separated test modules like specified above
---

## Tests Runtime

```
(Bundle) ===================> (Scenario Tests)
    |                                  | -- test one
    |                                  | -- test two
    |                                  | -- test ...
    .zip artifact
```

1. During the `Bundle` step the `.zip artifact` is stored in Jenkins workspace. 
1. The `Scenario Tests` step firstly stashes that artifact for each test's `node` and unstash inside the `node` 
1. Then the script will start to search tests focusing on `docker-compose.yml`
1. Each finding will produce a separate node and its own `Workspace`
1. Each `.zip artifact` file is unstashed and unpacked to its own `Workspace`
1. If `bundle-overrides` directory exists inside the test -> the contents will replace an original agent's files
1. `Setup` is executed
    - **!!! IMPORTANT !!! make sure your custom `.env.defaults.` does not violate any secrets**
1. If there is the file `.env.overrides` -> add specific environment variables to the Agent
1. Agent startup
1. Test startup 
1. Test shutdown
1. Agent shutdown
___

### Running Testing Scenarios Locally

To run the tests locally you have to run it from the `root` directory of your `sca-agent`

```sh
sh ./tests/run_test_scenario.sh %scenario_name%
```

`%scnario_name%` is a name of your testing scenario in `tests` directory