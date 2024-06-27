# CDK Node.js EC2 Instance Construct

This is a CDK Construct for creating an EC2 instance with Node.js installed.

You can use Node.js as soon as the EC2 instance starts.

[![View on Construct Hub](https://constructs.dev/badge?package=cdk-node-ec2-instance)](https://constructs.dev/packages/cdk-node-ec2-instance)

[![Open in Visual Studio Code](https://img.shields.io/static/v1?logo=visualstudiocode&label=&message=Open%20in%20Visual%20Studio%20Code&labelColor=2c2c32&color=007acc&logoColor=007acc)](https://open.vscode.dev/badmintoncryer/cdk-node-ec2-instance)
[![npm version](https://badge.fury.io/js/cdk-node-ec2-instance.svg)](https://badge.fury.io/js/cdk-node-ec2-instance)
[![Build Status](https://github.com/badmintoncryer/cdk-node-ec2-instance/actions/workflows/build.yml/badge.svg)](https://github.com/badmintoncryer/cdk-node-ec2-instance/actions/workflows/build.yml)
[![Release Status](https://github.com/badmintoncryer/cdk-node-ec2-instance/actions/workflows/release.yml/badge.svg)](https://github.com/badmintoncryer/cdk-node-ec2-instance/actions/workflows/release.yml)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![npm downloads](https://img.shields.io/npm/dm/cdk-node-ec2-instance.svg?style=flat)](https://www.npmjs.com/package/cdk-node-ec2-instance)

## Usage

Install the package:

```bash
npm install cdk-node-ec2-instance
```

Use it in your CDK stack:

```python
import { NodeEc2Instance } from 'cdk-node-ec2-instance';
import * as ec2 from 'aws-cdk-lib/aws-ec2';

declare const vpc: ec2.IVpc;

// You can configure all properties of the EC2 instance
new NodeEc2Instance(this, 'Instance', {
  vpc,
  instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.NANO),
  machineImage: new ec2.AmazonLinuxImage({
    generation: ec2.AmazonLinuxGeneration.AMAZON_LINUX_2023,
  }),
  nodeJsVersion: 'v20.13.1', // Optional property. Default is installing the latest LTS version
});
```

After the stack is deployed, you can SSH into the EC2 instance and use Node.js:

```bash
$ ssh ec2-user@<public-ip>
$ node --version
v20.13.1
```

## user data

Installation of Node.js is done by user data script. You can see the script in the `src/index.ts` file.

```python
nodejsUserData.addCommands(
  'touch ~/.bashrc',
  'curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash',
  'source ~/.bashrc',
  'export NVM_DIR="$HOME/.nvm"',
  '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"',
  `nvm install ${props.nodeJsVersion ?? '--lts'}`,
  // Note that the above will install nvm, node and npm for the root user.
  // It will not add the correct ENV VAR in ec2-user's environment.
  `cat <<EOF >> /home/ec2-user/.bashrc
export NVM_DIR="/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
EOF`);
```

Ofcourse, you can customize the additional user data script by calling `instance.userData.addCommands()` method.

```python
declare const instance: NodeEc2Instance;

// install VScode for linux
instance.userData.addCommands(
  'sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc',
  'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" | sudo tee /etc/yum.repos.d/vscode.repo > /dev/null',
  'sudo dnf check-update',
  'sudo dnf install -y code',
);
```
