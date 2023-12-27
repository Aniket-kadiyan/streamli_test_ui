
import colorsys
import streamlit as st
from influxdb import InfluxDBClient
import pandas as pd
import base64
from pathlib import Path


influxdb_client = None
influxdb_host = "172.104.176.90"
influxdb_port = 8086
influxdb_database = "mtConnectData"
influxdb_username = "root"
influxdb_password = "root"


influxdb_client = InfluxDBClient(
    host=influxdb_host,
    port=influxdb_port,
    username=influxdb_username,
    password=influxdb_password,
    database=influxdb_database)


# machine ip and value configurations
requiredvals = ["Program", "RunStatus", "M30Counter1"]
machines = [{"machine": "vmc-1", "url": "http://172.16.0.100:8082/current"},
            {"machine": "vmc-2", "url": "http://172.16.0.101:8082/current"},
            {"machine": "vmc-3", "url": "http://172.16.0.102:8082/current"},
            {"machine": "vmc-4", "url": "http://172.16.0.103:8082/current"},
            {"machine": "vmc-5", "url": "http://172.16.0.104:8082/current"},
            {"machine": "vmc-6", "url": "http://172.16.0.105:8082/current"}]

sleepTime = 10
def writetoinflux(jsonobject): influxdb_client.write_points(jsonobject)


influxlockfile = "F:\jobrelatedworks\MTconnect\influx_lock.txt"


def getinfluxLock():
    filename = influxlockfile
    readlock = 2
    while readlock == 2:
        with open(filename, 'r') as f:
            data = f.read()
            print(data)
            if data != "" or data != '':
                readlock = int(data)

    with open(filename, 'w') as f:
        f.write("1")


def releaseinfluxlock():
    filename = influxlockfile
    with open(filename, 'w') as f:
        f.write("0")


def getProgramData():
    getinfluxLock()
    query = "select * from ALP_ProgramData;"
    result = influxdb_client.query(query)
    points = influxdb_client.query(
        query, chunked=True, chunk_size=10000).get_points()
    dfs = pd.DataFrame(points)
    releaseinfluxlock()
    return dfs


def getLoginData():
    getinfluxLock()
    query = "select * from ALP_Toolroom_UI_logins;"
    result = influxdb_client.query(query)
    points = influxdb_client.query(
        query, chunked=True, chunk_size=10000).get_points()
    dfs = pd.DataFrame(points)
    releaseinfluxlock()
    return dfs


def login_success(username: str) -> None:
    st.session_state["authenticated"] = True
    st.session_state["username"] = username


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def change_label_color(label,  font_color='black'):
    html = f"""
    <script>
        var elems = window.parent.document.querySelectorAll('p');
        var elem = Array.from(elems).find(x => x.innerText == '{label}');
        elem.style.color = '{font_color}';
    </script>
    """
    st.components.v1.html(html)


def img_to_html(img_path):
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
        img_to_bytes(img_path)
    )
    return img_html


def set_color(key: str, color: str):
    st.session_state[key] = color
    print(key+" == "+str(st.session_state[key]))
    # sync_rgb_to_hls(key)


machineselectionlist = ("VMC-1", "VMC-2", "VMC-3", "VMC-4", "VMC-5", "VMC-6")
machineselectionlistmapping = {"VMC-1": "vmc-1", "VMC-2": "vmc-2",
                               "VMC-3": "vmc-3", "VMC-4": "vmc-4", "VMC-5": "vmc-5", "VMC-6": "vmc-6"}
machinenamemapping = {"vmc-1": "Machine1", "vmc-2": "Machine",
                      "vmc-3": "VF-2-I", "vmc-4": "Machine4", "vmc-5": "VF-2-I", "vmc-6": "VF-7/40"}
#
# UI Body Start
#
st.set_page_config(layout='wide')
st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)
titleplaceholder = st.empty()
placeholder = st.empty()
# hide_streamlit_style = """
# <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# </style>

# """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# st.markdown('''
# <style>
# .stApp [data-testid="stToolbar"]{
#     display:none;
# }
# </style>
# ''', unsafe_allow_html=True)

def update_theme():
    keys = ['primaryColor', 'backgroundColor',
            'secondaryBackgroundColor', 'textColor']
    has_changed = False
    for key in keys:
        if st._config.get_option(f'theme.{key}') != st.session_state[key]:
            st._config.set_option(f'theme.{key}', st.session_state[key])
            has_changed = True
    if has_changed:
        st.experimental_rerun()


