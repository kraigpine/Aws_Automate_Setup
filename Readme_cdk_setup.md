To set a cdk app, aws profile, and bootstrap & deploy to an account

1. Install Nodejs
    a. Download for your os and install
    b. To verify installation, run this in a terminal or command line: npm-v
2. Install Python 3.12 
3. Install Vs Code or IDE of your choice
4. Setup Vs Code to recognize Python:
    a. Install the following extensions:
        i. Python
        ii. Pylance
        iii. Python Debugger
    b. Set the interpreter
        i. Press Ctrl+Shift+P to bring up the interpreter
        ii. Select 'Python'
        iii. Select the 'Global' interpreter path
5. In Vs Code terminal (defaults to powershell so you are running commands in powershell):
    a. npm install -g aws-cdk
6. In terminal, create or navigate to a directory that will house your cdk app
    a. mkdir mycdkapp
    b. cd 
7. In terminal, create the cdk app with the basic files:
    a. cdk init app --language python
8. In terminal, initialize the .venv
    a. ./source.bat
9. Install requirements (must be done in every new .venv):
    a. Verify pip is installed by running this in terminal:
        i. pip --version
            A. If pip not installed, verify python installation in terminal:
                1. python --version
                2. If python cannot be found, edit the Environment Variable to make sure python is in the 'Path' variable
            B. Clear Vs Code cache by doing the following:
                1. Close Vs Code
                2. (Windows) Delete the following directories in c://Users/<username>/Library/Application Support/Code 
                    a. Cache
                    b. CachedData
                    c. CachedExtensions
                    iv. Code Cache
                    v. CachedExtensionVSIXs
    b. In terminal:
        i. ./source.bat
            This will activate a new .venv
        ii. pip install -r requirements.txt
10. AwsCli:
    a. To verify installation:
        i. aws --version
    b. To install:
        ii. pip install awscli
11. Log in to aws to create the IAM user:
    a. Create a new user with only programmatic access
    b. Create access policy 
        i. Select 'local code'
        ii. Download .csv
            Do NOT store in your repo
12. In aws, create 2 policies for the user:
    a. Create the policy for bootstrapping. (See bootstrap policy in example_access_policies)
        i. You can c&p from example_access_policies and replace the region and account number placeholders with your own
        ii. This policy is only for bootstrapping 'cdk bootstrap' It gets run 1x per account  and you will remove it after bootstrapping because it has more permissions that deploying needs
    b. Create the policy for deploying(See deploy policy in example_access_policies)
        i. You can c&p from example_access_policies and replace the region and account number placeholders with your own
        ii. This is the policy that will be used for running 'cdk deploy'
    c. Go back to IAM > user you just created and attach these 2 policies
13. Now we need to link your local machine to the aws account via the user you just made
    a. In terminal:
        i. aws configure --profile <name user you made in step 11>
            This is going to create a profile on your local machine linked to the aws account. Having different user names in different accounts is beneficial for recognizing which account you are bootstrapping or deploying to. 
            Example: cdk-user-dev, cdk-user-prod, cdk-user-qa, etc...
            a. Go through the prompts and input the values from the .csv. 
                i. Leave the 'Default output format' blank by hitting Enter
        ii. Go to c://Users/<username>/.aws and view the 2 files in a file editor. You should see the profile and credentials of your cdk user
14. Bootstrap to your aws account via the username
    a. In terminal, navigate to the directory you created in step 6. This should house the cdk app
    b. Run this in terminal: 
        i. cdk bootstrap --show-template bootstrap-template.yaml --profile <user from step 11>
            A. You should see a new file called 'bootstrap-template.yaml' in your directory
    c. Run this in terminal:
        i. cdk bootstrap --template bootstrap-template.yaml --profile <user from step 11>
    d. In your aws account, you should see a bucket for cdk resources and a stack in cloudformation called 'CDKToolkit'. Bootstrapping makes these by default.
    e. In IAM > <user from step 11>, remove the bootstrap policy
15. Deploy
    a. In terminal, make sure you are in the directory of the app and run:
        i. cdk deploy --profile <user from step 11> --all
            A. In cloudformation, you will see the stacks listed in app.py
        ii. You can alternatively deploy 1 stack at a time with:
            A. cdk deploy --profile <user from step 11> logical_id_of_stack_in_appdotpy
