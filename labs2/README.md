# labs1

sam deploy --no-confirm-changeset --no-fail-on-empty-changeset --stack-name sam-labs2 --s3-bucket sam-bucket-code --capabilities CAPABILITY_IAM --region eu-west-3

aws cloudformation delete-stack --stack-name sam-labs2