def set_login_theme():
    print("Login Theme: ")
    primaryColor = "#ff4b4b"
    backgroundColor = "#ffffff"
    secondaryBackgroundColor = "#f0f2f6"
    textColor = "#31333F"
    set_color('primaryColor', primaryColor)
    set_color('backgroundColor', backgroundColor)
    set_color('secondaryBackgroundColor', secondaryBackgroundColor)
    set_color('textColor', textColor)
    update_theme()


def set_home_theme():
    print("home theme:")
    primaryColor = "#ff4b4b"
    backgroundColor = "#272d43"
    secondaryBackgroundColor = "None"
    textColor = "#FFFFFF"
    set_color('primaryColor', primaryColor)

    set_color('backgroundColor', backgroundColor)
    set_color('secondaryBackgroundColor', secondaryBackgroundColor)
    set_color('textColor', textColor)
    update_theme()
# markdown to set page boundaries
# st.markdown("""
#         <style>
#                .block-container {
#                     padding-top: 4rem;
#                     padding-bottom: 0rem;
#                     padding-left: 2rem;
#                     padding-right: 2rem;
#                 }
#         </style>
#         """, unsafe_allow_html=True)


def show_titlebar(user: str):
    titlebar = """
    <div style="width: 50%; height: 80px; float: left; background: #272d43; color : white; display: table; vertical-align: middle;border-bottom: 4px solid orange">
        <div style="display: table-cell; vertical-align: middle;">
            <div>
                <h2>ALPO</h2>
            </div>
        </div>
    </div>
    <div style="width: 50%;padding-right:40px; float:right; height: 80px; background: #272d43;color : white; text-align: end; border-bottom: 4px solid orange">
        <br>Hi, """+user + """
    </div>
    """
    
    # st.markdown(titlebar, unsafe_allow_html=True)
    st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style=" padding-top :5ex;border-bottom: 4px solid orange; background: black">
<div style="width: 50%; height: 80px; float: left; background: black; color : white; display: table; vertical-align: middle;">
        <div style="display: table-cell; vertical-align: middle;">
            <div>
                <h2>ALPO</h2>
            </div>
        </div>
    </div>
    <div style="width: 50%;padding-right:40px; float:right; height: 80px; background: black;color : white; text-align: end;">
        <br>Hi, """+user + """
    </div>
</nav>
""", unsafe_allow_html=True)

# with titleplaceholder:
# show_titlebar("")


def userLogin():

    global placeholder

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = None
    if st.session_state["authenticated"] == True:
        login_success(st.session_state["username"])
        placeholder = st.success("Login successful")
        placeholder.empty()
        # with placeholder:
        mainDisplay()
    else:
        set_login_theme()
        with placeholder.form("login"):
            css = """
            <style>
    [data-testid="stForm"] {
        background: white;
    }
</style>
"""
            st.write(css, unsafe_allow_html=True)
            st.markdown("""
        <style>
               .block-container {
                    padding-top: 5rem;
                    padding-bottom: 10rem;
                    padding-left: 25rem;
                    padding-right: 25rem;
                }
        </style>
        """, unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: black;'>" +
                        img_to_html('log-in-icon.png')+"</p>", unsafe_allow_html=True)
            st.markdown(
                "<p style='text-align: center;color: black;'>Use a local account to log in</p>", unsafe_allow_html=True)
            st.divider()
            # label=":red[Username]"
            username = st.text_input(":gray[Username]")
            password = st.text_input(":gray[Password]", type="password")
            submit = st.form_submit_button("Login")
        if submit:
            if validate(username, password):
                placeholder.empty()
                login_success(username)
                placeholder = st.success("Login successful")
                # del (placeholder)
                placeholder.empty()
                # with placeholder:
                mainDisplay()
            else:
                st.error("Login failed")
        else:
            pass


def validate(username: str, password: str):
    login_data = getLoginData()
    # st.write(login_data)
    if (username == "" or password == ""):
        return False
    if login_data.size > 0:
        ind = login_data.loc[(login_data["username"] == username) & (
            login_data["password"] == password)]
        if ind.size > 0:
            return True
    return False


machine_selection = ""


def mainDisplay():
    global machine_selection
    set_home_theme()
    
    st.markdown("""
        <style>
               .block-container {
                    padding-top: 5rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)
    show_titlebar(st.session_state["username"])
    # tab styling markdown
    st.markdown("""
<style>

	.stTabs [data-baseweb="tab-list"] {
		gap: 8px;
  padding-top:5ex;
    }

	.stTabs [data-baseweb="tab"] {
		height: 40px;
        white-space: pre-wrap;
		background-color: #F0F2F6;
		border-radius: 4px 4px 0px 0px;
		gap: 40px;
		padding-top: 10px;
		padding-bottom: 10px;
		padding-left: 10px;
		padding-right: 10px;
        color: black;
        font-size : 80px;
    }

	.stTabs [aria-selected="true"] {
  		background-color: #047dd4;
    height: 40px;
    border-bottom: 3px solid red;
    color:white;
    
        font-size : 80px;
	}

</style>""", unsafe_allow_html=True)
    programtab, downtimetab = st.tabs(["Program Details", "Downtime Details"])
    with programtab:
        # st.title("VMC Machine Program Details")
        st.markdown(
            "<h1 style='text-align: center; color: white;'>VMC Machine Program Details</h1>", unsafe_allow_html=True)
    # st.subheader("Logged in: " + st.session_state["username"])
        st.divider()
        machine_selection = st.selectbox(
            label="Select Machine *", options=machineselectionlist, index=None, placeholder="Choose a machine...")

        if machine_selection != None:
            statusDisplay()


