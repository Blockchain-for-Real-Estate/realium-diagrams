# diagram.py
from diagrams import Diagram, Cluster
from diagrams.onprem.client import Users
from diagrams.aws.blockchain import BlockchainResource
from diagrams.aws.compute import EC2Instance, Lambda
from diagrams.aws.storage import SimpleStorageServiceS3Bucket
from diagrams.gcp.network import DNS
from diagrams.aws.network import Route53HostedZone, CF
from diagrams.programming.framework import React
from diagrams.programming.language import Javascript
from diagrams.aws.security import Cognito
from diagrams.aws.database import DB
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

            with Cluster("Vercel"):
                realium_cf = CF("CloudFront")
                realium_functions = Lambda("Lambda@Edge")
                realium_s3 = SimpleStorageServiceS3Bucket("S3")

                realium_cf >> realium_functions,
                realium_cf << realium_s3
            
            with Cluster("Google Analytics"):
                gtm = Dataflow("Google Tag Manager")
                gtm3 = Dataflow("Google My Business")

                gtm >> gtm3
            
            wallets = Javascript("Ethers JS")

            realium >> wallets
            realium >> realium_cf
            realium >> gtm


        with Cluster("AWS services"):
            auth_services = Cognito("Cognito")
            
            images = SimpleStorageServiceS3Bucket("Public Bucket")
            cf_images = CF("Image Distribution")

            user_table = DB("User's Table (3x)")
            private_images = SimpleStorageServiceS3Bucket("Private Bucket")
            
            ses = SimpleEmailServiceSes("Emails")
            sns = SimpleNotificationServiceSns("Text Notifications")

            images >> cf_images


        users >> domain
        dns >> realium
        realium_functions >> [ auth_services, images, ses, sns  ]
        realium_functions - [ user_table, private_images ]
        cf_images >> realium
    
    with Cluster("Backend"):

        with Cluster("EVM"):
            evm = EC2Instance("Smart Contracts")

        with Cluster("Avalanche Services"):
            avalanche = BlockchainResource("Blockchain")
        
        wallets >> evm
        evm >> avalanche
    

    realium_functions >> evm