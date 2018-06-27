# AWS Lambda Invocations Counter
Retrieves the invocation count of your AWS Lambda Functions from CloudWatch for a given number of minutes.

It makes use of the popular "Boto3" library and expects your local environment to be [setup with AWS credentials and region](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html).

## Usage:

	~$ python count-invocations.py -h

	usage: count-invocations.py [-h] [-f FILTER] [-m MINUTES] [-t TOP] [-v] [-z]

	optional arguments:
	  -h, --help            show this help message and exit
	  -f FILTER, --filter FILTER
	                        string to match in Lambda functions to report on (eg:
	                        "prod-")
	  -m MINUTES, --minutes MINUTES
	                        minutes of window period to measure (1440 for 24
	                        hours)
	  -t TOP, --top TOP     number of top results to return
	  -v, --verbose         display some progress info
	  -z, --zeros           return results with 0 invocations

## Example:

	~$ python count-invocations.py -f prod -m 2 -t 10 -v -z
	
	Skipping "dev-list-books" (does not match filter string)
	Counting invocations for "prod-list-books"
	Skipping "dev-create-book" (does not match filter string)
	Counting invocations for "prod-create-book"
	Skipping "dev-update-book" (does not match filter string)
	Counting invocations for "prod-update-book"
	Skipping "dev-delete-book" (does not match filter string)
	Counting invocations for "prod-delete-book"
	Lambda functions counted: 4
	Reducing result set to 10 highest results


	prod-list-books   31
	prod-create-book  4
	prod-update-book  0
	prod-delete-book  0
