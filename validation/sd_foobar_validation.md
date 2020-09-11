# 📓 Data Validation Report for `SD_FOOBAR`

## 📁 Files Evaluated

| Files       |
|:------------|
| dbgap_pedigree.csv      |
| subject_files.csv      |
| sample_manifest.csv    |
| sample_gf_manifest.csv      |
| sample_attributes.csv      |
| dbgap_subjects.csv     |


## #️⃣ Unique Entity Counts

| Type        | Count |
|:------------|:------|
| Family      |  1000 |
| Participant |  2208 |
| Biospecimen |  2209 |
| Sequence Manifest File |  2209 |
| Source Seq S3 File |  2210 |
| Sequencing Experiment |  2210 |


## 🚦 Relation Tests
| result   | name                                                          | details                                                          | error_locations                            |
|:---------|:--------------------------------------------------------------|:-----------------------------------------------------------------|:-------------------------------------------|
| ❌       | A Participant is in at least 1 Family Group                   | Participant P11 is linked to 0 Family entities                   | Found P11 in files: {'dbgap_pedigree.csv'}             |
| ❌       | A Family Group must have at least 1 Participant               | Family F12 is linked to 0 Participant entities                   | Found F12 in files: {'dbgap_pedigree.csv'}             |
| ❌       | A Specimen comes from 1 Participant                           | Biospecimen S2 is linked to 2 Participant entities: {'P2', 'P1'} | Found S2 in files: {'dbgap_pedigree.csv', 'sfp2.csv'} |
|          |                                                               | Biospecimen S8 is linked to 0 Participant entities               | Found S8 in files: {'dbgap_pedigree.csv'}             |
| ❌       | A Participant must have at least 1 Specimen                   | Participant P11 is linked to 0 Biospecimen entities              | Found P11 in files: {'dbgap_pedigree.csv'}             |
|          |                                                               | Participant P13 is linked to 0 Biospecimen entities              | Found P13 in files: {'dbgap_pedigree.csv'}             |
| ❌       | A Sequence Manifest File Record represents only 1 Specimen    | Sequence_Manifest_File ['foo/s11.txt'] is linked to 0 Biospecimen entities | Found ['foo/s11.txt'] in files: {'subject_files.csv'} |
|          |                                                               | Sequence_Manifest_File ['foo/s5.txt'] is linked to 0 Biospecimen entities  | Found ['foo/s5.txt'] in files: {'subject_files.csv'}  |
|          |                                                               | Sequence_Manifest_File ['foo/s9.txt'] is linked to 0 Biospecimen entities  | Found ['foo/s9.txt'] in files: {'subject_files.csv'}  |
| ❌       | A Specimen must have at least 1 Sequence Manifest File Record | Biospecimen NA is linked to 0 Sequence_Manifest_File entities              | Found NA in files: {'sfp2.csv'}            |
|          |                                                               | Biospecimen S1 is linked to 0 Sequence_Manifest_File entities              | Found S1 in files: {'dbgap_pedigree.csv'}             |
|          |                                                               | Biospecimen S11 is linked to 0 Sequence_Manifest_File entities             | Found S11 in files: {'sample_attributes.csv'}             |
|          |                                                               | Biospecimen S2 is linked to 0 Sequence_Manifest_File entities              | Found S2 in files: {'dbgap_pedigree.csv', 'sfp2.csv'} |
|          |                                                               | Biospecimen S3 is linked to 0 Sequence_Manifest_File entities              | Found S3 in files: {'dbgap_pedigree.csv'}             |
|          |                                                               | Biospecimen S4 is linked to 0 Sequence_Manifest_File entities              | Found S4 in files: {'dbgap_pedigree.csv'}             |
|          |                                                               | Biospecimen S5 is linked to 0 Sequence_Manifest_File entities              | Found S5 in files: {'dbgap_pedigree.csv'}             |
|          |                                                               | Biospecimen S6 is linked to 0 Sequence_Manifest_File entities              | Found S6 in files: {'dbgap_pedigree.csv'}             |
|          |                                                               | Biospecimen S8 is linked to 0 Sequence_Manifest_File entities              | Found S8 in files: {'dbgap_pedigree.csv'}             |
|          |                                                               | Biospecimen S9 is linked to 0 Sequence_Manifest_File entities              | Found S9 in files: {'dbgap_pedigree.csv'}             |

## 🚦Attribute Tests
| result   | name                                     | details                                                                               | error_locations   |
|:---------|:-----------------------------------------|:--------------------------------------------------------------------------------------|:------------------|
| ☑️        | A Participant must have exactly 1 gender | Test did not run, required columns not found ('PARTICIPANT.ID', 'PARTICIPANT.GENDER') |                   |
| ❌       | A Biospecimen must have exactly 1 analyte type | Biospecimen S1 is missing analyte_type                                                | Found S1 in files: {'sample_attributes.csv', 'sample_manifest.csv'} |
| ❌       | A Biospecimen must have exactly 1 analyte type | Biospecimen S2 has invalid analyte_type: "dna"                                         | Found S2 in files: {'sample_attributes.csv', 'sample_manifest.csv'} |



## 📝 Test Definitions
| test_type         | name                                                          | description                                                                                                                            |
|:------------------|:--------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------|
| attribute-test    | A Participant must have exactly 1 gender                      | Every uniquely identifiable Participant must have exactly 1 gender from the acceptable list: `Male`, `Female`                              |
| attribute-test    | A Biospecimen must have exactly 1 analyte_type                      | Every uniquely identifiable Biospecimen must have exactly 1 analyte_type from the acceptable list: `DNA`, `RNA`, `Virtual`, `Not Reported`, `Cannot Collect`, `Not Applicable`, `Unknown`                              |
| count-test        | Expected Participant Unique Count = 10                        | The number of uniquely identifiable participants found in study must be equal to 10                                                    |
| count-test        | Expected Specimen Unique Count = 12                           | The number of uniquely identifiable specimens found in study must be equal to 12                                                       |
| relationship-test | A Participant is in at least 1 Family Group                   | Every uniquely identifiable Participant must be linked to at  least 1 uniquely identifiable Family within the study                    |
| relationship-test | A Family Group must have at least 1 Participant               | Every uniquely identifiable Family Group must have at least 1 uniquely identifiable Participant within the study                       |
| relationship-test | A Specimen comes from 1 Participant                           | Every uniquely identifiable Specimen must be linked to  exactly 1 uniquely identifiable Participant within the study                   |
| relationship-test | A Participant must have at least 1 Specimen                   | Every uniquely identifiable Participant must have at least 1  uniquely identifiable Specimen within the study                          |
| relationship-test | A Sequence Manifest File Record represents only 1 Specimen    | Every uniquely identifiable Sequence Manifest File Record must be linked to exactly 1 uniquely identifiable Specimen within the study  |
| relationship-test | A Specimen must have at least 1 Sequence Manifest File Record | Every uniquely identifiable specimen must be linked to at least 1 uniquely identifiable Sequence Manifest File Record within the study |
