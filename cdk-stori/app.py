#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_stori.cdk_stori_stack import CdkStoriStack

account = os.getenv('AWS_ACCOUNT')
region = os.getenv('AWS_REGION')
app = cdk.App()
CdkStoriStack(
    app,
    "CdkStoriStack",
    env = cdk.Environment(account=account, region=region),
    )

app.synth()
