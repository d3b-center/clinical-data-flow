
<p align="center">
  <img alt="Logo for The Center for Data Driven Discovery" src="https://raw.githubusercontent.com/d3b-center/handbook/master/website/static/img/chop_logo.svg?sanitize=true" width="400px" />
</p>
<p align="center">
  <a href="https://github.com/d3b-center/clinical-data-flow/blob/master/LICENSE"><img src="https://img.shields.io/github/license/d3b-center/clinical-data-flow.svg?style=for-the-badge"></a>
</p>

# Clinical Data Flow
Project management and design artifacts for [Clinical Data Flow](https://d3b.io/docs/products/clinical-data-flow) product

## Evolving Architecture
[Draw.io Source](https://drive.google.com/file/d/1xdtljwZ2FjFVxJD4tPRbP1QWk2j1eE3d/view?usp=sharing)

![Architecture](docs/static/img/clinical-data-flow-draft-arch.png)

### Components

- [Data Ingest Library](https://github.com/kids-first/kf-lib-data-ingest)
- RedCap to FHIR (FHIR Cap) - TBD
- [Ingest Warehouse](warehouse/README.md)
- FHIR Staging Service - TBD
- [FHIR Data Service](https://github.com/kids-first/kf-api-fhir-service)
- [FHIR Data Model](https://github.com/kids-first/kf-model-fhir)
- [FHIR Data Dashboard](https://github.com/kids-first/kf-ui-fhir-data-dashboard)

