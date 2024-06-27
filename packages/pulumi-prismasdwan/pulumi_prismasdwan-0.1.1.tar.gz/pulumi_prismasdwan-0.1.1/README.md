# Prisma SD-WAN Resource Provider

A Pulumi package for managing Prisma SD-WAN resources. 

This provider was created leveraging the existing
[Strata Cloud Manager](https://www.pulumi.com/registry/packages/scm/) provider, as the Prisma SD-WAN functionality is 
a superset of the SCM functionality. 

Future releases of SCM providers may incorporate the alternate, single JSON configuration capabilities available in this provider.

## Installing

This package is available for several languages/platforms:

### Node.js (JavaScript/TypeScript)

To use from JavaScript or TypeScript in Node.js, install using either `npm`:

```bash
npm install @pulumi/prismasdwan
```

or `yarn`:

```bash
yarn add @pulumi/prismasdwan
```

### Python

To use from Python, install using `pip`:

```bash
pip install pulumi_prismasdwan
```

### Go

To use from Go, use `go get` to grab the latest version of the library:

```bash
go get github.com/paloaltonetworks/pulumi-prismasdwan/sdk/go/...
```

### .NET

To use from .NET, install using `dotnet add package`:

```bash
dotnet add package Pulumi.Prismasdwan
```

## Configuration

The following configuration points are **required** for the `prismasdwan` provider:

- `prismasdwan:clientId` (environment: `SCM_CLIENT_ID`) - The client ID for the connection.
- `prismasdwan:clientSecret` (environment: `SCM_CLIENT_SECRET`) - The client secret for the connection.
- `prismasdwan:scope` (environment: `SCM_CLIENT_ID`) - "The client scope (Tenant Service Group ID, or tsg_id in format `tsg_id:<value>`).

## Reference

For detailed reference documentation, please visit [the Pulumi registry](https://www.pulumi.com/registry/packages/).
