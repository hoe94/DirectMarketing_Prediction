# -*- coding: utf-8 -*-

from flask import Flask,render_template,request
import pickle

from datetime import datetime
from sklearn.preprocessing import MinMaxScaler


app = Flask(__name__)



with open('model.plk','rb') as file:
    model = pickle.load(file)

@app.route('/',methods=['GET'])
def Home():
    return render_template('home.html')

@app.route('/predict',methods=['POST','GET'])
def predict():
    
    if request.method == "POST":
        name = request.form['Name']
        age_new = int(request.form['Age'])
        gender = request.form.getlist('Gender')
        dob = datetime.strptime(request.form['Date'],'%Y-%m-%d')
        #email = request.form['Email']
        
        #Select the Marital Status
        marital = request.form['Marital']
        if (marital == 'single'):
           marital_single = 1
           marital_married = 0
           marital_unknown = 0
        elif (marital == 'married'):
           marital_single = 0
           marital_married = 1
           marital_unknown = 0
        elif (marital == 'unknown'):
           marital_single = 0
           marital_married = 0
           marital_unknown = 1
        else:
           marital_single = 0
           marital_married = 0
           marital_unknown = 0        
        
        #Select the Education level of customer
        education = request.form['Education']
        if (education == 'basic.4y'):
            education_basic_4y = 1
            education_basic_9y = 0
            education_high_school = 0
            education_university_degree = 0 
            education_professional_course = 0
        elif (education == 'basic.9y'):
            education_basic_4y = 0
            education_basic_9y = 1
            education_high_school = 0
            education_university_degree = 0 
            education_professional_course = 0
        elif (education == 'high.school'):
            education_basic_4y = 0
            education_basic_9y = 0
            education_high_school = 1
            education_university_degree = 0 
            education_professional_course = 0
        elif (education == 'university_degree'):
            education_basic_4y = 0
            education_basic_9y = 0
            education_high_school = 0
            education_university_degree = 1
            education_professional_course = 0
        elif (education == 'professional.course'):
            education_basic_4y = 0
            education_basic_9y = 0
            education_high_school = 0
            education_university_degree = 0
            education_professional_course = 1
        
        #Select the Job worked with
        job = request.form['Job']
        if (job == 'admin'):
            job_admin = 1
            job_blue_collar = 0
            job_management = 0
            job_services = 0 
            job_technician = 0
        elif (job == 'blue-collar'):
            job_admin = 0
            job_blue_collar = 1
            job_management = 0
            job_services = 0 
            job_technician = 0
        elif (job == 'management'):
            job_admin = 0
            job_blue_collar = 0
            job_management = 1
            job_services = 0 
            job_technician = 0
        elif (job == 'services'):
            job_admin = 0
            job_blue_collar = 0
            job_management = 0
            job_services = 1
            job_technician = 0
        elif (job == 'technician'):
            job_admin = 0
            job_blue_collar = 0
            job_management = 0
            job_services = 0
            job_technician = 1
        else:
            job_admin = 0
            job_blue_collar = 0
            job_management = 0
            job_services = 0
            job_technician = 0
        
        #Get to know customer got the credit before
        default = request.form.getlist('Default')
        if (default == 'yes'):
            default_yes = 1
            default_unknown = 0
        elif (default == 'no'):
            default_yes = 0
            default_unknown = 0
        else: 
            default_yes = 0
            default_unknown = 1
        
        #Get to know customer got the housing loan before
        housing = request.form.getlist('Housing')
        if (housing == 'yes'):
            housing_yes = 1
            housing_unknown = 0
        elif (housing == 'no'):
            housing_yes = 0
            housing_unknown = 0
        else: 
            housing_yes = 0
            housing_unknown = 1
        
        #Get to know customer got the personal loan before
        loan = request.form.getlist('Loan')
        if (loan == 'yes'):
            loan_yes = 1
            loan_unknown = 0
        elif (loan == 'no'):
            loan_yes = 0
            loan_unknown = 0
        else: 
            loan_yes = 0
            loan_unknown = 1
        
        #How the way to contact the customer
        contact = request.form.getlist('Contact')
        if (contact == 'Telephone'):
            contact_telephone = 1
        else: 
            contact_telephone = 0
        
        #Convert the last call date into the featue
        contacts = datetime.strptime(request.form['Contacts'],'%Y-%m-%d')
        contacts_day = contacts.strftime("%A")
        contacts_month = contacts.strftime("%B")
        if (contacts_day == 'Monday'):
            day_of_week_mapping = 1
        elif (contacts_day == 'Tuesday'):
            day_of_week_mapping = 2
        elif (contacts_day == 'Wednestday'):
            day_of_week_mapping = 3
        elif (contacts_day == 'Thrusday'):
            day_of_week_mapping = 4
        elif (contacts_day == 'Friday'):
            day_of_week_mapping = 5
        else:
             day_of_week_mapping = 0
             
        newMonth = {'March':'1','April':'2','May':'3','June':'4','July':'5','August':'6',
                              'September':'7','October':'8','November':'9','December':'10'}  
        # NewMonth = {'March':1,'April':2,'May':3,'June':4,'July':5,'August':6,
        #             'September':7,'October':8,'November':9,'Dec':10}
          
        # def convert_month(input):
        #     for month,value in newMonth.items():
        #         input.replace(month,float(value))
        #         return input
            
        # map(convert_month,contacts_day)
        for items,value in newMonth.items():
            if contacts_month in items:
                newMonth = int(value)

        campaign = int(request.form['Campaign'])
        previous = int(request.form['Previous'])
        
        #Is this customer subscribed from last campaign
        poutcome = request.form.getlist('Poutcome')
        if (poutcome == 'success'):
            poutcome_success = 1
            poutcome_nonexistent = 0
        elif (poutcome == 'failure'): 
            poutcome_success = 0
            poutcome_nonexistent = 0
        else:
            poutcome_success = 0
            poutcome_nonexistent = 1

        emp_var_rate_min = -3.40
        emp_var_rate_max = 1.40
        cons_price_idx_min = 92.20
        cons_price_idx_max = 94.76
        cons_conf_idx_min = -50.80
        cons_conf_idx_max = -26.90
        euribor3m_min = 0.634
        euribor3m_max = 5.045
        nr_employed_min = 4963.60
        nr_employed_max = 5228.10
        
        

        sc = MinMaxScaler()
        emp_var_rate = ((int(request.form['emp_var_rate']) - emp_var_rate_min) / (emp_var_rate_max-emp_var_rate_min))
        #emp_var_rate = np.asarray(int(request.form['emp_var_rate']))
        #emp_var_rate = sc.fit_transform(emp_var_rate.reshape(-1,1))
        
        cons_price_idx = ((int(request.form['cons_price_idx']) - cons_price_idx_min) / (cons_price_idx_max-cons_price_idx_min))
        #cons_price_idx = np.asarray( float(request.form['cons_price_idx']))
        #cons_price_idx = sc.fit_transform(cons_price_idx.reshape(-1,1))
 
        cons_conf_idx = ((int(request.form['cons_conf_idx']) - cons_conf_idx_min) / (cons_conf_idx_max-cons_conf_idx_min))
        #cons_conf_idx = np.asarray(int(request.form['cons_conf_idx']))
        #cons_conf_idx = sc.fit_transform(cons_conf_idx.reshape(-1,1))       
        
        euribor3m = ((int(request.form['euribor3m']) - euribor3m_min) / (euribor3m_max-euribor3m_min))
        #euribor3m = np.asarray(int(request.form['euribor3m']))
        #euribor3m = sc.fit_transform(euribor3m.reshape(-1,1))     
        
        nr_employed = ((int(request.form['nr_employed']) - nr_employed_min) / (nr_employed_max-nr_employed_min))
        #nr_employed = np.asarray(int(request.form['nr_employed']))
        #nr_employed = sc.fit_transform(nr_employed.reshape(-1,1))    



        #cons_price_idx = sc.fit_transform(float(request.form['cons_price_idx']))
        #cons_conf_idx = sc.fit_transform(int(request.form['cons_conf_idx']))
        #euribor3m = sc.fit_transform(int(request.form['euribor3m']))
        #nr_employed = sc.fit_transform(int(request.form['nr_employed']))

           
        # prediction = model.predict([[age_new,marital_single,marital_married,marital_unknown
        #                             ,education_basic_4y,education_basic_9y,education_high_school,education_university_degree,education_professional_course
        #                             ,job_admin,job_blue_collar,job_management,job_services,job_technician
        #                             ,default_yes,default_unknown,housing_yes,housing_unknown,loan_yes,loan_unknown
        #                             ,contact_telephone,day_of_week_mapping,newMonth,campaign,previous,poutcome_success,poutcome_nonexistent
        #                             ,emp_var_rate,cons_price_idx,cons_conf_idx,euribor3m,nr_employed]])
        
        prediction = model.predict([[campaign,previous,emp_var_rate,cons_price_idx,cons_conf_idx,euribor3m,nr_employed,age_new,
                                     education_basic_4y,education_basic_9y,education_high_school,education_university_degree,education_professional_course,
                                     job_admin,job_blue_collar,job_management,job_services,job_technician,
                                     marital_single,marital_married,marital_unknown,
                                     default_yes,default_unknown,housing_yes,housing_unknown,loan_yes,loan_unknown,
                                     poutcome_success,poutcome_nonexistent,contact_telephone,day_of_week_mapping,newMonth]])
        emp_var_rate = float(emp_var_rate)
        cons_price_idx = float(cons_price_idx)
        cons_conf_idx = float(cons_conf_idx)
        euribor3m = float(euribor3m)
        nr_employed = float(nr_employed)

        if prediction == 0:
            prediction_texts = "This customer is not gonna subscribed the program"
            return render_template('result.html',prediction_texts = prediction_texts)
        elif prediction == 1:
            prediction_texts = "Please call this customer for the program"
            return render_template('result.html',prediction_texts = prediction_texts)   

    elif request.method == "GET":
        return render_template('home.html')
    else:
         return render_template('home.html')
     
if __name__ == "__main__":
  app.run(debug=True)
  

