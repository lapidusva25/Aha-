# Aha-wishlist-as-collection-and-timeline

## Quick start: 
* Edit the lambda_function.py file and input your own token/api keys
* Setup the Customer Data Hub job within Totango to fetch the file

## Business use cases:
* Give your CSMs a view of all enhancement requests that each customer has submitted via Aha.
* Create a play / campaign when a wishlist item status has updated to Planned or Started.

## Requirements: 
* Aha token
* You have an AWS bucket with an AWS_key / AWS_secret
* You have the ability to read and write to this bucket
* Totango token
* Totango Admin rights

## Minimizing API calls: 
The code checks to see if the file was previously generated, if it was it grabs the max value of the updated_at date from the previously generated file and uses that in the subsequent query.

## High level functional overview: 
This code is meant to run on a recurring basis.
This code grabs all wishlist items within Aha, looks up the user within Totango to see which accounts that user belongs to.  Then adds a collection/timeline line item for each user / account combination to the CSV.
You can then setup a jub in the Customer Data Hub to retrieve the file.

## Support:
Please reach out to support@totango.com with any issues