def statusDisplay():
    global machine_selection
    dfs = getProgramData()
    if dfs.size > 0:
        dfs = dfs[dfs["name"] ==
                  machineselectionlistmapping.get(machine_selection)]
    if dfs.size > 0:
        dfs[["Priority"]] = dfs[["Priority"]].astype(str).astype(int)
        dfs = dfs.sort_values(by="Priority", ascending=False).reset_index()
        dfs = dfs[dfs["Priority"] >= 0]
        dfs = dfs[["name", "MachineName", "MainProgramName",
                   "NoOfSubPrograms", "CompletedSubPrograms"]]
        st.subheader("Current Program :")
        # st.write(dfs)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("<h5 style='text-align: center; color: white;'>" +
                        " Machine: "+"<h5>", unsafe_allow_html=True)
            st.markdown("<h4 style='text-align: center; color: white;'>" +
                        dfs.iloc[0]["MachineName"]+" ("+dfs.iloc[0]["name"]+")"+"<h4>", unsafe_allow_html=True)
        with col2:
            st.markdown("<h5 style='text-align: center; color: white;'>" +
                        " Program: "+"<h5>", unsafe_allow_html=True)
            st.markdown("<h4 style='text-align: center; color: white;'>" +
                        dfs.iloc[0]["MainProgramName"]+"<h4>", unsafe_allow_html=True)

        with col3:
            st.markdown("<h5 style='text-align: center; color: white;'>" +
                        "Total No. of Sub-Programs"+" : "+"<h5>", unsafe_allow_html=True)
            st.markdown("<h4 style='text-align: center; color: white;'>" +
                        dfs.iloc[0]["NoOfSubPrograms"]+"<h4>", unsafe_allow_html=True)
        with col4:
            st.markdown("<h5 style='text-align: center; color: white;'>" +
                        "No. of Sub-Programs completed"+" : "+"<h5>", unsafe_allow_html=True)
            st.markdown("<h4 style='text-align: center; color: white;'>" +
                        dfs.iloc[0]["CompletedSubPrograms"]+"<h4>", unsafe_allow_html=True)

        addtab, resumetab = st.tabs(
            ["Add new Program to Machine", "Resume Old Program on Machine"])
        with addtab:
            AddnewProgram_wo()
            with resumetab:
                resumeProgram()
    else:
        st.write("No Programs Running")
        addtab, resumetab = st.tabs(
            ["Add new Program to Machine", "Resume Old Program on Machine"])
        with addtab:
            AddnewProgram()
            with resumetab:
                resumeProgram()


