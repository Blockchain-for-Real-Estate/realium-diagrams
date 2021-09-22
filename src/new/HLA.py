# diagram.py
from diagrams import Diagram, Cluster
from diagrams.onprem.client import Users, User 
from diagrams.aws.blockchain import BlockchainResource
from diagrams.aws.compute import EC2Instance, Lambda, Lightsail
from diagrams.aws.storage import SimpleStorageServiceS3Bucket
from diagrams.gcp.network import DNS
from diagrams.aws.network import Route53HostedZone, CF
from diagrams.programming.framework import React, Django
from diagrams.aws.mobile import Amplify
from diagrams.saas.identity import Auth0
from diagrams.saas.social import Facebook, Twitter
from diagrams.onprem.certificates import LetsEncrypt
from diagrams.onprem.database import Mysql
from diagrams.aws.security import Cognito
from diagrams.onprem.compute import Server
from diagrams.aws.database import Dynamodb, RDSPostgresqlInstance
from diagrams.aws.mobile import APIGateway
from diagrams.aws.engagement import SimpleEmailServiceSes
from diagrams.aws.integration import SimpleNotificationServiceSns
from diagrams.gcp.analytics import Dataflow
from diagrams.generic.storage import Storage
from diagrams.aws.integration import SimpleNotificationServiceSns

with Diagram("High Level Architecture - Level 0"):
    users = Users()

    with Cluster("Front End"):
        with Cluster("DNS"):
            domain = DNS("Google Domains")
            dns = Route53HostedZone("Route53 Hosted Zone")

            domain >> dns

        with Cluster("realium.io"):
            realium = React("Next.js")

            with Cluster("AWS Amplify"):
                realium_cf = CF("CloudFront")
                realium_functions = Lambda("Lambda@Edge")
                realium_s3 = SimpleStorageServiceS3Bucket("S3")

                realium_cf >> realium_functions,
                realium_cf << realium_s3
            
            with Cluster("Google Analytics"):
                gtm = Dataflow("Google Tag Manager")
                gtm3 = Dataflow("Google My Business")

                gtm >> gtm3
            
            with Cluster("Web3"):
                metamask = Storage("Metamask")

            realium >> metamask
            realium >> realium_cf
            realium >> gtm


        with Cluster("NextAuth Providers"):
            auth_services = Cognito("Cognito")


        with Cluster("AWS services"):
            images = SimpleStorageServiceS3Bucket("Public Bucket")
            cf_images = CF("Image Distribution")

            user_table = Dynamodb("User's Table")
            private_images = SimpleStorageServiceS3Bucket("Private Bucket")
            
            ses = SimpleEmailServiceSes("Emails")
            sns = SimpleNotificationServiceSns("Text Notifications")

            images >> cf_images



        users >> domain
        dns >> realium
        realium_functions >> [ auth_services, images, private_images, ses, sns ]
        realium_functions - [ user_table ]
        cf_images >> realium
    
    with Cluster("Backend"):

        with Cluster("EVM"):
            evm = EC2Instance("Smart Contracts")

        with Cluster("Avalanche Services"):
            avalanche = BlockchainResource("Blockchain")
        
        evm >> avalanche
    

    realium_functions >> evm