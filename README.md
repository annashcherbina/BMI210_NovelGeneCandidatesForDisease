# BMI210_NovelGeneCandidatesForDisease
Code for BMI210 final project: Finding novel gene candidates for rare diseases 

The program has been implemented in Python, and the main executable is "find\_novel\_genes.py". This script will query the MySQL database instance that is running on the Amazon Web Services cloud, so it is not necessary to restore the MySQL database from the attached MySQL dump file prior to executing the script (although it is possible to execute the script with a local database instance as well by passing the appropriate flag).

Executing the Python script with no input arguments will cause a help message to be printed (Figure 1):
![](readme_images/help_message_from_code.png?raw=true)

The list of required and optional arguments to find\_novel\_genes.py is as follows:
Markup : *subject id (-subject). This is the identifier used to reference the subject in PGP, such as "huB1FD55".
*subject's diagnosis  (-disease). The database query will return any string, such that the -disease argument is a substring of this string. Providing "hypertrophic" as the argument will match "hypertrophic cardiomyopathy" and similar variations of the disease name.
*list of genes whose mutations are known to cause the disease (-genes). This argument is optional. If it is not provided, the list of genes will be queried from the MySQL "gene\_disease" table.
*boolean flag indicating whether to filter by cellular location (-filterByCellularLocation). If this flag is provided, associated genes must be in the same pathway as the input genes, and in the same cellular location. If the flag is not provided, the associated genes may be in a different cellular location from the input gene.
*minor allele frequency threshold (-maf). Indicates the highest allowed minor allele frequency for a variant to be reported. The default is maf=0.01.
*various database connection parameters (-h, -u, -p, -db, -port). These indicate, respectively, the host, username, password, database name, port to use when connecting to the system database. By default, the system will use the AWS database instance with preset connection parameters.

Examples of how the program can be executed for the three HCM patients analyzed in this project are provided in the shell script  included with the submission: "find\_novel\_genes.sh", illustrated in Figure 2:

![](readme_images/example_execution.png?raw=true)

"find\_novel\_genes.py" will generate an output file, as specified by the \-o flag. An example output file for subject "huB1FD55" is illustrated in Figure 3.

![](readme_images/code_output.png?raw=true)

