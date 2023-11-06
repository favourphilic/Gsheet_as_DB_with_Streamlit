import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd


st.header(" :chart_with_upwards_trend: TempHumidity-APP")
st.markdown('_Kindly input the data displayed on the clock in the form below_ :point_down:')

# Create a connection object, which will fetch the required information from our secrets.toml
conn = st.connection("gsheets", type=GSheetsConnection)
# Fetch existing  data from any of the sheets using the sheet name and 
# specifying the number of columns 
datadf= conn.read(worksheet="temp", usecols=[0,1,2,3,4,5] , ttl=5)
datadf = datadf.dropna(how="all")
pharmdf= conn.read(worksheet="pharmacist", usecols=[0,1,2,3,4,5])
pharmdf = pharmdf.dropna(how="all")
#------------------------------------------------------------------------------------------------------------
#unique_pdt = list(productdf.ProductName.unique())  #unique_emp= list(empdf.EmpName.unique())
unique_pharms = list(pharmdf.PharmacistName.unique()) #to get the unique name of the pharmacists
#st.write(unique_pharms) 
#---------------------------------------------------------------------------------------------
with st.form(key="TheForm"):
    date = st.date_input(label="Date")
    time= st.time_input(label="Time")
    TemperatureIn = st.slider("TempIN", min_value=1.0,max_value=50.0,step=1e-1, format="%.1f")
    TemperatureOut = st.slider("TempOUT", min_value=1.0,max_value=50.0,step=1e-1, format="%.1f")
    RelativeHumidity = st.slider("RelativeHumidity", min_value=0,max_value=100)
    PharmacistName= st.selectbox("PharmacistName", unique_pharms, index=None)

    submit_button=st.form_submit_button(label="Submit Details")

    if submit_button:
        if  TemperatureIn <= 15 or TemperatureOut <=15 :
                st.warning("Temp Field must be greater than 15.")
                st.stop()
        elif RelativeHumidity <= 40 :
             st.warning("Humidity not optimal, inform focal-Pharmacist")
             st.stop()
        # elif TemperatureIn <= 15 or TemperatureOut <=15 and RelativeHumidity <= 40:
        #      st.warning("Temp Field must be greater than 15 ")
        #      st.warning("Humidity not optimal, inform focal-Pharmacist")
                #st.stop()
        else:
             new_df = pd.DataFrame(
                    [
                        {
                            "Date": date.strftime("%d-%B-%Y"),
                            "Time":time,
                            "TemperatureIn": TemperatureIn,
                            "TemperatureOut": TemperatureOut,
                            "Humidity": RelativeHumidity,
                            "PharmacistName": PharmacistName
                           
                        }
                    ]
                )
             updated_df = pd.concat([datadf, new_df], ignore_index=True)
             conn.update(worksheet="temp", data=updated_df)
             st.success("Daily Chart successfully submitted!")






st.subheader("Daily_Chart")
st.dataframe(datadf.tail(2))
st.subheader("Pharmacist_Table")
st.dataframe(pharmdf)
