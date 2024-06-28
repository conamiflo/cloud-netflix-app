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

        subscription_table = dynamodb.Table(
            self, "subscription-table",
            table_name="subscription-table",
            partition_key=dynamodb.Attribute(
                name="subscription_id",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="username",
                type=dynamodb.AttributeType.STRING
            ),
            read_capacity=1,
            write_capacity=1
        )

        review_table = dynamodb.Table(
            self, "review-table2",
            table_name="review-table2",
            partition_key=dynamodb.Attribute(
                name="review_id",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="username",
                type=dynamodb.AttributeType.STRING
            ),
            read_capacity=1,
            write_capacity=1
        )

        download_history_table = dynamodb.Table(
            self, "download-history-table",
            table_name="download-history-table",
            partition_key=dynamodb.Attribute(
                name="download_id",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="username",
                type=dynamodb.AttributeType.STRING
            ),
            read_capacity=1,
            write_capacity=1
        )

        feed_table = dynamodb.Table(
            self, "feed-table",
            table_name="feed-table",
            partition_key=dynamodb.Attribute(
                name="username",
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


        def create_lambda_function(id, handler, include_dir, method, environment):
            function = _lambda.Function(
                self, id,
                runtime=_lambda.Runtime.PYTHON_3_11,
                handler=handler,
                code=_lambda.Code.from_asset(include_dir),
                memory_size=128,
                timeout=Duration.seconds(10),
                environment=environment,
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
            {
                'TABLE_NAME': movie_table.table_name,
                'BUCKET_NAME': s3_bucket.bucket_name
            },
        )

        download_movie_lambda = create_lambda_function(
            "downloadMovie",
            "download_movie.download_movie",
            "movie_service",
            "GET",
            {
                'TABLE_NAME': movie_table.table_name,
                'BUCKET_NAME': s3_bucket.bucket_name
            },
        )

        update_movie_lambda = create_lambda_function(
            "updateMovie",
            "update_movie.update_movie",
            "movie_service",
            "PUT",
            {
                'TABLE_NAME': movie_table.table_name,
                'BUCKET_NAME': s3_bucket.bucket_name
            },
        )

        movies_resource = api.root.add_resource("movies")
        movies_resource.add_method("POST", apigateway.LambdaIntegration(create_movie_lambda))
        movies_resource.add_method("GET", apigateway.LambdaIntegration(download_movie_lambda))
        movies_resource.add_method("PUT", apigateway.LambdaIntegration(update_movie_lambda))

        subscribe_lambda = create_lambda_function(
            "subscribe",
            "subscribe.subscribe",
            "subscription_service",
            "POST",
            {
                'TABLE_NAME': subscription_table.table_name
            }
        )

        unsubscribe_lambda = create_lambda_function(
            "unsubscribe",
            "unsubscribe.unsubscribe",
            "subscription_service",
            "DELETE",
            {
                'TABLE_NAME': subscription_table.table_name
            }
        )

        get_subscriptions_lambda = create_lambda_function(
            "getSubscriptions",
            "get_subscriptions.get_subscriptions",
            "subscription_service",
            "GET",
            {
                'TABLE_NAME': subscription_table.table_name
            }
        )

        subscriptions_resource = api.root.add_resource("subscriptions")
        subscriptions_resource.add_method("POST", apigateway.LambdaIntegration(subscribe_lambda))
        subscriptions_resource.add_method("DELETE", apigateway.LambdaIntegration(unsubscribe_lambda))
        subscriptions_resource.add_method("GET", apigateway.LambdaIntegration(get_subscriptions_lambda))

        review_lambda = create_lambda_function(
            "review",
            "review.review",
            "review_service",
            "POST",
            {
                'TABLE_NAME': review_table.table_name
            }
        )

        review_resource = api.root.add_resource("reviews")
        review_resource.add_method("POST", apigateway.LambdaIntegration(review_lambda))

        get_feed_lambda = create_lambda_function(
            "getFeed",
            "get_feed.get_feed",
            "feed_service",
            "GET",
            {
                'MOVIES_TABLE_NAME': movie_table.table_name,
                'FEED_TABLE_NAME': feed_table.table_name
            }
        )

        update_users_feed_lambda = create_lambda_function(
            "updateUsersFeed",
            "update_users_feed.update_users_feed",
            "feed_service",
            "PUT",
            {
                'MOVIES_TABLE_NAME': movie_table.table_name,
                'FEED_TABLE_NAME': feed_table.table_name,
                'REVIEWS_TABLE_NAME': review_table.table_name,
                'SUBSCRIPTIONS_TABLE_NAME': subscription_table.table_name,
                'DOWNLOAD_HISTORY_TABLE_NAME': download_history_table.table_name
            }
        )

        feed_resource = api.root.add_resource("feed")
        feed_resource.add_method("GET", apigateway.LambdaIntegration(get_feed_lambda))
        feed_resource.add_method("PUT", apigateway.LambdaIntegration(update_users_feed_lambda))