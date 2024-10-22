#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_stori.cdk_stori_stack import CdkStoriStack


app = cdk.App()
CdkStoriStack(
    app,
    "CdkStoriStack",
    env = cdk.Environment(account='123456789012', region='us-east-1'),
    )

app.synth()