def AddnewProgram_wo():
    global machine_selection
    action_selection = st.selectbox(label="select Action on current Program", options=[
                                    "Pause Current Program", "Stop Current Program"])
    programNameInput = st.text_input(
        label="Program Name *", placeholder="...")
    noSubProgramsInput = st.number_input(
        label="No. of Sub-Programs *", min_value=0, value=0, step=1)
    customerNameInput = st.text_input(
        label="Project Name *", placeholder="...")
    componentNameInput = st.text_input(
        label="Component Name *", placeholder="...")
    estimatedTimeInput = st.number_input(
        label="Estimated Time (in mins) *", min_value=0, value=0, step=1)
    submit_program_button = st.button(
        label="Submit", type="primary")

    if submit_program_button:
        if action_selection == "Stop Current Program":
            stopselected()
            st.success(
                "Current Program has been Stopped.\n please press 'R' to refresh the data")
        if action_selection == "Pause Current Program":
            pauseCurrent()
        if (programNameInput == "" or customerNameInput == "" or componentNameInput == "" or machine_selection == None):
            st.write("please enter all the requred information")
        else:
            dfs = getProgramData()
            dfs = dfs[dfs["name"] ==
                      machineselectionlistmapping.get(machine_selection)]
            getinfluxLock()
            if dfs.size > 0:

                maxpriority = int(dfs["Priority"].max())

                jsontoinflux = [{
                    "tags": {
                        "MachineName": dfs.iloc[0]["MachineName"],
                        "MainProgramName": programNameInput,
                        "ComponentName": componentNameInput,
                        "EstimatedTime": estimatedTimeInput,
                        "NoOfSubPrograms": int(noSubProgramsInput),
                        "CompletedSubPrograms": 0,
                        "CustomerName": customerNameInput,
                        "Priority": maxpriority+1
                    },
                    "fields": {
                        "name": machineselectionlistmapping.get(machine_selection)
                    },
                    "measurement": "ALP_ProgramData"
                }]
            else:
                maxpriority = 0
                jsontoinflux = [{
                    "tags": {
                        "MachineName": machinenamemapping.get(machineselectionlistmapping.get(machine_selection)),
                        "MainProgramName": programNameInput,
                        "ComponentName": componentNameInput,
                        "EstimatedTime": estimatedTimeInput,
                        "NoOfSubPrograms": int(noSubProgramsInput),
                        "CompletedSubPrograms": 0,
                        "CustomerName": customerNameInput,
                        "Priority": maxpriority+1
                    },
                    "fields": {
                        "name": machineselectionlistmapping.get(machine_selection)
                    },
                    "measurement": "ALP_ProgramData"
                }]
            # getinfluxLock()
            writetoinflux(jsontoinflux)
            releaseinfluxlock()
            st.success(
                "New Program Added.\n Please press 'R' to refresh the data")


def AddnewProgram():
    global machine_selection
    # action_selection = st.selectbox(label="select Action on current Program",options=["Pause Current Program","Stop Current Program"])
    programNameInput = st.text_input(
        label="Program Name *", placeholder="...")
    noSubProgramsInput = st.number_input(
        label="No. of Sub-Programs *", min_value=0, value=0, step=1)
    customerNameInput = st.text_input(
        label="Project Name *", placeholder="...")
    componentNameInput = st.text_input(
        label="Component Name *", placeholder="...")
    estimatedTimeInput = st.number_input(
        label="Estimated Time (in mins) *", min_value=0, value=0, step=1)
    submit_program_button = st.button(
        label="start Program", type="primary")

    if submit_program_button:
        # st.write("button Pressed with data", machine_selection, programNameInput,
        #          noSubProgramsInput, customerNameInput, componentNameInput, estimatedTimeInput, "action:::", action_selection)
        # if action_selection == "Stop Current Program":
        #     stopselected()
        #     st.write("Current Program has been Stopped.")
        if (programNameInput == "" or customerNameInput == "" or componentNameInput == "" or machine_selection == None):
            st.write("please enter all the requred information")
        else:
            dfs = getProgramData()
            # st.write(dfs.size,dfs)
            dfs = dfs[dfs["name"] ==
                      machineselectionlistmapping.get(machine_selection)]
            if dfs.size > 0:
                maxpriority = int(dfs["Priority"].max())
                jsontoinflux = [{
                    "tags": {
                        "MachineName": dfs.iloc[0]["MachineName"],
                        "MainProgramName": programNameInput,
                        "ComponentName": componentNameInput,
                        "EstimatedTime": estimatedTimeInput,
                        "NoOfSubPrograms": int(noSubProgramsInput),
                        "CompletedSubPrograms": 0,
                        "CustomerName": customerNameInput,
                        "Priority": maxpriority+1
                    },
                    "fields": {
                        "name": machineselectionlistmapping.get(machine_selection)
                    },
                    "measurement": "ALP_ProgramData"
                }]
            else:
                maxpriority = 0
                jsontoinflux = [{
                    "tags": {
                        "MachineName": machinenamemapping.get(machineselectionlistmapping.get(machine_selection)),
                        "MainProgramName": programNameInput,
                        "ComponentName": componentNameInput,
                        "EstimatedTime": estimatedTimeInput,
                        "NoOfSubPrograms": int(noSubProgramsInput),
                        "CompletedSubPrograms": 0,
                        "CustomerName": customerNameInput,
                        "Priority": maxpriority+1
                    },
                    "fields": {
                        "name": machineselectionlistmapping.get(machine_selection)
                    },
                    "measurement": "ALP_ProgramData"
                }]
            getinfluxLock()
            writetoinflux(jsontoinflux)
            releaseinfluxlock()
            st.success(
                "New Program Added.\n Please press 'R' to refresh the data")


