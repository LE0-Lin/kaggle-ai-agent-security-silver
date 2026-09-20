# Security policy

## Scope

This repository is a defensive research artifact for a deterministic offline benchmark. It must not be used to probe, manipulate, or send data through systems without explicit authorization.

## Reporting a problem

Please open a GitHub security advisory for vulnerabilities in the repository itself. Do not publish secrets, private competition assets, real targets, or exploit traces in a public issue.

For issues in the original competition infrastructure, use the reporting channel designated by Kaggle or the competition organizers.

## Safe defaults

- all example recipients use the reserved `example.invalid` domain;
- local tests use an in-memory fake environment;
- no network calls or live tools are part of the test suite;
- credentials, datasets, submissions, and model artifacts are ignored by Git.
