#python find_novel_genes.py -subject huA9D22A -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 GLA LAMP2 MYBPC3 MYH7 MYL2 MYL3 PRKAG2 TNNI3 TNNT2 TPM1 TNNC1 TTR 
#python find_novel_genes.py -subject huB1FD55 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 GLA LAMP2 MYBPC3 MYH7 MYL2 MYL3 PRKAG2 TNNI3 TNNT2 TPM1 TNNC1 TTR
#python find_novel_genes.py -subject huB1FD55 -disease "Hypertrophic" -filterByCellularLocation
#python find_novel_genes.py -subject huED0F40 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 GLA LAMP2 MYBPC3 MYH7 MYL2 MYL3 PRKAG2 TNNI3 TNNT2 TPM1 TNNC1 TTR


#variant LOOCV
#python find_novel_genes.py -subject huB1FD55 -disease "Hypertrophic" -filterByCellularLocation -genes GLA LAMP2 MYBPC3 MYH7 MYL2 MYL3 PRKAG2 TNNI3 TNNT2 TPM1 TNNC1 TTR -o cv.ACTC1
#python find_novel_genes.py -subject huB1FD55 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 LAMP2 MYBPC3 MYH7 MYL2 MYL3 PRKAG2 TNNI3 TNNT2 TPM1 TNNC1 TTR -o cv.GLA
#python find_novel_genes.py -subject huB1FD55 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 GLA MYBPC3 MYH7 MYL2 MYL3 PRKAG2 TNNI3 TNNT2 TPM1 TNNC1 TTR -o cv.LAMP2
#python find_novel_genes.py -subject huB1FD55 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 GLA LAMP2 MYH7 MYL2 MYL3 PRKAG2 TNNI3 TNNT2 TPM1 TNNC1 TTR -o cv.MYBPC3
#python find_novel_genes.py -subject huB1FD55 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 GLA LAMP2 MYBPC3 MYL2 MYL3 PRKAG2 TNNI3 TNNT2 TPM1 TNNC1 TTR -o cv.MYH7
#python find_novel_genes.py -subject huB1FD55 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 GLA LAMP2 MYBPC3 MYH7 MYL3 PRKAG2 TNNI3 TNNT2 TPM1 TNNC1 TTR -o cv.MYL2
#python find_novel_genes.py -subject huB1FD55 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 GLA LAMP2 MYBPC3 MYH7 MYL2 MYL3 PRKAG2 TNNI3 TNNT2 TPM1 TNNC1 TTR -o cv.MYL3
#python find_novel_genes.py -subject huB1FD55 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 GLA LAMP2 MYBPC3 MYH7 MYL2 MYL3 TNNI3 TNNT2 TPM1 TNNC1 TTR -o cv.PRKAG2
#python find_novel_genes.py -subject huB1FD55 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 GLA LAMP2 MYBPC3 MYH7 MYL2 MYL3 PRKAG2 TNNT2 TPM1 TNNC1 TTR -o cv.TNNI3
#python find_novel_genes.py -subject huB1FD55 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 GLA LAMP2 MYBPC3 MYH7 MYL2 MYL3 PRKAG2 TNNI3 TPM1 TNNC1 TTR -o cv.TNNT2
#python find_novel_genes.py -subject huB1FD55 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 GLA LAMP2 MYBPC3 MYH7 MYL2 MYL3 PRKAG2 TNNI3 TNNT2 TNNC1 TTR -o cv.TPM1
#python find_novel_genes.py -subject huB1FD55 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 GLA LAMP2 MYBPC3 MYH7 MYL2 MYL3 PRKAG2 TNNI3 TNNT2 TPM1 TTR -o cv.TNNC1
#python find_novel_genes.py -subject huB1FD55 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 GLA LAMP2 MYBPC3 MYH7 MYL2 MYL3 PRKAG2 TNNI3 TNNT2 TPM1 TNNC1 -o cv.TTR

python find_novel_genes.py -subject huED0F40 -disease "Hypertrophic" -filterByCellularLocation -genes GLA LAMP2 MYBPC3 MYH7 MYL2 MYL3 PRKAG2 TNNI3 TNNT2 TPM1 TNNC1 TTR -o cv.ACTC1
python find_novel_genes.py -subject huED0F40 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 LAMP2 MYBPC3 MYH7 MYL2 MYL3 PRKAG2 TNNI3 TNNT2 TPM1 TNNC1 TTR -o cv.GLA
python find_novel_genes.py -subject huED0F40 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 GLA MYBPC3 MYH7 MYL2 MYL3 PRKAG2 TNNI3 TNNT2 TPM1 TNNC1 TTR -o cv.LAMP2
python find_novel_genes.py -subject huED0F40 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 GLA LAMP2 MYH7 MYL2 MYL3 PRKAG2 TNNI3 TNNT2 TPM1 TNNC1 TTR -o cv.MYBPC3
python find_novel_genes.py -subject huED0F40 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 GLA LAMP2 MYBPC3 MYL2 MYL3 PRKAG2 TNNI3 TNNT2 TPM1 TNNC1 TTR -o cv.MYH7
python find_novel_genes.py -subject huED0F40 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 GLA LAMP2 MYBPC3 MYH7 MYL3 PRKAG2 TNNI3 TNNT2 TPM1 TNNC1 TTR -o cv.MYL2
python find_novel_genes.py -subject huED0F40 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 GLA LAMP2 MYBPC3 MYH7 MYL2 PRKAG2 TNNI3 TNNT2 TPM1 TNNC1 TTR -o cv.MYL3
python find_novel_genes.py -subject huED0F40 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 GLA LAMP2 MYBPC3 MYH7 MYL2 MYL3 TNNI3 TNNT2 TPM1 TNNC1 TTR -o cv.PRKAG2
python find_novel_genes.py -subject huED0F40 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 GLA LAMP2 MYBPC3 MYH7 MYL2 MYL3 PRKAG2 TNNT2 TPM1 TNNC1 TTR -o cv.TNNI3
python find_novel_genes.py -subject huED0F40 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 GLA LAMP2 MYBPC3 MYH7 MYL2 MYL3 PRKAG2 TNNI3 TPM1 TNNC1 TTR -o cv.TNNT2
python find_novel_genes.py -subject huED0F40 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 GLA LAMP2 MYBPC3 MYH7 MYL2 MYL3 PRKAG2 TNNI3 TNNT2 TNNC1 TTR -o cv.TPM1
python find_novel_genes.py -subject huED0F40 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 GLA LAMP2 MYBPC3 MYH7 MYL2 MYL3 PRKAG2 TNNI3 TNNT2 TPM1 TTR -o cv.TNNC1
python find_novel_genes.py -subject huED0F40 -disease "Hypertrophic" -filterByCellularLocation -genes ACTC1 GLA LAMP2 MYBPC3 MYH7 MYL2 MYL3 PRKAG2 TNNI3 TNNT2 TPM1 TNNC1 -o cv.TTR

