from flask import Flask, make_response, request, jsonify
from flask_mongoengine import MongoEngine
from constants import mongodb_password, datetime_format, mongodb_uri, mongodb_name
import datetime
import calendar 

app = Flask(__name__)

print("A")
DB_URI = "mongodb+srv://Desmond:Desmond63@cluster1.j2rmu.mongodb.net/APPOINTMENT?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI

db = MongoEngine()
db.init_app(app)

##### Patient Medical Data #####
class PatientMedicalData(db.Document):
    PatientId = db.StringField()
    Symptom = db.StringField()
    PreferredDate = db.DateTimeField()
    PreferredTime = db.StringField()

    def to_json(self):
        return {
            "PatientId": self.PatientId,
            "Symptom": self.Symptom,
            "PreferredDate": self.PreferredDate,
            "PreferredTime": self.PreferredTime
        }

@app.route('/api/patient_medical_data/populate', methods=['POST'])
def patient_populate():
    obj1 = PatientMedicalData(PatientId="1", Symptom="fever,running nose", PreferredDate=datetime.datetime(2021,3,27, 0 , 0), PreferredTime="10:00am")
    obj2 = PatientMedicalData(PatientId="2", Symptom="headache,vommit", PreferredDate=datetime.datetime(2021,4,5, 0 , 0), PreferredTime="03:00pm")
    obj3 = PatientMedicalData(PatientId="3", Symptom="amnesia,headache,", PreferredDate=datetime.datetime(2021,3,30, 0 , 0), PreferredTime="05:30pm")
    obj4 = PatientMedicalData(PatientId="4", Symptom="flu,headache,muscle pain", PreferredDate=datetime.datetime(2021,4,20, 0 , 0), PreferredTime="12:00pm")
    obj5 = PatientMedicalData(PatientId="5", Symptom="vommit,cough", PreferredDate=datetime.datetime(2021,4,11, 0 , 0), PreferredTime="09:30am")
    
    obj1.save()
    obj2.save()
    obj3.save()
    obj4.save()
    obj5.save()

    return make_response("Populated successfully",201)

@app.route('/api/patient_medical_datas', methods=['GET','POST'])
def api_patient_med_data():
    if request.method == "GET":
        datas = []
        for data in PatientMedicalData.objects:
            datas.append(data)

        return make_response(jsonify(datas), 200)

    elif request.method == "POST":
        content = request.json
        
        data = PatientMedicalData(PatientId=content['PatientId'], Symptom=content['Symptom'], PreferredDate=datetime.datetime.strptime(content['PreferredDate'], datetime_format), PreferredTime=content['PreferredTime'])
        data.save()

        return make_response("Inserted successfully",201)

@app.route('/api/patient_medical_datas/<patient_id>', methods=['GET','PUT','DELETE'])
def api_each_patient_med_data(patient_id):
    if request.method == "GET":
        obj = PatientMedicalData.objects(PatientId=patient_id).first()
        if obj:
            return make_response(jsonify(obj.to_json()), 200)
        else:
            return make_response("Data not found", 404)

    elif request.method == "PUT":
        content = request.json
        obj = PatientMedicalData.objects(PatientId=patient_id).first()
        obj.update(Symptom=content['Symptom'], PreferredDate=datetime.datetime.strptime(content['PreferredDate'], datetime_format), PreferredTime=content['PreferredTime'])

        return make_response("Updated successfully", 204)

    elif request.method == "DELETE":
        obj = PatientMedicalData.objects(PatientId=patient_id).first()
        obj.delete()

        return make_response("Deleted successfully", 204)

##### DoctorSpeciality #####
class DoctorSpeciality(db.Document):
    DoctorId = db.StringField()
    HandledSymptoms = db.StringField()
    AvailableDay = db.StringField()
    AvailableTime = db.StringField()
    Rating = db.IntField()
    ChargeRate = db.FloatField()

    def to_json(self):
        return {
            "DoctorId": self.DoctorId,
            "HandledSymptoms": self.HandledSymptoms,
            "AvailableDay": self.AvailableDay,
            "AvailableTime": self.AvailableTime,
            "Rating": self.Rating,
            "ChargeRate": self.ChargeRate
        }

@app.route('/api/doctor_speciality/populate', methods=['POST'])
def doctor_populate():
    obj1 = DoctorSpeciality(DoctorId="1", HandledSymptoms="fever,vommit", AvailableDay="Saturday,Sunday", AvailableTime="07:00pm",Rating=3,ChargeRate=40.5)
    obj2 = DoctorSpeciality(DoctorId="2", HandledSymptoms="headache,amnesia", AvailableDay="Sunday", AvailableTime="10:00am",Rating=1,ChargeRate=50)
    obj3 = DoctorSpeciality(DoctorId="3", HandledSymptoms="muscle pain,headache,", AvailableDay="Monday,Wednesday", AvailableTime="03:00pm",Rating=5,ChargeRate=60)
    obj4 = DoctorSpeciality(DoctorId="4", HandledSymptoms="flu,running nose,headache", AvailableDay="Saturday", AvailableTime="04:00pm",Rating=4,ChargeRate=25)
    obj5 = DoctorSpeciality(DoctorId="5", HandledSymptoms="fever,cough", AvailableDay="Friday,Saturday", AvailableTime="06:30pm",Rating=3,ChargeRate=30)
    
    obj1.save()
    obj2.save()
    obj3.save()
    obj4.save()
    obj5.save()

    return make_response("Populated successfully",201)

