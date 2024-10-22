class constants():
    def __init__(self):
        pass
    scorecard_scores =  [ 602,   81,   63,  52,   41,   32,   16,   -4,   -5,   -9,  -10,    3,    5,    5,
                    8,  -24,   20,   17,   11,    8,    1,    0,   18,   15,   10,    6,    3,    1,
                    0,   -5,    6,    5,    7,    5,    4,    2,    0,    2,    0,   -2,    5,   -2,
                    -3,   -5,   13,  -16,   17,    0,  -28,  -11,  -17,   21,   85,   56,   38,   18,
                    -120,  -75,  -41,  -31,  -25,  -13,   13,    0,    4,    3,    2,    3,   -1,   -1,
                    0,   -7,   -7,   -6,   -3,   -4,   92,   16,  -25,  -53,  -54,  -20,  -31
                    ]


    required_columns = ['id', 'member_id', 'loan_amnt', 'funded_amnt', 'funded_amnt_inv', 
                    'term', 'int_rate', 'installment', 'grade', 'sub_grade', 'emp_title', 
                    'emp_length', 'home_ownership', 'annual_inc', 'verification_status', 
                    'issue_d', 'pymnt_plan', 'url', 'desc', 'purpose', 'title', 
                    'zip_code', 'addr_state', 'dti', 'delinq_2yrs', 'earliest_cr_line', 
                    'inq_last_6mths', 'mths_since_last_delinq', 'mths_since_last_record', 
                    'open_acc', 'pub_rec', 'revol_bal', 'revol_util', 'total_acc', 'initial_list_status', 
                    'out_prncp', 'out_prncp_inv', 'total_pymnt', 'total_pymnt_inv', 'total_rec_prncp', 
                    'total_rec_int', 'total_rec_late_fee', 'recoveries', 'collection_recovery_fee', 'last_pymnt_d', 
                    'last_pymnt_amnt', 'next_pymnt_d', 'last_credit_pull_d', 'collections_12_mths_ex_med', 
                    'mths_since_last_major_derog', 'policy_code', 'application_type', 'annual_inc_joint', 'dti_joint',
                    'verification_status_joint', 'acc_now_delinq', 'tot_coll_amt', 'tot_cur_bal', 'open_acc_6m', 'open_il_6m',
                    'open_il_12m', 'open_il_24m', 'mths_since_rcnt_il', 'total_bal_il', 'il_util', 'open_rv_12m', 'open_rv_24m',
                    'max_bal_bc', 'all_util', 'total_rev_hi_lim', 'inq_fi', 'total_cu_tl', 'inq_last_12m'
                        ]

    ref_categories = ['last_credit_pull_d_months_since:>75', 'issue_d_months_since:>122', 'earliest_cr_line_months_since:>434', 'total_rev_hi_lim:>79,780',
                    'total_rec_int:>7,260', 'total_pymnt:>25,000', 'out_prncp:>15,437', 'revol_util:>1.0', 'inq_last_6mths:>4', 'dti:>35.191',
                    'annual_inc:>150K', 'int_rate:>20.281', 'term:60', 'purpose:major_purch__car__home_impr', 'verification_status:Not Verified',
                    'home_ownership:MORTGAGE', 'grade:G']