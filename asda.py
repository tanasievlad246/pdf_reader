# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/etl')
from nb_module import *

sql_select_nb_collection_fee = f"""
SELECT CLT_NO, DBR_ASSIGN_AMT, CLT_COLL_FEE_PER,
@comm_fee := IFNULL(
IF (DBR_ASSIGN_AMT <= COM_T_ASS_AMT1, COM_FEE1,
IF (DBR_ASSIGN_AMT <= COM_T_ASS_AMT2, COM_FEE2,
IF (DBR_ASSIGN_AMT <= COM_T_ASS_AMT3, COM_FEE3,
IF (DBR_ASSIGN_AMT <= COM_T_ASS_AMT4, COM_FEE4,
IF (DBR_ASSIGN_AMT <= COM_T_ASS_AMT5, COM_FEE5,
IF (DBR_ASSIGN_AMT <= COM_T_ASS_AMT6, COM_FEE6, 0
)))))),0) AS comm_fee,
ROUND(IF(@comm_fee > 0, @comm_fee, CLT_COLL_FEE_PER)/100,2) AS ACTUAL_FEE
FROM CDS.CLT 
LEFT JOIN CDS.COM 
ON CLT_COMM_RULE = COM_CODE
LEFT JOIN CDS.DBR
ON CLT_NO = DBR_CLIENT
WHERE CLT_NO = {client_id}
"""

config_obj = {
    'commit_flag': 'N',
    'locale': 'en_US.utf8',
    'timezone': 'US/Central',
    'dbr_posterid': 'gabriel.dinu@dandsltd.com',
    'usr_code': 'EDI',
    'dbr_desk': '001',
    'invoice_new_open_closed_account': True,
    'invoice_new_add_IAD_note': True,
    'flag_for_pif': True,
    'do_not_reopen': ('PIE', 'REC', 'DUP', 'FPS', 'CWO'),
    'invoice_update_ivt_date': True,
    'invoice_update_due_date': True}

def parseNB(filename):
    """ Read and parse the nb file
    """
    # Return list
    parse_obj = dict()
    parse_obj['row_count'] = 0
    parse_obj['account_count'] = 0
    parse_obj['filename'] = filename
    # add other optional aggregate keys about the parse here e.g. total amount, etc
    parse_obj['dbr_data_obj_list'] = list()
    reqs = [['dbr_client', 'client_id'],
            ['dbr_agency', 'agency_id'],
            ['dbr_cli_ref_no', 'cli_ref'],
            ['dbr_name1', 'name1'],
            ['dbr_assign_amt', 'balance'],
            ['adr_addr1','addr1', 'add1'],
            ['adr_city','city1'],
            ['adr_state', 'state1', 'state'],
            ['adr_zip_code','zip1'],
            ['adr_cntry','country1'],
            ['adr_phone1','phone1'],
            # ['ivt_ivt_no','inv_num'],
            # ['ivt_ivt_date_o','inv_date'],
            # ['ivt_due_date','inv_due_date'],
            ['adr_email', 'email'],
            ['name2'],
            ['adr_addr2', 'addr2', 'add2'],
            ['adr_phone2', 'phone2'],
            ['dom'],
            ['ssn'],
            # ['other_amt'],
            ['interest_amt'],
            ['dbr_cl_misc_1', 'misc1'],
            ['dbr_cl_misc_2', 'misc2'],
            ['dbr_cl_misc_3', 'misc3'],
            ['dbr_cl_misc_4', 'misc4'],
            ['dbr_cl_codes_1', 'code1'],
            ['dbr_cl_codes_2', 'code2'],
            ['dbr_cl_codes_3', 'code3'],
            ['dbr_cl_codes_4', 'code4']]
    debtor_list = []
    # Parse the inv file
    rows = csv.reader(open(filename), delimiter=",")
    header = next(rows)
    h = flexibleHeaderMap(header, reqs)
    for l in rows:
        parse_obj['row_count'] += 1
        dbr_data_obj = dict()
        if len(l[h['dbr_cli_ref_no']]) > 1:
            client_ref = l[h['dbr_cli_ref_no']]
            agency_id = l[h['dbr_agency']]

            # track unique accounts
            if client_ref not in debtor_list:
                debtor_list.append(client_ref)
                parse_obj['account_count'] += 1
            # Required fields
            dbr_data_obj['dbr_cli_ref_no'] = client_ref
            dbr_data_obj['dbr_name1'] = tigerDeQuote(strip_non_ascii(l[h['dbr_name1']]))
            dbr_data_obj['dbr_agency'] = agency_id

            adr_name = tigerDeQuote(strip_non_ascii(l[h['dbr_name1']]))

            if 'adr_addr1' in h:
                adr_addr1 = l[h['adr_addr1']]
            else:
                adr_addr1 = ''

            if 'adr_city' in h:
                adr_city = l[h['adr_city']]
            else:
                adr_city = ''

            if 'adr_state' in h:
                adr_state = l[h['adr_state']]
            else:
                adr_state = ''

            if 'adr_zip_code' in h:
                adr_zip_code = l[h['adr_zip_code']]
            else:
                adr_zip_code = ''

            if 'adr_cntry' in h:
                adr_cntry = l[h['adr_cntry']]
            else:
                adr_cntry = ''

            if 'dbr_assign_amt' in h:
                dbr_assign_amt = l[h['dbr_assign_amt']]
            else:
                dbr_assign_amt = ''

            if 'dbr_cl_misc_1' in h:
                dbr_cl_misc_1 = l[h['dbr_cl_misc_1']]
            else:
                dbr_cl_misc_1 = ''

            if 'dbr_cl_misc_2' in h:
                dbr_cl_misc_2 = l[h['dbr_cl_misc_2']]
            else:
                dbr_cl_misc_2 = ''

            if 'dbr_cl_misc_3' in h:
                dbr_cl_misc_3 = l[h['dbr_cl_misc_3']]
            else:
                dbr_cl_misc_3 = ''

            if 'dbr_cl_misc_4' in h:
                dbr_cl_misc_4 = l[h['dbr_cl_misc_4']]
            else:
                dbr_cl_misc_4 = ''

            dbr_data_obj['dbr_cl_misc_1'] = dbr_cl_misc_1
            dbr_data_obj['dbr_cl_misc_2'] = dbr_cl_misc_2
            dbr_data_obj['dbr_cl_misc_3'] = dbr_cl_misc_3
            dbr_data_obj['dbr_cl_misc_4'] = dbr_cl_misc_4


            dbr_data_obj['adr_data_obj_list'] = [
                {
                    'adr_name': adr_name,
                    'adr_addr1': adr_addr1,
                    'adr_city': adr_city,
                    'adr_state': adr_state,
                    'adr_zip_code': adr_zip_code,
                    'adr_cntry': adr_cntry,
                    'adr_phone1': cleanPhoneNo(l[h['adr_phone1']]),
                    'adr_email': l[h['adr_email']],
                }
            ]

            parse_obj['dbr_data_obj_list'].append(dbr_data_obj)
        return parse_obj




