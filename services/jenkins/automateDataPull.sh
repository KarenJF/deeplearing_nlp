# This shell script calls a python script to get CaseLaw Data

#curl "https://api.case.law/v1/cases/?jurisdiction=ill&page_size=1"

#echo $PWD
#cd ..
#echo $PWD

python3 ./services/caselaw/GetSampleDataFromCaseLaw.py
