sam deploy --no-confirm-changeset --no-fail-on-empty-changeset --stack-name sam-hello --s3-bucket sam-bucket-code --capabilities CAPABILITY_IAM --region eu-west-3

docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

sam local start-api

sam local invoke "HelloWorldFunction" -e events/event.json

aws cloudformation delete-stack --stack-name sam-labs0