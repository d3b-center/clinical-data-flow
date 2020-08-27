# Avi's graph-based validation test

`python3 test_validator.py`

CURRENT RESULTS:

```txt
==========================================================================================
======================================== DATASET1 ========================================
==========================================================================================

DATASET1/sfp2.csv
  BIOSPECIMEN|ID PARTICIPANT|ID FAMILY|ID
0             S7             P5        F2
1                            P6        F3
2             S2             P2        F1

DATASET1/pg.csv
  GENOMIC_FILE|URL_LIST PARTICIPANT|ID
0        ['foo/s5.txt']             P4
1        ['foo/s9.txt']             P9
2       ['foo/s11.txt']            P10

DATASET1/pf.csv
  PARTICIPANT|ID FAMILY|ID
0            P10       F10
1            P11
2                      F12
3            P13       F13

DATASET1/spf.csv
  BIOSPECIMEN|ID PARTICIPANT|ID FAMILY|ID
0             S1             P1        F1
1             S2             P1        F1
2             S3             P3        F1
3             S4             P3
4             S5             P4        F2
5             S6             P5        F2
6             S7                       F2
7             S8
8             S9             P9        F9

DATASET1/sg.csv
  GENOMIC_FILE|URL_LIST BIOSPECIMEN|ID
0        ['foo/s7.txt']             S7
1       ['foo/s10.txt']            S10

DATASET1/sp.csv
  BIOSPECIMEN|ID PARTICIPANT|ID
0             S7             P5
1            S10             P6
2            S11            P10

Test: Each FAMILY|ID links to at least 1 PARTICIPANT|ID                         Result: ❌

Error Reasons:
	('FAMILY|ID', 'F12') -> []

Locations:
	('FAMILY|ID', 'F12') found in ['DATASET1/pf.csv']

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test: Each PARTICIPANT|ID links to at least 1 FAMILY|ID                         Result: ❌

Error Reasons:
	('PARTICIPANT|ID', 'P11') -> []

Locations:
	('PARTICIPANT|ID', 'P11') found in ['DATASET1/pf.csv']

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test: Each PARTICIPANT|ID links to at least 1 BIOSPECIMEN|ID                    Result: ❌

Error Reasons:
	('PARTICIPANT|ID', 'P11') -> []
	('PARTICIPANT|ID', 'P13') -> []

Locations:
	('PARTICIPANT|ID', 'P11') found in ['DATASET1/pf.csv']
	('PARTICIPANT|ID', 'P13') found in ['DATASET1/pf.csv']

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test: Each BIOSPECIMEN|ID links to exactly 1 PARTICIPANT|ID                     Result: ❌

Error Reasons:
	('BIOSPECIMEN|ID', 'S2') -> [('PARTICIPANT|ID', 'P1'), ('PARTICIPANT|ID', 'P2')]
	('BIOSPECIMEN|ID', 'S8') -> []

Locations:
	('BIOSPECIMEN|ID', 'S2') found in ['DATASET1/sfp2.csv', 'DATASET1/spf.csv']
	('BIOSPECIMEN|ID', 'S8') found in ['DATASET1/spf.csv']
	('PARTICIPANT|ID', 'P1') found in ['DATASET1/spf.csv']
	('PARTICIPANT|ID', 'P2') found in ['DATASET1/sfp2.csv']

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test: Each BIOSPECIMEN|ID links to at least 1 GENOMIC_FILE|URL_LIST             Result: ❌

Error Reasons:
	('BIOSPECIMEN|ID', 'S1') -> []
	('BIOSPECIMEN|ID', 'S2') -> []
	('BIOSPECIMEN|ID', 'S3') -> []
	('BIOSPECIMEN|ID', 'S4') -> []
	('BIOSPECIMEN|ID', 'S6') -> []
	('BIOSPECIMEN|ID', 'S8') -> []

Locations:
	('BIOSPECIMEN|ID', 'S1') found in ['DATASET1/spf.csv']
	('BIOSPECIMEN|ID', 'S2') found in ['DATASET1/sfp2.csv', 'DATASET1/spf.csv']
	('BIOSPECIMEN|ID', 'S3') found in ['DATASET1/spf.csv']
	('BIOSPECIMEN|ID', 'S4') found in ['DATASET1/spf.csv']
	('BIOSPECIMEN|ID', 'S6') found in ['DATASET1/spf.csv']
	('BIOSPECIMEN|ID', 'S8') found in ['DATASET1/spf.csv']

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test: Each GENOMIC_FILE|URL_LIST links to exactly 1 BIOSPECIMEN|ID              Result: ✅

==========================================================================================
======================================== DATASET2 ========================================
==========================================================================================

DATASET2/npg.csv
  GENOMIC_FILE|URL_LIST PARTICIPANT|ID
0        ['foo/s5.txt']             P5
1        ['foo/s9.txt']             P9
2       ['foo/s11.txt']            P11

DATASET2/nps.csv
  BIOSPECIMEN|ID PARTICIPANT|ID
0             S5             P5
1             S9             P9
2            S11            P11

DATASET2/nfg.csv
  GENOMIC_FILE|URL_LIST FAMILY|ID
0        ['foo/s5.txt']        F5
1        ['foo/s9.txt']        F9
2       ['foo/s11.txt']       F11

Test: Each FAMILY|ID links to at least 1 PARTICIPANT|ID                         Result: ✅

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test: Each PARTICIPANT|ID links to at least 1 FAMILY|ID                         Result: ✅

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test: Each PARTICIPANT|ID links to at least 1 BIOSPECIMEN|ID                    Result: ✅

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test: Each BIOSPECIMEN|ID links to exactly 1 PARTICIPANT|ID                     Result: ✅

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test: Each BIOSPECIMEN|ID links to at least 1 GENOMIC_FILE|URL_LIST             Result: ✅

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test: Each GENOMIC_FILE|URL_LIST links to exactly 1 BIOSPECIMEN|ID              Result: ✅

==========================================================================================
======================================== DATASET3 ========================================
==========================================================================================

DATASET3/pb.csv
  BIOSPECIMEN|ID PARTICIPANT|ID
0             B1             P1

DATASET3/fp.csv
  PARTICIPANT|ID FAMILY|ID
0             P1        F1
1             P1        F2
2             P2        F2

Test: Each FAMILY|ID links to at least 1 PARTICIPANT|ID                         Result: ✅

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test: Each PARTICIPANT|ID links to at least 1 FAMILY|ID                         Result: ✅

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test: Each PARTICIPANT|ID links to at least 1 BIOSPECIMEN|ID                    Result: ❌

Error Reasons:
	('PARTICIPANT|ID', 'P2') -> []

Locations:
	('PARTICIPANT|ID', 'P2') found in ['DATASET3/fp.csv']

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test: Each BIOSPECIMEN|ID links to exactly 1 PARTICIPANT|ID                     Result: ✅

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test: Each BIOSPECIMEN|ID links to at least 1 GENOMIC_FILE|URL_LIST             Result: ❌

Error Reasons:
	('BIOSPECIMEN|ID', 'B1') -> []

Locations:
	('BIOSPECIMEN|ID', 'B1') found in ['DATASET3/pb.csv']

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test: Each GENOMIC_FILE|URL_LIST links to exactly 1 BIOSPECIMEN|ID              Result: ⛔

==========================================================================================
======================================== DATASET4 ========================================
==========================================================================================

DATASET4/fb.csv
  BIOSPECIMEN|ID FAMILY|ID
0             B1        F2

DATASET4/fp.csv
  PARTICIPANT|ID FAMILY|ID
0             P1        F1
1             P1        F2
2             P2        F2

Test: Each FAMILY|ID links to at least 1 PARTICIPANT|ID                         Result: ✅

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test: Each PARTICIPANT|ID links to at least 1 FAMILY|ID                         Result: ✅

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test: Each PARTICIPANT|ID links to at least 1 BIOSPECIMEN|ID                    Result: ✅

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test: Each BIOSPECIMEN|ID links to exactly 1 PARTICIPANT|ID                     Result: ❌

Error Reasons:
	('BIOSPECIMEN|ID', 'B1') -> [('PARTICIPANT|ID', 'P1'), ('PARTICIPANT|ID', 'P2')]

Locations:
	('BIOSPECIMEN|ID', 'B1') found in ['DATASET4/fb.csv']
	('PARTICIPANT|ID', 'P1') found in ['DATASET4/fp.csv']
	('PARTICIPANT|ID', 'P2') found in ['DATASET4/fp.csv']

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test: Each BIOSPECIMEN|ID links to at least 1 GENOMIC_FILE|URL_LIST             Result: ❌

Error Reasons:
	('BIOSPECIMEN|ID', 'B1') -> []

Locations:
	('BIOSPECIMEN|ID', 'B1') found in ['DATASET4/fb.csv']

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test: Each GENOMIC_FILE|URL_LIST links to exactly 1 BIOSPECIMEN|ID              Result: ⛔

==========================================================================================
======================================== DATASET5 ========================================
==========================================================================================

DATASET5/pb.csv
  BIOSPECIMEN|ID PARTICIPANT|ID
0             B1             P1

DATASET5/fb.csv
  BIOSPECIMEN|ID FAMILY|ID
0             B1        F1
1             B2        F2

DATASET5/fp.csv
  PARTICIPANT|ID FAMILY|ID
0             P1        F2

Test: Each FAMILY|ID links to at least 1 PARTICIPANT|ID                         Result: ✅

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test: Each PARTICIPANT|ID links to at least 1 FAMILY|ID                         Result: ✅

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test: Each PARTICIPANT|ID links to at least 1 BIOSPECIMEN|ID                    Result: ✅

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test: Each BIOSPECIMEN|ID links to exactly 1 PARTICIPANT|ID                     Result: ✅

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test: Each BIOSPECIMEN|ID links to at least 1 GENOMIC_FILE|URL_LIST             Result: ❌

Error Reasons:
	('BIOSPECIMEN|ID', 'B1') -> []
	('BIOSPECIMEN|ID', 'B2') -> []

Locations:
	('BIOSPECIMEN|ID', 'B1') found in ['DATASET5/pb.csv', 'DATASET5/fb.csv']
	('BIOSPECIMEN|ID', 'B2') found in ['DATASET5/fb.csv']

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test: Each GENOMIC_FILE|URL_LIST links to exactly 1 BIOSPECIMEN|ID              Result: ⛔
```