def resumeProgram():
    global machine_selection
    dfs = getProgramData()
    if dfs.size > 0:
        dfg = dfs.copy()
        dfg = dfg[dfg["CompletedSubPrograms"] < dfg["NoOfSubPrograms"]]
        dfg = dfg.sort_values(by="Priority", ascending=False).reset_index()
        dff = dfg.copy()
        dff["ProjectName"] = dff["CustomerName"]
        dff = dff[["name", "ProjectName", "MainProgramName",
                   "NoOfSubPrograms", "CompletedSubPrograms"]]
        if dfg.size > 0:
            st.write("paused Programs:")
            st.write(dff)
            program_to_resume = st.number_input(
                label="Index of Program to resume *", min_value=0, value=0, step=1)
            resume_program_button = st.button(
                label="Resume Program", type="primary")
            if resume_program_button:
                # st.write("buttonpressed",program_to_resume)
                selected_program = dfg.iloc[program_to_resume]
                # st.write(selected_program)
                resumeSelected(selected_program)
                st.success("program resumed on "+machine_selection +
                           "\nplease press 'R' to refresh the data")

        else:
            st.write("No Programs available to resume")
    else:
        st.write("No Programs available to resume")


def resumeSelected(program_to_resume: pd.DataFrame):
    global machine_selection
    dfs = getProgramData()
    getinfluxLock()
    dfs[["NoOfSubPrograms", "CompletedSubPrograms", "Priority"]] = dfs[[
        "NoOfSubPrograms", "CompletedSubPrograms", "Priority"]].astype(str).astype(int)
    # print(program_to_resume)
    # st.write(dfs, program_to_resume)
    ind = dfs.loc[(dfs["MachineName"] == program_to_resume["MachineName"]) &
                  (dfs["MainProgramName"] == program_to_resume["MainProgramName"]) &
                  (dfs["ComponentName"] == program_to_resume["ComponentName"]) &
                  (dfs["EstimatedTime"] == program_to_resume["EstimatedTime"]) &
                  (dfs["NoOfSubPrograms"] == int(program_to_resume["NoOfSubPrograms"])) &
                  (dfs["CompletedSubPrograms"] == int(program_to_resume["CompletedSubPrograms"]))].index[0]
    print(ind)
    dfg = dfs.copy()
    dfg = dfg[dfg["name"] ==
              machineselectionlistmapping.get(machine_selection)]
    maxpriority = 0
    if dfg.size > 0:
        maxpriority = int(dfg["Priority"].max())
    dfs.at[ind, "Priority"] = maxpriority+1
    dfs.at[ind, "name"] = machineselectionlistmapping.get(machine_selection)
    dfs.at[ind, "MachineName"] = machinenamemapping.get(
        machineselectionlistmapping.get(machine_selection))
    query = 'DROP MEASUREMENT ALP_ProgramData'
    result = influxdb_client.query(query)
    for index, row in dfs.iterrows():
        jsontoinflux = [{
            "tags": {
                "MachineName": row["MachineName"],
                "MainProgramName": row["MainProgramName"],
                "ComponentName": row["ComponentName"],
                "EstimatedTime": row["EstimatedTime"],
                "NoOfSubPrograms": row["NoOfSubPrograms"],
                "CompletedSubPrograms": row["CompletedSubPrograms"],
                "CustomerName": row["CustomerName"],
                "Priority": row["Priority"]
            },
            "fields": {
                "name": row["name"]
            },
            "measurement": "ALP_ProgramData"
        }]
        # print(jsontoinflux)
        writetoinflux(jsontoinflux)
    releaseinfluxlock()


