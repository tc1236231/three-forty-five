ThreeFourtyFive

This sample code helps get you started with a simple Flask web service
deployed by AWS Elastic Beanstalk and AWS CloudFormation.

What's Here
-----------

This sample includes:

* README.md - this file
* buildspec.yml - this file is used by AWS CodeBuild to package your
  application for deployment to AWS Lambda
* requirements.txt - this file is used install Python dependencies needed by
  the Flask application
* setup.py - this file is used by Python's setuptools library to describe how
  your application will be packaged and installed
* mnhsdata/ - this directory contains the Python source code for your Flask application
* tests/ - this directory contains unit tests for your application
* .ebextensions/ - this directory contains the configuration files that allow
  AWS Elastic Beanstalk to deploy your application
* template.yml - this file contains the description of AWS resources used by AWS
  CloudFormation to deploy your infrastructure
* template-configuration.json - this file contains the project ARN with placeholders used for tagging resources with the project ID

Getting Started
---------------

Clone and enter the repo. Then:

1. Create a Python virtual environment:

        $ python3 -m venv venv

2. Activate the virtual environment:

        $ . venv/bin/activate

3. Install Python dependencies for this project:

        $ pip install -r requirements.txt

4. Install the application code into your virtual environment:

        $ pip install -e .  # sudo pip install -e . for Cloud9 

5. Start the Flask development server (note: Cloud9 requires port 8080):

        $ python tff/application.py --debug --port 8080

6. Open http://127.0.0.1:8080/ in a web browser to view the output of your
   service.

What Do I Do Next?
------------------

Once you have a virtual environment running, you can start making changes. To
run your tests locally, go to the root directory of the sample code and run the
`python setup.py pytest` command, which AWS CodeBuild also runs through your
`buildspec.yml` file.

To test your new code during the release process, modify the existing tests or
add tests to the tests directory. AWS CodeBuild will run the tests during the
build stage of the project pipeline. You can find the test results in the AWS
CodeBuild console.

Learn more about AWS CodeBuild and how it builds and tests your application here:
https://docs.aws.amazon.com/codebuild/latest/userguide/concepts.html

Learn more about AWS CodeStar by reading the user guide. Ask questions or make
suggestions on our forum.

User Guide: http://docs.aws.amazon.com/codestar/latest/userguide/welcome.html
Forum: https://forums.aws.amazon.com/forum.jspa?forumID=248

Best Practices: https://docs.aws.amazon.com/codestar/latest/userguide/best-practices.html?icmpid=docs_acs_rm_sec

How Do I Add Template Resources to My Project?
------------------

To add AWS resources to your project, you'll need to edit the `template.yml`
file in your project's repository. You may also need to modify permissions for
your project's worker roles. After you push the template change, AWS CodeStar
and AWS CloudFormation provision the resources for you.

See the AWS CodeStar user guide for instructions to modify your template:
https://docs.aws.amazon.com/codestar/latest/userguide/how-to-change-project#customize-project-template.html
=======
