# Avi's graph-based validation test

`python3 test_validator.py`

EXPECTED RESULT:

```txt
DATASET1
    Test Failed:
        ('BIOSPECIMEN|ID', 'S2') -> [('PARTICIPANT|ID', 'P2'), ('PARTICIPANT|ID', 'P1')]
        ('BIOSPECIMEN|ID', 'S8') -> []
    Test Failed:
        ('PARTICIPANT|ID', 'P11') -> []
        ('PARTICIPANT|ID', 'P13') -> []
    Test Failed:
        ('PARTICIPANT|ID', 'P11') -> []
    Test Failed:
        ('FAMILY|ID', 'F12') -> []
    Test Passed
DATASET2
    Test Passed
    Test Passed
    Test Passed
    Test Passed
    Test Passed
```
