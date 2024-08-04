## SQL cheatsheet
_In the spirit of continuous development_

Structured Query Language (SQL) is nonprocedural query language, i.e.,
it can do much more than just query results. it is used widely for- -
writing ETL pipelines, - designing data models, - querying underlying
data, etc.

### In the field of Business Analytics -

-   it is used for scheduling jobs,
-   projection calculations,
-   creating dashboards,
-   automated reports, etc.

## SQL Command Categories:

### A. Data Definition Language (DDL):

-   includes commands for defining schema, deleting relations, modifying
    the schema.
-   It consists of commands for specific integrity constraints examples:
    -   CREATE,
    -   DROP,
    -   TRUNCATE,
    -   ALTER,
    -   COMMENT,
    -   RENAME

### B. Data Query Language (DQL):

-   includes commands to perform operations on data within the defined
    schema.
-   example:
    -   SELECT

### C. Data Manipulation Language (DML):

-   includes commands to manipulate data in the database
-   examples:
    -   INSERT,
    -   UPDATE,
    -   DELETE

### D. Data Control Language (DCL):

-   includes the command to control rights and permission of the
    database.
-   example:
    -   GRANT,
    -   REVOKE

## R session information

``` r
sessionInfo()
```

R version 4.3.3 (2024-02-29) Platform: aarch64-apple-darwin23.2.0
(64-bit) Running under: macOS Sonoma 14.4.1

Matrix products: default BLAS:
/opt/homebrew/Cellar/openblas/0.3.26/lib/libopenblasp-r0.3.26.dylib
LAPACK: /opt/homebrew/Cellar/r/4.3.3/lib/R/lib/libRlapack.dylib; LAPACK
version 3.11.0

locale: \[1\]
en_US.UTF-8/en_US.UTF-8/en_US.UTF-8/C/en_US.UTF-8/en_US.UTF-8

time zone: America/Los_Angeles tzcode source: internal

attached base packages: \[1\] stats graphics grDevices utils datasets
methods base

loaded via a namespace (and not attached): \[1\] compiler_4.3.3
fastmap_1.1.1 cli_3.6.2 tools_4.3.3  
\[5\] htmltools_0.5.8.1 rstudioapi_0.16.0 yaml_2.3.8 rmarkdown_2.26  
\[9\] knitr_1.45 xfun_0.43 digest_0.6.35 rlang_1.1.3  
\[13\] evaluate_0.23
