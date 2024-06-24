from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    aws_s3 as s3,
    Stack,
    Duration,
    BundlingOptions,
    RemovalPolicy
)
from constructs import Construct
from aws_cdk.aws_lambda_python_alpha import PythonLayerVersion
import boto3

class NetflixBackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        movie_table = dynamodb.Table(
            self, "movies-dbtable2",
            table_name="movies-dbtable2",
            partition_key=dynamodb.Attribute(
                name="movie_id",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="title",
                type=dynamodb.AttributeType.STRING
            ),
            read_capacity=1,
            write_capacity=1
        )
        
        s3_bucket = s3.Bucket(self,id="movie-bucket3",bucket_name="movie-bucket3")

        lambda_role = iam.Role(
            self, "LambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )

        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        )
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
        )
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess")
        )

        lambda_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "dynamodb:DescribeTable",
                    "dynamodb:Query",
                    "dynamodb:Scan",
                    "dynamodb:GetItem",
                    "dynamodb:PutItem",
                    "dynamodb:UpdateItem",
                    "dynamodb:DeleteItem",
                    "s3:PutObject",
                    "s3:PutObjectAcl",
                    "s3:GetObject",
                    "s3:GetObjectAcl",
                    "s3:DeleteObject"
                ],
                resources=[movie_table.table_arn,f"{s3_bucket.bucket_arn}/*"]
                # resources=[movie_table.table_arn,"arn:aws:s3:::<movie-bucket>/*"]
            )
        )
        

        def create_lambda_function(id, handler, include_dir, method):
            function = _lambda.Function(
                self, id,
                runtime=_lambda.Runtime.PYTHON_3_11,
                handler=handler,
                code=_lambda.Code.from_asset(include_dir),
                memory_size=128,
                timeout=Duration.seconds(10),
                environment={
                    'TABLE_NAME': movie_table.table_name,
                    'BUCKET_NAME': s3_bucket.bucket_name
                },
                role=lambda_role
            )
            fn_url = function.add_function_url(
                auth_type=_lambda.FunctionUrlAuthType.NONE,
                cors=_lambda.FunctionUrlCorsOptions(
                    allowed_origins=["*"]
                )
            )
            
            return function


        api = apigateway.RestApi(self, "netflix-api", 
                                rest_api_name="netflix-api",
                                endpoint_types=[apigateway.EndpointType.REGIONAL],
                                default_cors_preflight_options=apigateway.CorsOptions(
                                    allow_origins=apigateway.Cors.ALL_ORIGINS,
                                    allow_methods=apigateway.Cors.ALL_METHODS,
                                    allow_headers=apigateway.Cors.DEFAULT_HEADERS
                                ))
        
        create_movie_lambda = create_lambda_function(
            "createMovie",
            "create_movie.post_movie",
            "movie_service",
            "POST",
        )

        download_movie_lambda = create_lambda_function(
            "downloadMovie",
            "download_movie.download_movie",
            "movie_service",
            "GET",
        )
        
        update_movie_lambda = create_lambda_function(
            "updateMovie",
            "update_movie.update_movie",
            "movie_service",
            "PUT",
        )
        
        movies_resource = api.root.add_resource("movies")
        create_movie_integration = apigateway.LambdaIntegration(create_movie_lambda)
        movies_resource.add_method("POST", create_movie_integration)

        download_integration = apigateway.LambdaIntegration(download_movie_lambda)
        movies_resource.add_method("GET", download_integration)
        
        update_integration = apigateway.LambdaIntegration(update_movie_lambda)
        movies_resource.add_method("PUT", update_integration)
