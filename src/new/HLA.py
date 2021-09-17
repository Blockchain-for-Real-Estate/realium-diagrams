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


with Diagram("High Level Architecture - Level 0"):
    users = Users()

    with Cluster("DNS"):
        domain = DNS("Google Domains")
        dns = Route53HostedZone("Route53 Hosted Zone")

        domain >> dns

    # CLUSTERS
    with Cluster("realium.io"):
        home = Server("Wordpress")

        with Cluster("Wordpress by Bitnami"):
            home_wp = Lightsail("Wordpress")
            home_ssl = LetsEncrypt("Lets Encrypt SSL")
            home_db = Mysql()
        
        home >> home_wp
        home_wp << home_ssl
        home_wp << home_db

    with Cluster("coownership.realium.io"):
        co = React("Next.js")
        with Cluster("AWS Amplify"):
            co_cf = CF("CloudFront")
            co_functions = Lambda("Lambda@Edge")
            co_s3 = SimpleStorageServiceS3Bucket("S3")

            co_cf >> co_functions,
            co_cf << co_s3

        co >> co_cf

    with Cluster("ats.realium.io"):
        ats = React("Next.js")
        with Cluster("AWS Amplify"):
            ats_cf = CF("CloudFront")
            ats_functions = Lambda("Lambda@Edge")
            ats_s3 = SimpleStorageServiceS3Bucket("S3")

            ats_cf >> ats_functions,
            ats_cf << ats_s3

        ats >> ats_cf

    with Cluster("NextAuth Providers"):
        auth_services = Cognito("Cognito")

    with Cluster("AWS Storage"):
        user_table = Dynamodb("User's Table")
        relational = RDSPostgresqlInstance("DB (Maybe)")
    
    with Cluster("Avalanche Services"):
        avalanche = BlockchainResource("Blockchain")

    users >> domain
    dns >> [ home, ats, co ]
    co_functions >> [ auth_services, avalanche, user_table, relational ]
    ats_functions >> [ auth_services, avalanche, user_table, relational ]