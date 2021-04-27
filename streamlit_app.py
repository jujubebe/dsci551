import streamlit as st
import numpy as np
import pandas as pd
import pymongo
import plotly.express as px
import datetime
import altair as alt



myclient = pymongo.MongoClient("mongodb+srv://julia:dsci551AAA@cluster0.wu443.mongodb.net/myDB?retryWrites=true&w=majority")
mydb = myclient["myDB"]
mycol1 = mydb["covid"]
mycol2 = mydb["hospital_sum"]
mycol3 = mydb["hospital"]


query = mycol1.find({},{ "_id": 0, "date": 1, "positive": 1, "totalTestResults": 1, "death":1, "positiveIncrease":1, "deathIncrease":1 })
covid = pd.DataFrame(list(query))
covid['death'].fillna(0, inplace = True)


hospital = pd.DataFrame(list(mycol2.find({},{"_id": 0, "date" :1,"hospital_cfm_patients":1, "hospital_spc_patients": 1, "hospital_patients":1,
"icu_cfm_patients":1, "icu_spc_patients":1, "all_bed":1})))


query1 = mycol3.find({},{"_id":0})

hospital_county = pd.DataFrame(list(query1))
hospital_county.fillna(0, inplace = True)
hospital_county.rename(columns={'todays_date': 'date'}, inplace=True)


selected_table = st.selectbox('Which table do you want to explore?',
 ["All (Comparison of COVID19 and Hospital)",'COVID-19 Data', 'Hospital Data','County Hospital Data'])


if selected_table == 'All (Comparison of COVID19 and Hospital)':
	st.subheader('COVID-19 Data')
	st.write(covid)
	st.subheader('Hospital Data')
	st.write(hospital)

	min_date, max_date = min(covid['date']), max(hospital['date'])
	min_time, max_time = datetime.datetime.strptime(min_date, '%Y-%m-%d'), datetime.datetime.strptime(max_date, '%Y-%m-%d')
	date_range = st.sidebar.slider('Select date range:', value = (min_time, max_time))

	covid_range = st.sidebar.selectbox("Which variable you want to explore form COVID-19 Data?",
			("positive","totalTestResults", "death", "positiveIncrease", "deathIncrease"))
	hospital_range = st.sidebar.selectbox("Which variable you want to explore form Hospital Data?" ,
		("hospital_cfm_patients", "hospital_spc_patients","hospital_patients","icu_cfm_patients","icu_spc_patients","all_bed"))

	if st.sidebar.button('Search'):
		st.write('Intergration Result:')
		search1 = mycol1.find({"date": {"$gte": date_range[0].isoformat(), "$lte": date_range[1].isoformat() }},
			{ "_id": 0, "date": 1, "positive": 1, "totalTestResults": 1,
			"death":1, "positiveIncrease":1, "deathIncrease":1 })
		search2 = mycol2.find({"date": {"$gte": date_range[0].isoformat(), "$lte": date_range[1].isoformat() }},
			{"_id": 0, "date" :1,"hospital_cfm_patients":1, "hospital_spc_patients": 1, "hospital_patients":1,
			"icu_cfm_patients":1, "icu_spc_patients":1, "all_bed":1})
		dd1 = pd.DataFrame(list(search1))
		dd2 = pd.DataFrame(list(search2))
		result = pd.merge(dd1,dd2, how = 'outer', on = 'date')
		result

		st.header("{} VS. {}".format(covid_range, hospital_range))
		chart = alt.Chart(result).mark_line().encode(
    		x=alt.X(covid_range+":Q"),
    		y=alt.Y(hospital_range+":Q")
		).properties(
    		width=600,
    		height=500
		)
		chart


		

