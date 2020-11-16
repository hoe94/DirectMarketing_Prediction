# -*- coding: utf-8 -*-
import pandas as pd
#import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
#from sklearn.ensemble import RandomForestClassifier
#from sklearn.model_selection import RandomizedSearchCV
#from sklearn.model_selection import GridSearchCV
#from sklearn.metrics import accuracy_score,confusion_matrix,classification_report


#from imblearn.under_sampling import NearMiss
#from imblearn.over_sampling import RandomOverSampler
from imblearn.combine import SMOTETomek
#from collections import Counter

from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)
import pickle

dataset = pd.read_csv('dataset_v2.csv',index_col = 0)
X = dataset[['campaign','previous','emp_var_rate','cons_price_idx','cons_conf_idx','euribor3m','nr_employed','age_new',
             'education_university_degree',	'education_high_school','education_basic_9y','education_professional_course','education_basic_4y',
             'job_admin','job_blue_collar','job_management','job_services','job_technician',
             'marital_single','marital_married','marital_unknown',
             'default_unknown','default_yes',
             'housing_yes','housing_unknown','loan_yes','loan_unknown','poutcome_nonexistent','poutcome_success','contact_telephone',
             'day_of_week_mapping','newMonth']]
#X = dataset.drop('y',axis = 1)
y = dataset['y']
x_train,x_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=0)


smote = SMOTETomek(sampling_strategy=0.8)
x_train_smote, y_train_smote = smote.fit_sample(x_train,y_train)
x_test_smote, y_test_smote = smote.fit_sample(x_test,y_test)

# random = RandomForestClassifier(criterion='entropy', 
#                                  max_depth=20, 
#                                  max_features='auto', 
#                                  min_samples_leaf=2, 
#                                  min_samples_split=2, n_estimators=300)

log = LogisticRegression(solver = 'lbfgs', penalty ='l2', max_iter=200, C=10)
								
log.fit(x_train_smote,y_train_smote)
#y_pred = log.predict(x_test_smote)
#print(accuracy_score(y_test_smote,y_pred))

with open('model.plk','wb')as file:
    pickle.dump(log,file)
    