# ppRank

Alpha version with most useful functions implemented.

Developed by Tiago Costa Soares, Pedro Augusto Mendes


# Overview

The project implements a bi-objective lexicographic ranking approach. The classification is done based on two input files, one containing the results of each algorithm, and the other containing the execution times for each scenario.

# Installation

Make sure you have Python 3 installed. Then, you can install the package using the following command:


from ppRank import bilex, par10


# Usage

After installing the package.
O pacote pode ser encontrado em: https://test.pypi.org/project/ppRank/


## Function bilex:

The bilex function takes three input parameters, the first parameter is the results.csv file that contains the results of each algorithm, the second file is the time.csv that contains the execution time for each of the scenarios, and finally a boolean has_header, which indicates whether the files have a header(true) or not(false). The has_header parameter defaults to false. The return is a matrix with the results properly ranked.

The bilex function can be executed in two ways:

### 1- The first way is to execute the function using only the csv files as parameters, as follows:

    matrix_ranking = bilex('results.csv', 'time.csv')
    
'Replace 'results.csv' and 'time.csv' with your file names'

In this case, the header will not be considered, since has_header is false by default. If your files have a header, it is recommended to use the second approach, in order to avoid possible errors in the classification of the algorithms.

### 2- The second way is to execute the function using the files and the boolean as parameters.

    matrix_ranking = bilex('results.csv', 'time.csv', 'has_header')

'Replace 'results.csv' and 'time.csv' with your file names'

This approach is recommended for files that have a header line. By assigning true to has_header, the function will no longer apply the classification to the first line of the files.



## Function par10

The par10 function takes two input parameters, the first parameter is the G.csv file that contains the results of each algorithm, the second parameter is a boolean has_header, which indicates whether the files have a header(true) or not(false). The has_header parameter defaults to false. The return is a matrix with the results properly ranked.

The par10 function can be executed in two ways:

### 1- The first way is to execute the function using only the csv file as a parameter, as follows:

    matrix_par10 = par10('G.csv')
    
'Replace 'G.csv' with your file name'

In this case, the header will not be considered, since has_header is false by default. If your file has a header, it is recommended to use the second approach, in order to avoid possible errors in the classification of the algorithms.

### 2- The second way is to execute the function using the file and the boolean as parameters.

    matrix_ranking = par10('G.csv', 'has_header')

'Replace 'G.csv' with your file name'

This approach is recommended for files that have a header line. By assigning true to has_header, the function will no longer apply the classification to the first line of the files.


## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.