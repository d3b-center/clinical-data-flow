
# ✔️ Clinical Data Flow Team Objectives and Key Results

## Objectives (1 Year - end of 2020)

1. Increase interoperability, data access, and flow among internal
   CHOP stakeholders and external stakeholders

    - a) Replace the Kids First Data Service with a FHIR data service since FHIR
      is the emerging standard for modeling, searching, exchanging, and
      distributing biomedical data.

    - b) Ingest Kids First studies into the Kids First FHIR server

    - c) Provide an app for stakeholders that makes it easy to
      browse and download data in their FHIR server

    - d) Provide an app for stakeholders that makes it easy to exchange
      data from one FHIR server to another FHIR server

    - e) Secure the clinical data service(s) with encryption, authentication, and
      authorization so that only users with necessary permissions to
      access a subset of data may access it

2. Increase participation from domain experts and model developers
   in clinical data model development

    - a) Provide tooling to make local FHIR model validation, testing easier
    - b) Document and publish the clinical data model in a technology agnostic way
      such that non-technical stakeholders may understand it
    - c) Automate FHIR model deployment - validate, test, publish documentation,
      load into server

3. Continually maximize the amount of clean, high quality clinical data available
   for researchers and other stakeholders

   - a) Clean, ingest, and harmonize X01 studies into the Kids First
        Data Service
   - b) Provide clear documentation and guidelines on the Kids First ingestion
        process for analysts and data engineers developing ingest packages

4. Decrease the time to deliver a study's high quality clean clinical data

    - a) Reduce manual and redundant analyst efforts to do data accounting by
      automating accounting tests and report generation
    - b) Reduce manual and redundant analyst efforts to do quality assessment
      on data as it moves through the clinical data pipeline    
    - c) Make quality assessment and control a more collaborative process among
      data curators and data analysts in the quality assessment

5. Improve the completeness and quality of clinical data for researchers

    - a) Reduce manual and redundant curator effort in ontology harmonization
      by automating harmonization with a smarter/machine learning based process
    - b) Make it easier for curators to collaborate on ontology harmonization by
      providing

6. Contribute to the open source FHIR community to increase collaboration on
   tool, service, and app development.

   - a) Open source the FHIR 101 tutorial  
   - b) Open source FHIR model development tool chain
   - c) Open source FHIR data dashboard


# Key Results

## Q2 2020 - ends June 30

The main goals of Q2 2020 are to: deploy an MVP Kids First FHIR server to
production and load 2 studies into the server using the entire CDF pipeline.

1. (O1a, O2a) Develop, validate, and test an MVP FHIR model for Kids First
2. (O2b) Publish documentation on the Kids First FHIR model as a public HL7 IG
3. (O2b) Publish model developer documentation on the Kids First FHIR model tool chain

4. (O1a, O1e) Deploy the Kids First FHIR server with the MVP model to production
5. (O1e) Integrate Auth0 into Kids First FHIR server to enable OIDC/OAuth 2.0 authn/z

6. (O1e) Implement client side OIDC + OAuth 2 authn/z flows in FHIR data dashboard
7. (O1c) Deploy the FHIR data dashboard app to production

8. (O1b) Ingest at least 2 studies (1 Kids First, 1 non-Kids First) into the
   Kids First FHIR server using the clinical data flow pipeline
   - PCGC
   - RIMGC 10-trio
9. (O3a) Ingest X01 studies into the Kids First Data Service
    - Chung 2018
    - Seidman 2018

### Sprint 3 - ends March 13

This sprint we will be working towards KR 1, KR 4, and KR 6

1. Secure the FHIR server with TLS and reduce # of exposed ports
    - Test with FHIR data dashboard and FHIR ingest
2. Create a 1-click script with a docker-compose stack to bootstrap the CDF pipeline
   for developers.
    - We need to make it easier for other developers to spin up our CDF pipeline so that
     they can collaborate with us, test our our pipeline for demo purposes or
     use it for their own development needs.
3. Write and publish a markdown document detailing feedback + questions on FHIR
   Phenopackets model, and lessons learned with FHIR modeling thus far.
4. Start development of the Kids First FHIR model:
    - Clean up kf-model-fhir branches
    - Publish a markdown doc with naming conventions for files and IDs  
    - Develop Participant with all attributes and search parameters
    - Develop Biospecimen with all attributes and search parameters
    - All extensions should be primitive types to start
5. Remove the FHIR Phenopackets model and load the Kids First model into FHIR server
6. Modify Phenopacket FHIR mappers for the Kids First FHIR model
7. Load PCGC into FHIR server using new Kids First mappers
8. Continue working on Ingest Library modifications for FHIR
9. Continue working on study ingestion (Chung 2018, Seidman 2018, RIMGC 10-trio)

### Sprint 4
TBD

### Sprint 5
TBD