def parseINV(filename, clientID):
    parse_obj = dict()
    parse_obj['row_count'] = 0
    parse_obj['invoice_count'] = 0
    parse_obj['ivt_data_obj_list'] = list()

    reqs = [['dbr_client', 'client_id'],
            ['dbr_agency', 'agency_id'],
            ['dbr_cli_ref_no', 'cli_ref'],
            ['ivt_ivt_no','inv_num'],
            ['ivt_amount', 'balance'],
            ['ivt_ivt_date_o','inv_date'],
            ['ivt_due_date','inv_due_date'],
            ['interest_amt'],
            ['dbr_cl_misc_1', 'misc1'],
            ['dbr_cl_misc_2', 'misc2'],
            ['dbr_cl_misc_3', 'misc3'],
            ['dbr_cl_misc_4', 'misc4'],
            ['dbr_cl_codes_1', 'code1'],
            ['dbr_cl_codes_2', 'code2'],
            ['dbr_cl_codes_3', 'code3'],
            ['dbr_cl_codes_4', 'code4']]

    ivt_key_list = []
    rows = csv.reader(open(filename), delimiter=",")
    header = next(rows)
    h = flexibleHeaderMap(header, reqs)
    # full_amount = 0
    for l in rows:

        parse_obj['row_count'] += 1
        ivt_data_obj = dict()
        if len(l[h['dbr_cli_ref_no']]) > 1:
            # track unique invoices
            client_ref = l[h['dbr_cli_ref_no']]
            inv_date = l[h['ivt_ivt_date_o']]
            inv_due_date = l[h['ivt_due_date']]

            if (client_ref, l[h['ivt_ivt_no']]) not in ivt_key_list:
                ivt_key_list.append((client_ref, l[h['ivt_ivt_no']]))
                parse_obj['invoice_count'] += 1
            # Required fields
            ivt_data_obj['dbr_cli_ref_no'] = client_ref
            ivt_data_obj['ivt_ivt_no'] = l[h['ivt_ivt_no']]
            ivt_data_obj['ivt_amount'] = getCleanNumericString(l[h['ivt_amount']])
            ivt_data_obj['ivt_due'] = getCleanNumericString(l[h['ivt_amount']])
            ivt_data_obj['ivt_ivt_date_o'] = inv_date
            ivt_data_obj['ivt_due_date'] = inv_due_date

            parse_obj['ivt_data_obj_list'].append(ivt_data_obj)
    #         full_amount += (float(ivt_data_obj['ivt_amount']))
    # print(full_amount)
    return parse_obj

    db = getDBConnection()
    # Explicitly start a transaction
    curs = db.cursor()

    collection_fee_info = sqlSelectList(curs, sql_select_nb_collection_fee, (float('DBR_ASSIGN_AMT'), client_id))[0]
    print(sql_select_nb_collection_fee)
    print(collection_fee_info)
    print('DBR_ASSIGN_AMT')


if __name__ == '__main__':
    # Parse args
    usage = f"Usage: %prog <commit Y/N> <nb file> <client id>"
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    if len(args) != 3:
        parser.error("Please specify the commit flag, the nb file and the client ID")
    else:
        try:
            moved_acct = 0
            client_id = args[2]
            flag = args[0]

            config_obj['commit_flag'] = flag
            config_obj['client_list'] = "'" + client_id + "'"
            config_obj['dbr_client'] = client_id

            nb_parse_obj = parseNB(args[1])
            nb_result_obj = postNB(nb_parse_obj, config_obj)
            printNB(nb_result_obj, nb_parse_obj)

            inv_parse_obj = parseINV(args[1], client_id)
            inv_result_obj = postINV(inv_parse_obj, config_obj)
            printINV(inv_result_obj, inv_parse_obj)

        except:
            print(sys.exc_info())
            raise