from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd


ref_categories = ['last_credit_pull_d_months_since:>75', 'issue_d_months_since:>122', 'earliest_cr_line_months_since:>434', 'total_rev_hi_lim:>79,780',
                  'total_rec_int:>7,260', 'total_pymnt:>25,000', 'out_prncp:>15,437', 'revol_util:>1.0', 'inq_last_6mths:>4', 'dti:>35.191',
                  'annual_inc:>150K', 'int_rate:>20.281', 'term:60', 'purpose:major_purch__car__home_impr', 'verification_status:Not Verified',
                  'home_ownership:MORTGAGE', 'grade:G']

# This custom class will create new categorical dummy features based on the cut-off points that we manually identified
# based on the WoE plots and IV above.
# Given the way it is structured, this class also allows a fit_transform method to be implemented on it, thereby allowing
# us to use it as part of a scikit-learn Pipeline
class WoE_Binning(BaseEstimator, TransformerMixin):
    def __init__(self, X): # no *args or *kargs
        self.X = X
    def fit(self, X, y = None):
        return self #nothing else to do
    def transform(self, X):
        X_new = X.loc[:, 'grade:A': 'grade:G']
        X_new['home_ownership:OWN'] = X.loc[:,'home_ownership:OWN']
        X_new['home_ownership:MORTGAGE'] = X.loc[:,'home_ownership:MORTGAGE']
        X_new['home_ownership:OTHER_NONE_RENT'] = sum([X['home_ownership:ANY'], X['home_ownership:RENT']])
        X_new = pd.concat([X_new, X.loc[:, 'verification_status:Not Verified':'verification_status:Verified']], axis = 1)
        # For the purpose of this column, we keep debt_consolidation (due to volume) and credit_card (due to unique characteristics) as separate cateogories
        # These categories have very few observations: educational, renewable_energy, vacation, house, wedding, car
        # car is the least risky so we will combine it with the other 2 least risky categories: home_improvement and major_purchase
        # educational, renewable_energy (both low observations) will be combined with small_business and moving
        # vacation, house and wedding (remaining 3 with low observations) will be combined with medical and other
        X_new['purpose:debt_consolidation'] = X.loc[:,'purpose:debt_consolidation']
        X_new['purpose:credit_card'] = X.loc[:,'purpose:credit_card']
        X_new['purpose:major_purch__car__home_impr'] = sum([X['purpose:major_purchase'], X['purpose:car'], X['purpose:home_improvement']])
        X_new['purpose:educ__ren_en__sm_b__mov'] = sum([X['purpose:educational'], X['purpose:renewable_energy'], X['purpose:small_business'],
                                                        X['purpose:moving']])
        X_new['purpose:vacation__house__wedding__med__oth'] = sum([X['purpose:vacation'], X['purpose:house'], X['purpose:wedding'],
                                                                   X['purpose:medical'], X['purpose:other']])
        X_new['term:36'] = np.where((X['term'] == 36), 1, 0)
        X_new['term:60'] = np.where((X['term'] == 60), 1, 0)
        X_new['int_rate:<7.071'] = np.where((X['int_rate'] <= 7.214), 1, 0)
        X_new['int_rate:7.071-10.374'] = np.where((X['int_rate'] > 7.214) & (X['int_rate'] <= 11.001), 1, 0)
        X_new['int_rate:10.374-13.676'] = np.where((X['int_rate'] > 11.001) & (X['int_rate'] <= 14.788), 1, 0)
        X_new['int_rate:13.676-15.74'] = np.where((X['int_rate'] > 14.788) & (X['int_rate'] <= 17.155), 1, 0)
        X_new['int_rate:15.74-20.281'] = np.where((X['int_rate'] > 17.155) & (X['int_rate'] <= 22.362), 1, 0)
        X_new['int_rate:>20.281'] = np.where((X['int_rate'] > 22.362), 1, 0)
        X_new['annual_inc:missing'] = np.where(X['annual_inc'].isnull(), 1, 0)
        X_new['annual_inc:<28,555'] = np.where((X['annual_inc'] <= 27000), 1, 0)
        X_new['annual_inc:28,555-37,440'] = np.where((X['annual_inc'] > 27000) & (X['annual_inc'] <= 36000), 1, 0)
        X_new['annual_inc:37,440-61,137'] = np.where((X['annual_inc'] > 36000) & (X['annual_inc'] <= 60000), 1, 0)
        X_new['annual_inc:61,137-81,872'] = np.where((X['annual_inc'] > 60000) & (X['annual_inc'] <= 81000), 1, 0)
        X_new['annual_inc:81,872-102,606'] = np.where((X['annual_inc'] > 81000) & (X['annual_inc'] <= 102000), 1, 0)
        X_new['annual_inc:102,606-120,379'] = np.where((X['annual_inc'] > 102000) & (X['annual_inc'] <= 120000), 1, 0)
        X_new['annual_inc:120,379-150,000'] = np.where((X['annual_inc'] > 120000) & (X['annual_inc'] <= 150000), 1, 0)
        X_new['annual_inc:>150K'] = np.where((X['annual_inc'] > 150000), 1, 0)
        X_new['dti:<=1.6'] = np.where((X['dti'] <= 1.7), 1, 0)
        X_new['dti:1.6-5.599'] = np.where((X['dti'] > 1.6) & (X['dti'] <= 5.872), 1, 0)
        X_new['dti:5.599-10.397'] = np.where((X['dti'] > 5.872) & (X['dti'] <= 10.904), 1, 0)
        X_new['dti:10.397-15.196'] = np.where((X['dti'] > 10.904) & (X['dti'] <= 15.098), 1, 0)
        X_new['dti:15.196-19.195'] = np.where((X['dti'] > 15.098) & (X['dti'] <= 19.292), 1, 0)
        X_new['dti:19.195-24.794'] = np.where((X['dti'] > 19.292) & (X['dti'] <= 24.325), 1, 0)
        X_new['dti:24.794-35.191'] = np.where((X['dti'] > 24.325) & (X['dti'] <= 35.230), 1, 0)
        X_new['dti:>35.191'] = np.where((X['dti'] > 35.230), 1, 0)
        X_new['inq_last_6mths:missing'] = np.where(X['inq_last_6mths'].isnull(), 1, 0)
        X_new['inq_last_6mths:0'] = np.where((X['inq_last_6mths'] == 0), 1, 0)
        X_new['inq_last_6mths:1-2'] = np.where((X['inq_last_6mths'] >= 1) & (X['inq_last_6mths'] <= 2), 1, 0)
        X_new['inq_last_6mths:3-4'] = np.where((X['inq_last_6mths'] >= 3) & (X['inq_last_6mths'] <= 4), 1, 0)
        X_new['inq_last_6mths:>4'] = np.where((X['inq_last_6mths'] > 4), 1, 0)
        # We will discretize on the deciles for revol_util
        X_new['revol_util:missing'] = np.where(X['revol_util'].isnull(), 1, 0)
        X_new['revol_util:<0.1'] = np.where((X['revol_util'] <= 0.1), 1, 0)
        X_new['revol_util:0.1-0.2'] = np.where((X['revol_util'] > 0.1) & (X['revol_util'] <= 0.2), 1, 0)
        X_new['revol_util:0.2-0.3'] = np.where((X['revol_util'] > 0.2) & (X['revol_util'] <= 0.3), 1, 0)
        X_new['revol_util:0.3-0.4'] = np.where((X['revol_util'] > 0.3) & (X['revol_util'] <= 0.4), 1, 0)
        X_new['revol_util:0.4-0.5'] = np.where((X['revol_util'] > 0.4) & (X['revol_util'] <= 0.5), 1, 0)
        X_new['revol_util:0.5-0.6'] = np.where((X['revol_util'] > 0.5) & (X['revol_util'] <= 0.6), 1, 0)
        X_new['revol_util:0.6-0.7'] = np.where((X['revol_util'] > 0.6) & (X['revol_util'] <= 0.7), 1, 0)
        X_new['revol_util:0.7-0.8'] = np.where((X['revol_util'] > 0.7) & (X['revol_util'] <= 0.8), 1, 0)
        X_new['revol_util:0.8-0.9'] = np.where((X['revol_util'] > 0.8) & (X['revol_util'] <= 0.9), 1, 0)
        X_new['revol_util:0.9-1.0'] = np.where((X['revol_util'] > 0.9) & (X['revol_util'] <= 1.0), 1, 0)
        X_new['revol_util:>1.0'] = np.where((X['revol_util'] > 1.0), 1, 0)
        X_new['out_prncp:<1,286'] = np.where((X['out_prncp'] <= 1975), 1, 0)
        X_new['out_prncp:1,286-6,432'] = np.where((X['out_prncp'] > 1975) & (X['out_prncp'] <= 6000), 1, 0)
        X_new['out_prncp:6,432-9,005'] = np.where((X['out_prncp'] > 6000) & (X['out_prncp'] <= 9875), 1, 0)
        X_new['out_prncp:9,005-10,291'] = np.where((X['out_prncp'] > 9875) & (X['out_prncp'] <= 15800), 1, 0)
        X_new['out_prncp:10,291-15,437'] = np.where((X['out_prncp'] > 15800) & (X['out_prncp'] <= 25675), 1, 0)
        X_new['out_prncp:>15,437'] = np.where((X['out_prncp'] > 27675), 1, 0)
        X_new['total_pymnt:<10,000'] = np.where((X['total_pymnt'] <= 1250), 1, 0)
        X_new['total_pymnt:10,000-15,000'] = np.where((X['total_pymnt'] > 1250) & (X['total_pymnt'] <= 2500), 1, 0)
        X_new['total_pymnt:15,000-20,000'] = np.where((X['total_pymnt'] > 2500) & (X['total_pymnt'] <= 5000), 1, 0)
        X_new['total_pymnt:>25,000'] = np.where((X['total_pymnt'] > 5000), 1, 0)
        X_new['total_rec_int:<1,089'] = np.where((X['total_rec_int'] <= 1089), 1, 0)
        X_new['total_rec_int:1,089-2,541'] = np.where((X['total_rec_int'] > 1089) & (X['total_rec_int'] <= 2541), 1, 0)
        X_new['total_rec_int:2,541-4,719'] = np.where((X['total_rec_int'] > 2541) & (X['total_rec_int'] <= 4719), 1, 0)
        X_new['total_rec_int:4,719-7,260'] = np.where((X['total_rec_int'] > 4719) & (X['total_rec_int'] <= 7260), 1, 0)
        X_new['total_rec_int:>7,260'] = np.where((X['total_rec_int'] > 7260), 1, 0)
        X_new['total_rev_hi_lim:missing'] = np.where(X['total_rev_hi_lim'].isnull(), 1, 0)
        X_new['total_rev_hi_lim:<6,381'] = np.where((X['total_rev_hi_lim'] <= 6381), 1, 0)
        X_new['total_rev_hi_lim:6,381-19,144'] = np.where((X['total_rev_hi_lim'] > 6381) & (X['total_rev_hi_lim'] <= 19144), 1, 0)
        X_new['total_rev_hi_lim:19,144-25,525'] = np.where((X['total_rev_hi_lim'] > 19144) & (X['total_rev_hi_lim'] <= 25525), 1, 0)
        X_new['total_rev_hi_lim:25,525-35,097'] = np.where((X['total_rev_hi_lim'] > 25525) & (X['total_rev_hi_lim'] <= 35097), 1, 0)
        X_new['total_rev_hi_lim:35,097-54,241'] = np.where((X['total_rev_hi_lim'] > 35097) & (X['total_rev_hi_lim'] <= 54241), 1, 0)
        X_new['total_rev_hi_lim:54,241-79,780'] = np.where((X['total_rev_hi_lim'] > 54241) & (X['total_rev_hi_lim'] <= 79780), 1, 0)
        X_new['total_rev_hi_lim:>79,780'] = np.where((X['total_rev_hi_lim'] > 79780), 1, 0)
        X_new['earliest_cr_line_months_since:missing'] = np.where(X['earliest_cr_line_months_since'].isnull(), 1, 0)
        X_new['earliest_cr_line_months_since:<125'] = np.where((X['earliest_cr_line_months_since'] <= 115), 1, 0)
        X_new['earliest_cr_line_months_since:125-167'] = np.where((X['earliest_cr_line_months_since'] > 115) & (X['earliest_cr_line_months_since'] <= 157), 1, 0)
        X_new['earliest_cr_line_months_since:167-249'] = np.where((X['earliest_cr_line_months_since'] > 157) & (X['earliest_cr_line_months_since'] <= 260), 1, 0)
        X_new['earliest_cr_line_months_since:249-331'] = np.where((X['earliest_cr_line_months_since'] > 260) & (X['earliest_cr_line_months_since'] <= 325), 1, 0)
        X_new['earliest_cr_line_months_since:331-434'] = np.where((X['earliest_cr_line_months_since'] > 325) & (X['earliest_cr_line_months_since'] <= 434), 1, 0)
        X_new['earliest_cr_line_months_since:>434'] = np.where((X['earliest_cr_line_months_since'] > 434), 1, 0)
        X_new['issue_d_months_since:<79'] = np.where((X['issue_d_months_since'] <= 59), 1, 0)
        X_new['issue_d_months_since:79-89'] = np.where((X['issue_d_months_since'] > 59) & (X['issue_d_months_since'] <= 62), 1, 0)
        X_new['issue_d_months_since:89-100'] = np.where((X['issue_d_months_since'] > 62) & (X['issue_d_months_since'] <= 65), 1, 0)
        X_new['issue_d_months_since:100-122'] = np.where((X['issue_d_months_since'] > 65) & (X['issue_d_months_since'] <= 67), 1, 0)
        X_new['issue_d_months_since:>122'] = np.where((X['issue_d_months_since'] > 67), 1, 0)
        X_new['last_credit_pull_d_months_since:missing'] = np.where(X['last_credit_pull_d_months_since'].isnull(), 1, 0)
        X_new['last_credit_pull_d_months_since:<56'] = np.where((X['last_credit_pull_d_months_since'] <= 56), 1, 0)
        X_new['last_credit_pull_d_months_since:56-61'] = np.where((X['last_credit_pull_d_months_since'] > 56) & (X['last_credit_pull_d_months_since'] <= 61), 1, 0)
        X_new['last_credit_pull_d_months_since:>75'] = np.where((X['last_credit_pull_d_months_since'] > 61), 1, 0)
        X_new.drop(columns = ref_categories, inplace = True)
        return X_new
# we could have also structured this class without the last drop statement and without creating categories out of the
# feature categories. But doing the way we have done here allows us to keep a proper track of the categories, if required