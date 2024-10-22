import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, RepeatedStratifiedKFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix, precision_recall_curve, auc
from sklearn.feature_selection import f_classif
from sklearn.pipeline import Pipeline
from scipy.stats import chi2_contingency
# import  pickle
from custom_packages.woe_binning import WoE_Binning
from fastapi import FastAPI,UploadFile,File,HTTPException
from custom_services.preprocessing import PreProcess_test_data
from custom_services.validation import validate_csv_columns
from custom_services.constants import constants as const
import python_multipart
import os
import json
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

# class MyCustomUnpickler(pickle.Unpickler):
#     def find_class(self, module, name):
#         if module == "__main__":  # When it was pickled, it could have been __main__
#             module = "custom_packages.woe_binning"  # Replace with actual module
#         return super().find_class(module, name)

def make_predictions(x_test,scorecard_scores):
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current file
    file_path = os.path.join(BASE_DIR, 'model_pipeline.pkl') 
    # pipeline = joblib.load(file_path)
    # with open(file_path, 'rb') as f:
    #     unpickler = MyCustomUnpickler(f)
    #     pipeline = unpickler.load()
    Preprocess_obj  = PreProcess_test_data(x_test)
    preprocessed_x_test = Preprocess_obj.preprocess()
    Woe_transformer = WoE_Binning(preprocessed_x_test)
    woe_transformed_x_test = Woe_transformer.transform(preprocessed_x_test)
    woe_transformed_x_test.insert(0,'intercept',1)
    scorecard_scores = np.array(scorecard_scores)
    final_scores = woe_transformed_x_test.dot(scorecard_scores)
    return final_scores




app = FastAPI(title="Credit Risk Model API", version="1.0")

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/",response_class=HTMLResponse)
async def read_root():
    with open("frontend/index.html") as f:
        return HTMLResponse(content=f.read())
    
@app.get("/predictions", response_class=HTMLResponse)
async def read_predictions():
    with open("frontend/predictions.html") as f:
        return HTMLResponse(content=f.read())
    
@app.get("/about", response_class=HTMLResponse)
async def read_about():
    with open("frontend/about.html") as f:
        return HTMLResponse(content=f.read())

#file: UploadFile = File(...)
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        if file.content_type != 'text/csv' or not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Invalid file type. Only CSV files are allowed.")

        #Read the uploaded file directly into a pandas DataFrame
        try:
            content = await file.read()
            data = pd.read_csv(pd.io.common.BytesIO(content))
        except:
            raise HTTPException(status_code=400, detail="error reading file")
        # BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current file
        # file_path = os.path.join(BASE_DIR, 'test_df_1.csv') 
        # data  = pd.read_csv(file_path)
        # Validate CSV columns, Update with actual column names
        try:
            if not validate_csv_columns(data):
                raise HTTPException(status_code=400, detail="CSV file is missing required columns.")
        except:
            raise HTTPException(status_code=400, detail="CSV file is invalid.")
        # Make predictions using the pre-trained pipeline
        scores =make_predictions(data,const.scorecard_scores)
        scores_with_pred = []
        qualifying_score = 570
        i = 1
        for score in scores:
            pred = {}
            pred["Score"] = score
            pred["Name"] = f'User {i}'
            if score>=qualifying_score:
                pred["Qualified_for_loan"] = True
            else:
                pred["Qualified_for_loan"] = False
            scores_with_pred.append(pred)
            i += 1
        
        return {'status_code': 200, "predictions": scores_with_pred}
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))




# x_test = pd.read_csv('test_data_10.csv')
# x_test_transformed  = pipeline['woe'].fit_transform(x_test)

# summary_table  = pd.DataFrame(columns = ['Feature'],data = x_test_transformed.columns)
# summary_table['Coefficient'] = np.transpose(pipeline['model'].coef_)
# summary_table.index  = summary_table.index+1
# summary_table.loc[0] = ['Intercept',pipeline['model'].intercept_[0]]
# summary_table = summary_table.sort_index()


# summary_table['original_col'] = summary_table['Feature'].apply(lambda x: x.split(':')[0]) 

# min_score = 300
# max_score = 850

# min_sum_coef = summary_table.groupby('original_col')['Coefficient'].min().sum()
# max_sum_coef = summary_table.groupby('original_col')['Coefficient'].max().sum()

# summary_table['Score-pre']  = (summary_table['Coefficient']*(max_score-min_score))/(max_sum_coef-min_sum_coef) 
# summary_table.loc[0, 'Score-pre'] = ((summary_table.loc[0,'Coefficient'] - min_sum_coef) / (max_sum_coef - min_sum_coef)) * (max_score - min_score) + min_score


# summary_table['socre-premi'] = summary_table['Score-pre'].apply(lambda x: round(x))


# summary_table.loc[0,'socre-premi'] = 602
# minpos_sum_coef = summary_table.groupby('original_col')['socre-premi'].min().sum()
# maxpos_sum_coef = summary_table.groupby('original_col')['socre-premi'].max().sum()
# print(minpos_sum_coef)
# print(maxpos_sum_coef)

# x_test_transformed.insert(0,'intercept',1)

# scorecard_scores = np.array(summary_table['socre-premi'])
# # check the shapes of test set and scorecard before doing matrix dot multiplication
# print(x_test_transformed.shape)
# print(scorecard_scores.shape)

# y_scores =x_test_transformed.dot(scorecard_scores)
# print(y_scores)

# plt.figure(figsize = (20, 12))
# plt.hist(y_scores, bins=200, color='green', edgecolor='black')

# # Add labels and title
# plt.xlabel('Value')
# plt.ylabel('Frequency')
# plt.title('Histogram of Data')

# # Display the plot
# plt.show()

# def predict():
#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current file
#     file_path = os.path.join(BASE_DIR, 'test_df_1.csv') 
#     data  = pd.read_csv(file_path)
#     # Validate CSV columns, Update with actual column names
#     if not validate_csv_columns(data):
#         print("CSV file is missing required columns.")

#     # Make predictions using the pre-trained pipeline
#     predictions =make_predictions(data,const.scorecard_scores)
        
#     return {"predictions": predictions.tolist()}

# print(predict())