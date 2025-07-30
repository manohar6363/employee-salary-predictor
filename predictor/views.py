from django.shortcuts import render
import cloudpickle
import os
import pandas as pd
import numpy as np

# Load model once
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'employee_model.pkl')
with open(MODEL_PATH, 'rb') as f:
    model = cloudpickle.load(f)

def home(request):
    return render(request, 'home.html')

def predict_salary(request):
    if request.method == 'POST':
        try:
            data = {
                'Age': float(request.POST.get('age')),
                'Gender': request.POST.get('gender').lower().strip(),
                'Department': request.POST.get('department').lower().strip(),
                'Job_Title': request.POST.get('job_title').lower().strip(),
                'Experience_Years': request.POST.get('experience_years').lower().strip(),
                'Education_Level': request.POST.get('education_level').lower().strip(),
                'Location': request.POST.get('location').lower().strip(),
            }

            input_df = pd.DataFrame([data])  # ← this is the fix
            prediction = model.predict(input_df)[0]
            prediction = round(prediction, 2)

            return render(request, 'home.html', {'prediction': prediction})

        except Exception as e:
            return render(request, 'home.html', {'error': str(e)})

    return render(request, 'home.html')