def stopselected():
    global machine_selection

    dfs = getProgramData()
    df = dfs.copy()
    getinfluxLock()
    df = df[df["name"] == machineselectionlistmapping.get(machine_selection)]
    df = df.sort_values(by="Priority", ascending=False).reset_index()
    df = df.iloc[0]
    dropindex = dfs[((dfs["MachineName"] == df["MachineName"]) &
                     (dfs["MainProgramName"] == df["MainProgramName"]) &
                     (dfs["ComponentName"] == df["ComponentName"]) &
                     (dfs["EstimatedTime"] == df["EstimatedTime"]) &
                     (dfs["NoOfSubPrograms"] == df["NoOfSubPrograms"]) &
                     (dfs["CompletedSubPrograms"] == df["CompletedSubPrograms"]) &
                     (dfs["CustomerName"] == df["CustomerName"]) &
                     (dfs["Priority"] == df["Priority"]))].index
    dfs.drop(dropindex, inplace=True)
    query = 'DROP MEASUREMENT ALP_ProgramData'
    result = influxdb_client.query(query)
    for index, row in dfs.iterrows():
        jsontoinflux = [{
            "tags": {
                "MachineName": row["MachineName"],
                "MainProgramName": row["MainProgramName"],
                "ComponentName": row["ComponentName"],
                "EstimatedTime": row["EstimatedTime"],
                "NoOfSubPrograms": row["NoOfSubPrograms"],
                "CompletedSubPrograms": row["CompletedSubPrograms"],
                "CustomerName": row["CustomerName"],
                "Priority": row["Priority"]
            },
            "fields": {
                "name": row["name"]
            },
            "measurement": "ALP_ProgramData"
        }]
        # print(jsontoinflux)
        writetoinflux(jsontoinflux)
    releaseinfluxlock()
    addprogramdisabled = False
    statusactionbuttondisabled = True


def pauseCurrent():
    global machine_selection
    dfs = getProgramData()
    dfs[["NoOfSubPrograms", "CompletedSubPrograms"]] = dfs[[
        "NoOfSubPrograms", "CompletedSubPrograms"]].astype(str).astype(int)
    getinfluxLock()
    if dfs.size > 0:
        dfg = dfs.copy()
        dfg = dfg[dfg["name"] ==
                  machineselectionlistmapping.get(machine_selection)]
        dfg = dfg.sort_values(by="Priority", ascending=False).reset_index()
        currentprogram = dfg.iloc[0]
        # currentprogram["name"]="--"
        # currentprogram["MachineName"]="--"
        ind = dfs.loc[(dfs["MachineName"] == currentprogram["MachineName"]) &
                      (dfs["MainProgramName"] == currentprogram["MainProgramName"]) &
                      (dfs["ComponentName"] == currentprogram["ComponentName"]) &
                      (dfs["EstimatedTime"] == currentprogram["EstimatedTime"]) &
                      (dfs["NoOfSubPrograms"] == currentprogram["NoOfSubPrograms"]) &
                      (dfs["CompletedSubPrograms"] == currentprogram["CompletedSubPrograms"]) &
                      (dfs["CustomerName"] == currentprogram["CustomerName"])].index[0]
        dfs.at[ind, "name"] = "--"
        dfs.at[ind, "MachineName"] = "--"
        query = 'DROP MEASUREMENT ALP_ProgramData'
        result = influxdb_client.query(query)
        for index, row in dfs.iterrows():
            jsontoinflux = [{
                "tags": {
                    "MachineName": row["MachineName"],
                    "MainProgramName": row["MainProgramName"],
                    "ComponentName": row["ComponentName"],
                    "EstimatedTime": row["EstimatedTime"],
                    "NoOfSubPrograms": row["NoOfSubPrograms"],
                    "CompletedSubPrograms": row["CompletedSubPrograms"],
                    "CustomerName": row["CustomerName"],
                    "Priority": row["Priority"]
                },
                "fields": {
                    "name": row["name"]
                },
                "measurement": "ALP_ProgramData"
            }]
        # print(jsontoinflux)
            writetoinflux(jsontoinflux)
        releaseinfluxlock()

st.markdown("""
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
""", unsafe_allow_html=True)

userLogin()