elif selected_table == 'COVID-19 Data':
	st.header('COVID-19 Data')
	st.write(covid)
	
	#select time range
	min_date, max_date = min(covid['date']), max(covid['date'])
	min_time, max_time = datetime.datetime.strptime(min_date, '%Y-%m-%d'), datetime.datetime.strptime(max_date, '%Y-%m-%d')
	date_range = st.sidebar.slider('Select date range:', value = (min_time, max_time))
	feature_range = st.sidebar.selectbox("Which feature do you want to explore?" ,
		("positive","totalTestResults", "death", "positiveIncrease", "deathIncrease"))


	if st.sidebar.button('Search'):
		st.write('Query Result:')
		search = mycol1.find({"date": {"$gte": date_range[0].isoformat(), "$lte": date_range[1].isoformat() }},
			{ "_id": 0, "date": 1, "positive": 1, "totalTestResults": 1,
			"death":1, "positiveIncrease":1, "deathIncrease":1 })
		output = pd.DataFrame(list(search))
		output

		chart = alt.Chart(output).mark_line().encode(
			x='date',
    		y=alt.Y(feature_range+':Q')
		)
		chart


		

elif selected_table == 'Hospital Data':
	st.header('Hospital Data')
	st.write(hospital)

	min_date, max_date = min(hospital['date']), max(hospital['date'])
	min_time, max_time = datetime.datetime.strptime(min_date, '%Y-%m-%d'), datetime.datetime.strptime(max_date, '%Y-%m-%d')
	date_range = st.sidebar.slider('Select date range:', value = (min_time, max_time))
	feature_range = st.sidebar.selectbox("Which feature do you want to explore?" ,
		("hospital_cfm_patients", "hospital_spc_patients","hospital_patients","icu_cfm_patients","icu_spc_patients","all_bed"))


	if st.sidebar.button('Search'):
		st.write('Query Result:')
		search = mycol2.find({"date": {"$gte": date_range[0].isoformat(), "$lte": date_range[1].isoformat() }},
			{"_id": 0, "date" :1,"hospital_cfm_patients":1, "hospital_spc_patients": 1, "hospital_patients":1,
			"icu_cfm_patients":1, "icu_spc_patients":1, "all_bed":1})
		output = pd.DataFrame(list(search))
		output

		chart = alt.Chart(output).mark_line().encode(
    		x='date',
    		y=alt.Y(feature_range+':Q')
		)
		chart

elif selected_table == 'County Hospital Data':
	st.header('County Hospital Data')
	st.write(hospital_county)

	county_range = st.sidebar.multiselect("Which county do you want to explore?" ,
		(hospital_county['county'].unique()))


	min_date, max_date = min(hospital_county['date']), max(hospital_county['date'])
	min_time, max_time = datetime.datetime.strptime(min_date, '%Y-%m-%d'), datetime.datetime.strptime(max_date, '%Y-%m-%d')
	date_range = st.sidebar.slider('Select date range:', value = (min_time, max_time))
	feasture_range = st.sidebar.selectbox("Which feasture do you want to compare amonge the counties?" ,
		("hospitalized_covid_confirmed_patients", "hospitalized_suspected_covid_patients","hospitalized_covid_patients",
			"all_hospital_beds","icu_covid_confirmed_patients","icu_suspected_covid_patients","icu_available_beds"))


	if st.sidebar.button('Search'):
		st.write('Query Result:')
		search = mycol3.find({"$and":[{"todays_date": {"$gte": date_range[0].isoformat(), 
                                             "$lte": date_range[1].isoformat() }},
                           { "county": { "$in": county_range } }
                           ]},{"_id":0})
		output = pd.DataFrame(list(search))		

		st.header("Comparison of {}".format(feasture_range))

		chart = alt.Chart(output).mark_line().encode(
			x='todays_date',
			y=feasture_range+":Q",
			color='county',
			strokeDash='county',)
		chart




#add_selectbox = st.sidebar.selectbox(
#	'Variable',
#	('positive', 'totalTestResults', 'totalTestResults','death','positiveIncrease','deathIncrease')
#)

#values = st.sidebar.slider("Number of Increased", float(data.positiveIncrease.min()), 5000., (500.,1000.))
#f = px.histogram(df.query(f"positiveIncrease.between{values}", x="Cases", nbins=15, title="Range of increased")
# f.update_xaxes(title="positiveIncrease")
#f.update_yaxes(title="No. of listings")
#st.plotly_chart(f)
