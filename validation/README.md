# Clinical Data Validation

Prototyping for validating relational data based on a set of rules.

## Notebooks

- MVP-Validation-Non-Graph.ipynb (uses DataFrames and does not consider implied connections)
- MVP-Validation-Graph.ipynb (uses a graph and considers implied connections)

Both notebooks output the same validation report

# Sample Validation Report

### \* View data in a connected [graph](graph.svg)

## Count Tests
| result   | name                                   | details   |
|:---------|:---------------------------------------|:----------|
| ✅       | Expected Participant Unique Count = 10 |           |
| ✅       | Expected Specimen Unique Count = 12    |           |

## Relation Tests
| result   | name                                                          | details                                                                             | error_locations                       |
|:---------|:--------------------------------------------------------------|:------------------------------------------------------------------------------------|:--------------------------------------|
| ❌       | A Participant is in at least 1 Family Group                   | Participant P11 is linked to 0 Family entities                                      | Found P11 in files: pf.csv            |
| ❌       | A Family Group must have at least 1 Participant               | Family F12 is linked to 0 Participant entities                                      | Found F12 in files: pf.csv            |
| ❌       | A Specimen comes from 1 Participant                           | Biospecimen S2 is linked to 2 Participant entities: {'P1', 'P2'}                    | Found S2 in files: spf.csv,sfp2.csv   |
|          |                                                               | Biospecimen S8 is linked to 0 Participant entities                                  | Found S8 in files: spf.csv            |
| ❌       | A Participant must have at least 1 Specimen                   | Participant P11 is linked to 0 Biospecimen entities                                 | Found P11 in files: pf.csv            |
|          |                                                               | Participant P13 is linked to 0 Biospecimen entities                                 | Found P13 in files: pf.csv            |
| ❌       | A Sequence Manifest File Record represents only 1 Specimen    | Genomic_File ['foo/s5.txt'] is linked to 3 Biospecimen entities: {'S7', 'S5', 'S6'} | Found ['foo/s5.txt'] in files: pg.csv |
| ❌       | A Specimen must have at least 1 Sequence Manifest File Record | Biospecimen S2 is linked to 0 Genomic_File entities                                 | Found S2 in files: spf.csv,sfp2.csv   |
|          |                                                               | Biospecimen S1 is linked to 0 Genomic_File entities                                 | Found S1 in files: spf.csv            |
|          |                                                               | Biospecimen S3 is linked to 0 Genomic_File entities                                 | Found S3 in files: spf.csv            |
|          |                                                               | Biospecimen S4 is linked to 0 Genomic_File entities                                 | Found S4 in files: spf.csv            |
|          |                                                               | Biospecimen S8 is linked to 0 Genomic_File entities                                 | Found S8 in files: spf.csv            |

## Attribute Tests
| result   | name                                     | details                                      | error_locations   |
|:---------|:-----------------------------------------|:---------------------------------------------|:------------------|
| ❌       | A Participant must have exactly 1 gender | 0 Participant have linked PARTICIPANT|GENDER |                   |

## Test Definitions
| test_type         | name                                                          | description                                                                                                                            |
|:------------------|:--------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------|
| count-test        | Expected Participant Unique Count = 10                        | The number of uniquely identifiable participants found in study must be equal to the expected count                                    |
| count-test        | Expected Specimen Unique Count = 12                           | The number of uniquely identifiable specimens found in study must be equal to the expected count                                       |
| attribute-test    | A Participant must have exactly 1 gender                      | Every uniquely identifiable Participant must have exactly 1 gender from the acceptable list: Male, Female                              |
| relationship-test | A Participant is in at least 1 Family Group                   | Every uniquely identifiable Participant must be linked to at  least 1 uniquely identifiable Family within the study                    |
| relationship-test | A Family Group must have at least 1 Participant               | Every uniquely identifiable Family Group must have at least 1 uniquely identifiable Participant within the study                       |
| relationship-test | A Specimen comes from 1 Participant                           | Every uniquely identifiable Specimen must be linked to  exactly 1 uniquely identifiable Participant within the study                   |
| relationship-test | A Participant must have at least 1 Specimen                   | Every uniquely identifiable Participant must have at least 1  uniquely identifiable Specimen within the study                          |
| relationship-test | A Sequence Manifest File Record represents only 1 Specimen    | Every uniquely identifiable Sequence Manifest File Record must be linked to exactly 1 uniquely identifiable Specimen within the study  |
| relationship-test | A Specimen must have at least 1 Sequence Manifest File Record | Every uniquely identifiable specimen must be linked to at least 1 uniquely identifiable Sequence Manifest File Record within the study |
