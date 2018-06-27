import boto3
import argparse
import datetime
import time
from texttable import Texttable

def get_lambda_functions(client):
	response = client.list_functions()
	return map(lambda x: x.get('FunctionName', False), response['Functions'])

def get_lambda_invocation_count(cloudwatch, function, minutes):
	current_time = datetime.datetime.utcnow()

	options = {
		"Namespace": "AWS/Lambda",
		"StartTime": (current_time - datetime.timedelta(minutes=minutes)).isoformat(), 
		"EndTime": current_time.isoformat(), 
		"Period": minutes * 60,
		"MetricName": "Invocations",
		"Statistics": ["Sum"], 
		"Unit": "Count",
		"Dimensions": [{
			"Name": "FunctionName",
			"Value": function
		}]
	}

	response = cloudwatch.get_metric_statistics(**options)
	if len(response['Datapoints']) > 0:
		invocations = int(round(response['Datapoints'][0]['Sum'], 0))
	else:
		invocations = 0

	return invocations

def get_lambda_functions_and_counts(minutes, filter_str, verbose):
	aws_lambda = boto3.client('lambda')

	cloudwatch = boto3.client('cloudwatch')

	invocations = []

	functions = get_lambda_functions(aws_lambda)
	for function in functions:

		if filter_str in function:
			if verbose:
				print 'Counting invocations for "'+ function + '"'
			num = get_lambda_invocation_count(cloudwatch, function, minutes)
			invocations.append({'name': function, 'invocations': num})

		else:
			if verbose:
				print 'Skipping "' + function + '" (does not match filter string)'

	return invocations

def run(minutes, filter_str, top, verbose, return_zero):
	invocations = get_lambda_functions_and_counts(minutes, filter_str, verbose)
	invocations = sorted(invocations, key=lambda k: k['invocations'], reverse=True)

	if verbose:
		print 'Lambda functions counted: ' + str(len(invocations))

	if top > 0:
		if verbose:
			print 'Reducing result set to ' + str(top) + ' highest results'
		invocations = invocations[0:top]

	if not return_zero:
		if verbose:
			print 'Removing results with 0 invocations'
		invocations = [i for i in invocations if i['invocations'] != 0]

	if verbose:
		print '\n' # clear lines

	t = Texttable()
	t.set_deco(Texttable.HEADER)
	for i in invocations:
		t.add_row([i['name'], i['invocations']])
		#print i['name'] + ' = ' + str(i['invocations']) + ' invocations'
	print t.draw()

ap = argparse.ArgumentParser()
ap.add_argument('-f', '--filter', help='string to match in Lambda functions to report on (eg: "prod-")')
ap.add_argument('-m', '--minutes', type=int, help='minutes of window period to measure (1440 for 24 hours)')
ap.add_argument('-t', '--top', type=int, help='number of top results to return')
ap.add_argument('-v', '--verbose', action='store_const', const=True, help='display some progress info')
ap.add_argument('-z', '--zeros', action='store_const', const=True, help='return results with 0 invocations')
args = vars(ap.parse_args())

# default settings:
minutes = 60
filter_str = ''
top = 0
verbose = False
return_zero = False

# set settings from arguments
if args.get('filter'):
	filter_str = args.get('filter')
if args.get('minutes'):
	minutes = int(args.get('minutes'))
if args.get('top'):
	top = int(args.get('top'))
if args.get('verbose'):
	verbose = True
if args.get('zeros'):
	return_zero = True

run(minutes, filter_str, top, verbose, return_zero)