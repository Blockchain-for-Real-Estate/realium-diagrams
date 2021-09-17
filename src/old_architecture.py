# diagram.py
from diagrams import Diagram, Cluster
from diagrams.aws.blockchain import BlockchainResource
from diagrams.aws.compute import EC2Instance
from diagrams.gcp.network import DNS
from diagrams.aws.network import Route53HostedZone
from diagrams.programming.framework import React, Django

with Diagram("Old Architecture"):
    # ENTITIES
    GoogleDomains = DNS("Google Domains")
    DNS = Route53HostedZone("DNS Hosted Zone")

    # CLUSTERS
    with Cluster("Web Services"):
        Realium = React("realium.io")
        WebServer = EC2Instance("EC2")
        Realium - WebServer

    with Cluster("Api Services"):
        RealiumApi = Django()
        ApiServer = EC2Instance("EC2")
        RealiumApi - ApiServer

    with Cluster("Avalanche Services"):
        Avalanche = BlockchainResource("Blockchain")

    # CONNECTIONS
    GoogleDomains - DNS - Realium
    WebServer - RealiumApi
    ApiServer - Avalanche