@app.route('/api/doctor_speciality_datas', methods=['GET','POST'])
def api_doctor_spec_data():
    if request.method == "GET":
        datas = []
        for data in DoctorSpeciality.objects:
            datas.append(data)
        print (type(datas))
        return make_response(jsonify(datas), 200)

    elif request.method == "POST":
        content = request.json
        
        data = DoctorSpeciality(DoctorId=content['DoctorId'], HandledSymptoms=content['HandledSymptoms'], AvailableDay=content['AvailableDay'], AvailableTime=content['AvailableTime'], Rating=content['Rating'], ChargeRate=content['ChargeRate'])
        data.save()

        return make_response("Inserted successfully",201)

@app.route('/api/doctor_speciality_datas/<doctor_id>', methods=['GET','PUT','DELETE'])
def api_each_doctor_spec_data(doctor_id):
    if request.method == "GET":
        obj = DoctorSpeciality.objects(DoctorId=doctor_id).first()
        if obj:
            return make_response(jsonify(obj.to_json()), 200)
        else:
            return make_response("Data not found", 404)

    elif request.method == "PUT":
        content = request.json
        obj = DoctorSpeciality.objects(DoctorId=doctor_id).first()
        obj.update(HandledSymptoms=content['HandledSymptoms'], AvailableDay=content['AvailableDay'], AvailableTime=content['AvailableTime'], Rating=content['Rating'], ChargeRate=content['ChargeRate'])

        return make_response("Updated successfully", 204)

    elif request.method == "DELETE":
        obj = DoctorSpeciality.objects(DoctorId=doctor_id).first()
        obj.delete()
        
        return make_response("Deleted successfully", 204)

##### DoctorRecommendation #####
@app.route('/api/getDoctorRanking', methods=['POST']) 
def getDoctorRanking():
    input_map = request.json
    patient_id= input_map.get("PatientId")
    #symptoms = []
    symptoms= input_map.get("Symptom")
    date= input_map.get("PreferredDate")
    time= input_map.get("PreferredTime")
    #datetime_object = datetime.strptime(available_time, '%m/%d/%Y')
    print ("A")
    #calculate the weekday for particular date
    def findDay(date): 
        week1 = datetime.datetime.strptime(date, '%m/%d/%Y').weekday() 
        return (calendar.day_name[week1])

    Actual_Date= findDay(date)
    Actual_time = datetime.datetime.strptime(time, '%I:%M%p').time()

    dummy_doctor_profiles = []
    for dummy_doctor_profiles1 in DoctorSpeciality.objects:
        dummy_doctor_profiles.append(dummy_doctor_profiles1)
   
    # loop doctor profiles and compare with patient symptoms to find the best doctor.
    # Can assign score for each doctor and rank according using "sorted" function 
    
    symptoms_list = set(symptoms.lower().split(","))
    #Actual_Date1 = list.append(Actual_Date)
    #Actual_Date1 = set(Actual_Date1.lower())
    #print(Actual_Date1)
    print("Patient Symptoms :", symptoms_list)
    print("Patient available Day :", Actual_Date, "\nPatient available time:", Actual_time)
    num_of_patient_symptoms= len(symptoms_list)
    new_doctor_list = []
    Doctors_time = []
    Doctors_date = []

    #Get all doctor profile from DB and doing recommendation 
    for profile in dummy_doctor_profiles:
        
        Doctor_date = profile["AvailableDay"]
        Doctor_time = profile["AvailableTime"]
        str1 = profile["HandledSymptoms"]
        handled_symptoms = set(str1.lower().split(","))
        matched_symptoms= handled_symptoms & symptoms_list

        if matched_symptoms:
            #symptoms matched and save doctor available date and time for reference if patient have different preference
            Doctors_date.append((str1 + "     " + Doctor_date + "   " +Doctor_time))
            Doctor_time = datetime.datetime.strptime(Doctor_time, '%I:%M%p').time()
            if Actual_Date in Doctor_date:
                if Actual_time == Doctor_time:
                    #Score calculation
                    num_of_matched_symptoms = len(matched_symptoms)
                    score = float(num_of_matched_symptoms / num_of_patient_symptoms)
                    print(score)
                    #higher weightage for matching of most symptoms, score drop as charge rate higher 
                    profile["Rating"] = ((profile["Rating"]/10 + score*10)/ (profile["ChargeRate"]/5))*10 
                    new_doctor_list.append(profile)
                    print ("Doctor Rating : ",profile["Rating"])
                   
    ranked_doctor_profiles = sorted(new_doctor_list, key=lambda k: k['Rating'], reverse=True) 
    #print(ranked_doctor_profiles)
    #print(Doctors_date)

    if not (ranked_doctor_profiles or Doctors_date):
        #no matching on symptoms
        return jsonify('no specialise doctor')
    elif not ranked_doctor_profiles:
        #symptoms matched but different timing
        return jsonify("no suitable time slot!", "Others available doctor time:", Doctors_date)
    else:
        #print (ranked_doctor_profiles['score'])
        filtered_profile  = [ obj for obj in ranked_doctor_profiles if obj['Rating'] > 0.0]
        return jsonify(filtered_profile)

###################

if __name__ == '__main__':
    app.run()
