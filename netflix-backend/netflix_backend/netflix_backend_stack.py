
from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    aws_s3 as s3,
    aws_cognito as cognito,
    Stack,
    Duration,
    BundlingOptions,
    aws_stepfunctions_tasks as sfn_tasks,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    RemovalPolicy, custom_resources,
    aws_sns as sns
)
from aws_cdk.aws_apigateway import AuthorizationType, IAuthorizer, Authorizer
from aws_cdk.aws_cognito import CfnUserPoolUser, CfnUserPoolUserToGroupAttachment
from aws_cdk.aws_lambda import Architecture
from constructs import Construct
from aws_cdk import aws_sqs as sqs, aws_lambda_event_sources as event_sources
from debugpy._vendored._util import cwd


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
        
        movie_table.add_global_secondary_index(
            index_name="SearchIndex",
            partition_key=dynamodb.Attribute(
                name="search_data",
                type=dynamodb.AttributeType.STRING
            ),
            projection_type=dynamodb.ProjectionType.ALL
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

        feed_update_queue = sqs.Queue(
            self, "FeedUpdateQueue",
            queue_name="FeedUpdateQueue",
            visibility_timeout=Duration.seconds(300)
        )

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
                    "s3:DeleteObject",
                    "sqs:SendMessage"
                ],
                resources=[movie_table.table_arn,f"{s3_bucket.bucket_arn}/*",feed_update_queue.queue_arn]
            )
        )

        user_pool = cognito.UserPool(
            self, "UserPool",
            user_pool_name="UserPool",
            self_sign_up_enabled=True,
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_digits=True,
                require_lowercase=True,
                require_uppercase=True,
                require_symbols=True

            ),
            sign_in_aliases=cognito.SignInAliases(username=True),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(
                    required=True,
                    mutable=False
                ),
                family_name=cognito.StandardAttribute(
                    required=True,
                    mutable=True
                ),
                phone_number=cognito.StandardAttribute(
                    required=True,
                    mutable=True
                ),
                given_name=cognito.StandardAttribute(
                    required=True,
                    mutable=True
                )
            ),


        )


        web_client = cognito.UserPoolClient(self, "WebAppClient",
                                    user_pool=user_pool,
                                    generate_secret=False,  # Typically false for web apps
                                    user_pool_client_name="WebAppClient",
                                    )

        admins_group = cognito.CfnUserPoolGroup(self, "AdminsGroup",
                                                group_name="Admins",
                                                user_pool_id=user_pool.user_pool_id
                                                )

        users_group = cognito.CfnUserPoolGroup(self, "UsersGroup",
                                                        group_name="Users",
                                                        user_pool_id=user_pool.user_pool_id
                                                        )


        user = CfnUserPoolUser(self, 'admir',
                               user_pool_id=user_pool.user_pool_id,
                               username='admir',
                               desired_delivery_mediums=["EMAIL"],
                               user_attributes=[cognito.CfnUserPoolUser.AttributeTypeProperty(
                                   name="email",
                                   value="a@gmail.com"
                               ),cognito.CfnUserPoolUser.AttributeTypeProperty(
                                   name="family_name",
                                   value="admirovic"
                               ),cognito.CfnUserPoolUser.AttributeTypeProperty(
                                   name="phone_number",
                                   value='+38160'
                               ),cognito.CfnUserPoolUser.AttributeTypeProperty(
                                   name="given_name",
                                   value="admir"
                               )])




        cfn_user_pool_user_to_group_attachment = cognito.CfnUserPoolUserToGroupAttachment(self,
                                                                                          "MyCfnUserPoolUserToGroupAttachment",
                                                                                          group_name="Admins",
                                                                                          username="admir",
                                                                                          user_pool_id=user_pool.user_pool_id
                                                                                          )

        set_password = custom_resources.AwsCustomResource(self, "SetTestUserPassword",
                                            on_create=custom_resources.AwsSdkCall(
                                                service="CognitoIdentityServiceProvider",
                                                action="adminSetUserPassword",
                                                parameters={
                                                    "UserPoolId": user_pool.user_pool_id,
                                                    "Username": "admir",
                                                    "Password": "Nemanja123*",
                                                    "Permanent": True,
                                                },
                                                physical_resource_id=custom_resources.PhysicalResourceId.of("SetTestUserPassword-admir")
                                            ),on_update=custom_resources.AwsSdkCall(
                                                service="CognitoIdentityServiceProvider",
                                                action="adminSetUserPassword",
                                                parameters={
                                                    "UserPoolId": user_pool.user_pool_id,
                                                    "Username": "admir",
                                                    "Password": "Nemanja123*",
                                                    "Permanent": True,
                                                },
                                                physical_resource_id=custom_resources.PhysicalResourceId.of("SetTestUserPassword-admir")
                                            ),

                                              policy=custom_resources.AwsCustomResourcePolicy.from_sdk_calls(
                                                  resources=custom_resources.AwsCustomResourcePolicy.ANY_RESOURCE
                                              )
                                            )

        set_password.node.add_dependency(cfn_user_pool_user_to_group_attachment)
        web_client.node.add_dependency(user_pool)
        admins_group.node.add_dependency(user_pool)
        users_group.node.add_dependency(user_pool)

        user.node.add_dependency(admins_group)
        cfn_user_pool_user_to_group_attachment.node.add_dependency(user)




        ffmpeg_layer = _lambda.LayerVersion(self, 'layer-ffmpeg',
                                     code= _lambda.Code.from_asset('./layer-ffmeg'),
                                     compatible_runtimes= [_lambda.Runtime.PYTHON_3_11],
                                     layer_version_name= 'ffmpeg-layer',
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
                                    allow_origins=["http://localhost:4200"],
                                    allow_methods=["PUT","POST","DELETE","GET","HEAD"],
                                    allow_headers=["*"]
                                ))

        create_movie_lambda = create_lambda_function(
            "createMovie",
            "create_movie.post_movie",
            "movie_service",
            "POST",
            {
                'TABLE_NAME': movie_table.table_name,
                'BUCKET_NAME': s3_bucket.bucket_name,
                'FEED_UPDATE_QUEUE_URL': feed_update_queue.queue_url,
                'USER_POOL_ID': user_pool.user_pool_id
            },
        )
        
        create_movie_lambda.add_to_role_policy(iam.PolicyStatement(
            actions=["sns:CreateTopic", "sns:Publish", "sns:Subscribe"],
            resources=["*"],
        ))
        
        prevent_duplicate_email_lambda = create_lambda_function(
            "preventDuplicateEmail",
            "prevent_duplicate_email.handler",
            "user_service",
            "POST",
            {}
        )

        add_to_user_group = create_lambda_function(
                    "addToUserGroup",
                    "add_to_user_group.handler",
                    "user_service",
                    "POST",
                    {}
                )


        hello = create_lambda_function(
            "hello",
            "test.handler",
            "user_service",
            "POST",
            {}
        )


        layer = _lambda.LayerVersion(self, 'layer',
            code= _lambda.Code.from_asset('./layer-jwt'),
            compatible_runtimes= [_lambda.Runtime.PYTHON_3_9],
            layer_version_name= 'jwt-layer',
        )

        authenticate_group=_lambda.Function(
            self, "authenticateGroup",
            runtime=_lambda.Runtime.PYTHON_3_9,
            architecture=Architecture.X86_64,
            handler="authenticate_group.handler",
            code=_lambda.Code.from_asset("user_service"),
            memory_size=128,
            timeout=Duration.seconds(10),
            environment={'USERPOOL_ID':user_pool.user_pool_id,
                         'WEB_CLIENT_ID':web_client.user_pool_client_id},
            role=lambda_role,
            layers=[layer]
        )


        authorizer=apigateway.RequestAuthorizer(self,id="bla",
                                                 authorizer_name="blabla",
                                                 identity_sources=['method.request.header.authorizationtoken'],
                                                 handler=authenticate_group,
                                                results_cache_ttl=Duration.seconds(0)
                                                )

        test_resource=api.root.add_resource("testiranje")
        test_resource.add_method("GET", apigateway.LambdaIntegration(hello),authorization_type=AuthorizationType.CUSTOM,authorizer=authorizer)

        pre_sign_up_lambda = prevent_duplicate_email_lambda
        post_sign_lambda=add_to_user_group

        user_pool.add_trigger(cognito.UserPoolOperation.PRE_SIGN_UP, pre_sign_up_lambda)
        user_pool.add_trigger(cognito.UserPoolOperation.POST_CONFIRMATION,post_sign_lambda)

        pre_sign_up_policy_statement = iam.PolicyStatement(
            actions=["cognito-idp:ListUsers"],
            resources=[user_pool.user_pool_arn]
        )

        pre_sign_up_lambda.role.attach_inline_policy(
            iam.Policy(self, 'PreSignUpLambdaPolicy',
                       statements=[pre_sign_up_policy_statement]
                       )
        )

        post_confirmation_policy_statement = iam.PolicyStatement(
            actions=[
                "cognito-idp:AdminAddUserToGroup",
                "cognito-idp:AdminGetUser",
                "cognito-idp:ListUsers"
            ],
            resources=[user_pool.user_pool_arn]
        )

        post_sign_lambda.role.attach_inline_policy(
            iam.Policy(self, 'PostConfirmationLambdaPolicy',
                       statements=[post_confirmation_policy_statement]
                       )
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
                'BUCKET_NAME': s3_bucket.bucket_name,
                'FEED_UPDATE_QUEUE_URL': feed_update_queue.queue_url
            },
        )

        delete_movie_lambda = create_lambda_function(
            "deleteMovie",
            "delete_movie.delete_movie",
            "movie_service",
            "DELETE",
            {
                'MOVIE_TABLE_NAME': movie_table.table_name,
                'REVIEW_TABLE_NAME': review_table.table_name,
                'DOWNLOAD_HISTORY_TABLE_NAME': download_history_table.table_name,
                'BUCKET_NAME': s3_bucket.bucket_name,
                'FEED_UPDATE_QUEUE_URL': feed_update_queue.queue_url
            },
        )
        
        get_series_lambda = create_lambda_function(
            "getMovieSeries",
            "get_series.get_series",
            "movie_service",
            "GET",
            {
                'TABLE_NAME': movie_table.table_name,
                'BUCKET_NAME': s3_bucket.bucket_name
            },
        )
        
        search_movies_lambda = create_lambda_function(
            "searchMoviesLambda",
            "search_movies.search_movies",
            "movie_service",
            "GET",
            {
                'TABLE_NAME': movie_table.table_name,
                'BUCKET_NAME': s3_bucket.bucket_name
            },
        )

        download_specific_resolution_lambda = create_lambda_function(
            "downloadSpecificResolution",
            "download_specific_resolution.download_specific_resolution",
            "movie_service",
            "GET",
            {
                'TABLE_NAME': movie_table.table_name,
                'BUCKET_NAME': s3_bucket.bucket_name,
            },
        )
        

        movies_resource = api.root.add_resource("movies")
        movies_resource.add_method("POST", apigateway.LambdaIntegration(create_movie_lambda),authorization_type=AuthorizationType.CUSTOM,authorizer=authorizer)
        movies_resource.add_method("GET", apigateway.LambdaIntegration(download_movie_lambda),authorization_type=AuthorizationType.CUSTOM,authorizer=authorizer)
        movies_resource.add_method("PUT", apigateway.LambdaIntegration(update_movie_lambda),authorization_type=AuthorizationType.CUSTOM,authorizer=authorizer)
        movies_resource.add_method("DELETE", apigateway.LambdaIntegration(delete_movie_lambda),authorization_type=AuthorizationType.CUSTOM,authorizer=authorizer)
        
        movies_resource = api.root.add_resource("series")
        movies_resource.add_method("GET", apigateway.LambdaIntegration(get_series_lambda),authorization_type=AuthorizationType.CUSTOM,authorizer=authorizer)
        
        search_resource = api.root.add_resource("search")
        search_resource.add_method("GET", apigateway.LambdaIntegration(search_movies_lambda),authorization_type=AuthorizationType.CUSTOM,authorizer=authorizer)

        download_resoluton_resource = api.root.add_resource("download")
        download_resoluton_resource.add_method("GET", apigateway.LambdaIntegration(download_specific_resolution_lambda))

        subscribe_lambda = create_lambda_function(
            "subscribe",
            "subscribe.subscribe",
            "subscription_service",
            "POST",
            {
                'TABLE_NAME': subscription_table.table_name,
                'FEED_UPDATE_QUEUE_URL': feed_update_queue.queue_url,
                'USER_POOL_ID': user_pool.user_pool_id
                
            }
        )

        subscribe_lambda.add_to_role_policy(iam.PolicyStatement(
            actions=["sns:CreateTopic", "sns:Publish", "sns:Subscribe", "sns:Unsubscribe"],
            resources=["*"],
        ))
        
        unsubscribe_lambda = create_lambda_function(
            "unsubscribe",
            "unsubscribe.unsubscribe",
            "subscription_service",
            "DELETE",
            {
                'TABLE_NAME': subscription_table.table_name,
                'FEED_UPDATE_QUEUE_URL': feed_update_queue.queue_url,
                'USER_POOL_ID': user_pool.user_pool_id
                
            }
        )
        
        unsubscribe_lambda.add_to_role_policy(iam.PolicyStatement(
            actions=["sns:CreateTopic",
                     "sns:DeleteTopic",
                     "sns:Publish",
                     "sns:Subscribe",
                     "sns:Unsubscribe",
                     "sns:ListSubscriptionsByTopic"],
            resources=["*"],
        ))

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
        subscriptions_resource.add_method("POST", apigateway.LambdaIntegration(subscribe_lambda),authorization_type=AuthorizationType.CUSTOM,authorizer=authorizer)
        subscriptions_resource.add_method("DELETE", apigateway.LambdaIntegration(unsubscribe_lambda),authorization_type=AuthorizationType.CUSTOM,authorizer=authorizer)
        subscriptions_resource.add_method("GET", apigateway.LambdaIntegration(get_subscriptions_lambda),authorization_type=AuthorizationType.CUSTOM,authorizer=authorizer)



        review_lambda = create_lambda_function(
            "review",
            "review.review",
            "review_service",
            "POST",
            {
                'TABLE_NAME': review_table.table_name,
                'FEED_UPDATE_QUEUE_URL': feed_update_queue.queue_url
            }
        )

        get_review_lambda = create_lambda_function(
            "getReview",
            "get_reviews.get_reviews",
            "review_service",
            "GET",
            {
                'TABLE_NAME': review_table.table_name
            }
        )

        review_resource = api.root.add_resource("reviews")
        review_resource.add_method("POST", apigateway.LambdaIntegration(review_lambda),authorization_type=AuthorizationType.CUSTOM,authorizer=authorizer)
        review_resource.add_method("GET", apigateway.LambdaIntegration(get_review_lambda),authorization_type=AuthorizationType.CUSTOM,authorizer=authorizer)

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

        feed_update_lambda = create_lambda_function(
            "FeedUpdateLambda",
            "update_users_feed.lambda_handler",
            "feed_service",
            "POST",
            {
                'USER_POOL_ID': user_pool.user_pool_id,
                'FEED_TABLE_NAME': feed_table.table_name,
                'MOVIES_TABLE_NAME': movie_table.table_name,
                'REVIEWS_TABLE_NAME': review_table.table_name,
                'SUBSCRIPTIONS_TABLE_NAME': subscription_table.table_name,
                'DOWNLOAD_HISTORY_TABLE_NAME': download_history_table.table_name
            }
        )

        feed_update_lambda.add_event_source(
            event_sources.SqsEventSource(feed_update_queue)
        )

        feed_resource = api.root.add_resource("feed")
        feed_resource.add_method("GET", apigateway.LambdaIntegration(get_feed_lambda),authorization_type=AuthorizationType.CUSTOM,authorizer=authorizer)

        create_download_history_lambda = create_lambda_function(
            "createDownloadHistory",
            "create_download_history.create_download_history",
            "download_history_service",
            "POST",
            {
                'DOWNLOAD_HISTORY_TABLE_NAME': download_history_table.table_name,
                'FEED_UPDATE_QUEUE_URL': feed_update_queue.queue_url
            }
        )

        history_resource = api.root.add_resource("history")
        history_resource.add_method("POST", apigateway.LambdaIntegration(create_download_history_lambda),authorization_type=AuthorizationType.CUSTOM,authorizer=authorizer)

        transcoding_data_lambda = _lambda.Function(
            self, "TranscodingData",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="transcoding_data.handler",
            code=_lambda.Code.from_asset("transcoding"),
            memory_size=128,
            timeout=Duration.seconds(10),
            environment={}
        )

        transcode_movie_lambda = _lambda.Function(
            self, "TranscodeLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="transcode.handler",
            code=_lambda.Code.from_asset("transcoding"),
            layers=[ffmpeg_layer],
            timeout=Duration.minutes(1),
            memory_size=512,
            environment={
                'BUCKET_NAME': s3_bucket.bucket_name,
            }
        )

        split_task = tasks.LambdaInvoke(
            self, "SplitTask",
            lambda_function=transcoding_data_lambda,
            output_path="$.Payload"
        )

        parallel_transcode = sfn.Parallel(self, 'parallelTranscoding')
        for resolution in ['360', '480', '720']:
            parallel_transcode.branch(sfn_tasks.LambdaInvoke(
                self, f'transcoding-{resolution}',
                lambda_function=transcode_movie_lambda,
                payload=sfn.TaskInput.from_object({
                    "movie_id": sfn.JsonPath.string_at("$.movie_id"),
                    "resolution": resolution
                }),
            ).add_retry(
                max_attempts=3,
                interval=Duration.seconds(60)
            ))

        definition = split_task.next(parallel_transcode)

        state_machine = sfn.StateMachine(
            self, "StateMachine",
            definition_body=sfn.DefinitionBody.from_chainable(definition),
            timeout=Duration.minutes(15)
        )

        start_transcoding_lambda = _lambda.Function(
            self, "StartTranscoding",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="start_transcoding.handler",
            code=_lambda.Code.from_asset("transcoding"),
            memory_size=128,
            timeout=Duration.seconds(10),
            environment={
                "STATE_MACHINE_ARN": state_machine.state_machine_arn
            }
        )

        state_machine.grant_start_execution(start_transcoding_lambda)
        s3_bucket.grant_read_write(transcode_movie_lambda)

        transcode_resource = api.root.add_resource("transcode")
        transcode_resource.add_method("PUT", apigateway.LambdaIntegration(start_transcoding_lambda))

