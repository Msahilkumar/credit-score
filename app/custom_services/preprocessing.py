import numpy as np
import pandas as pd



class PreProcess_test_data():
    def __init__(self,x):
        self.x = x
        self.drop_col_list = ['total_cu_tl', 'mths_since_rcnt_il', 'max_bal_bc', 'all_util', 'inq_last_12m', 
                              'open_il_12m', 'open_il_24m', 'open_rv_12m', 'il_util', 'open_il_6m', 'mths_since_last_record', 
                              'total_bal_il', 'dti_joint', 'inq_fi', 'desc', 'verification_status_joint', 'annual_inc_joint', 
                              'open_acc_6m', 'open_rv_24m','id','member_id','sub_grade','funded_amnt_inv','title','url',
                              'zip_code','collection_recovery_fee','total_rec_late_fee','next_pymnt_d',
                              'initial_list_status', 'addr_state', 'application_type', 'emp_title', 'pymnt_plan', 'policy_code',
                              'out_prncp_inv', 'total_pymnt_inv', 'funded_amnt','recoveries']
        self.training_columns = ['loan_amnt', 'term', 'int_rate', 'installment', 'grade', 'emp_length', 'home_ownership', 
                                 'annual_inc', 'verification_status', 'purpose', 'dti', 'delinq_2yrs', 'inq_last_6mths', 
                                 'mths_since_last_delinq', 'open_acc', 'pub_rec', 'revol_bal', 'revol_util', 'total_acc', 
                                 'out_prncp', 'total_pymnt', 'total_rec_prncp', 'total_rec_int', 'last_pymnt_amnt', 
                                 'collections_12_mths_ex_med', 'mths_since_last_major_derog', 'acc_now_delinq', 'tot_coll_amt', 
                                 'tot_cur_bal', 'total_rev_hi_lim', 'earliest_cr_line_months_since', 'issue_d_months_since', 
                                 'last_pymnt_d_months_since', 'last_credit_pull_d_months_since', 'grade:A', 'grade:B', 'grade:C',
                                   'grade:D', 'grade:E', 'grade:F', 'grade:G', 'home_ownership:ANY', 'home_ownership:MORTGAGE', 
                                   'home_ownership:OWN', 'home_ownership:RENT', 'verification_status:Not Verified', 
                                   'verification_status:Source Verified', 'verification_status:Verified', 'purpose:car', 
                                   'purpose:credit_card', 'purpose:debt_consolidation', 'purpose:educational', 'purpose:home_improvement', 
                                   'purpose:house', 'purpose:major_purchase', 'purpose:medical', 'purpose:moving', 'purpose:other', 
                                   'purpose:renewable_energy', 'purpose:small_business', 'purpose:vacation', 'purpose:wedding']
       
    def emp_length_converter(self, column):
        self.x[column] = self.x[column].str.replace('+ years', '')
        self.x[column] = self.x[column].str.replace('< 1 year', str(0))
        self.x[column] = self.x[column].str.replace(' years', '')
        self.x[column] = self.x[column].str.replace(' year', '')
        self.x[column] = self.x[column].str.replace('+', '')
        self.x[column] = pd.to_numeric(self.x[column])
        self.x[column] = self.x[column].fillna(value = 0)

    def months_since_date(self,col):
        # Get the current date
        today = pd.to_datetime('2020-08-01')
        self.x[col] = pd.to_datetime(self.x[col],format='%b-%y')
        self.x[f'{col}_months_since'] = ((today.year - self.x[col].dt.year) * 12 + (today.month - self.x[col].dt.month))

        self.x.drop([col],axis=1,inplace=True)
    
    def loan_term_converter(self, column):
        self.x[column] = pd.to_numeric(self.x[column].str.replace(' months', ''))

    def col_to_drop(self, columns_list):
        self.x.drop(columns = columns_list, inplace = True)
    
    def dummy_creation(self, columns_list):
        df_dummies = []
        for col in columns_list:
            df_dummies.append(pd.get_dummies(self.x[col], prefix = col, prefix_sep = ':'))
        df_dummies = pd.concat(df_dummies, axis = 1)
        self.x = pd.concat([self.x, df_dummies], axis = 1)

    def preprocess(self):
        self.col_to_drop(self.drop_col_list)
        self.emp_length_converter('emp_length')
        self.months_since_date('earliest_cr_line')
        self.months_since_date('issue_d')
        self.months_since_date('last_pymnt_d')
        self.months_since_date('last_credit_pull_d')
        self.loan_term_converter('term')
        self.dummy_creation(['grade', 'home_ownership', 'verification_status', 'purpose'])
        self.x  = self.x.reindex(columns=self.training_columns,fill_value=0)
        if 'Unnamed: 0' in self.x.columns:
            self.x.drop('Unnamed: 0',axis=1,inplace=True)

        return self.x

