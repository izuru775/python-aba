import datetime
from aba.generator import AbaFile
from aba import records
# 
import requests
import json

# connect to an api get the data
r = requests.get('https://07db78ea-5dec-4187-af8d-62b87341ca34.mock.pstmn.io/aba')
data = json.loads(r.text)

newData = data['data']
#loop through new data and create a new record for each item
for item in newData:
    header = records.DescriptiveRecord(
        user_bank=item['user_bank'],
        user_name=item['user_name'],
        user_number=item['user_number'],
        description=item['description'],
        date=datetime.date(item['year'],item['month'],item['date'])
    )

    entry = records.DetailRecord(
        bsb=item['entry']['bsb'],
        account_number=item['entry']['account_number'],
        txn_code=item['entry']['txn_code'],
        amount=item['entry']['amount'],
        payee_name=item['entry']['payee_name'],
        lodgment_ref=item['entry']['lodgment_ref'],
        sender_bsb=item['entry']['sender_bsb'],
        sender_account=item['entry']['sender_account'],
        remitter_name=item['entry']['remitter_name'],
    )

    aba_file = AbaFile(header)
    aba_file.add_record(entry)

    print (aba_file.render_to_string())
    #  Create file/ Write to file
    f = open("myfile.txt", "a")
    f.write(aba_file.render_to_string()+"\r")
    f.close()