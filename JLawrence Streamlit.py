import streamlit as st
import pandas as pd
import plotly.express as px

# Page title
st.set_page_config(page_title="JLawrence Streamlit Profile", layout="wide")

# Initialize idebar Menu
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Go to:",
    ["Intern Profile", "Training and onsite duty", "Cluster Data", "Extra", "Contact"]
)

# Cluster data table
cluster_data = pd.DataFrame({
    "System": ["CPU","Cores","Speed","RAM","GPU","GPU RAM"],
    "Compute Nodes": ["Intel Xeon", 24, "2.6 Ghz", "128GB / 64GB", "", ""],
    "'Fat Nodes'": ["Intel Xeon", 56, "2.6 GHz", "1TB", "", "" ],
    "GPU Nodes": ["Intel Xeon", 36, "2.2GHz","32 GB","Nvidia V100", "16GB / 32GB"]
    })

#Login user data
login_data = pd.read_csv("user_login.csv")

# Sections based on menu selection
if menu == "Intern Profile":
    st.title("Intern Profile")
    st.sidebar.header("Profile Options")

    # Basic information
    name = "Joshua Lawrence"
    position = "System Admininstrator Intern"
    field = "High Performance Computing"
    institution = "Center for High Performance Computing (CHPC)"
    
    
    # Display basic information
    st.write(f"**My name:** {name}")
    st.write(f"**My Job position:** {position}")
    st.write(f"**My field:** {field}")
    st.write(f"**Institution:** {institution}")
    
    st.write("Hello, I am intern at **CHPC**. My main role is being a **System Admininstrator**. My duty is to maintain and manage CHPC'S main data centre which is named **Lengau** (Setswana for cheetah).")
    st.image("https://images.squarespace-cdn.com/content/v1/588a02f11b10e3d4643f5c35/1597182547862-KQUEER7HVSTKJJV8AKCC/System+Admin+for+the+Software+Developer.jpg")    
    
    
#Navigation Menu Selection
elif menu == "Training and onsite duty":
    st.title("Training and onsite duty")
    st.sidebar.header("Upload and Filter")
    
    st.write("Some of my work duties include: ")
    st.write("""  
•  Using cluster management software to monitor and manage cluster resources. As well as measure system reliability and availability. \n
•  Monitor all server nodes and restore faulty ones, both physically and virtually.\n
•  Monitor and maintain the storage file system Lustre.\n
•  Supervise and report the status of NFS, Lustre and nodes' statuses.\n
•  Write scripts, as well as update existing ones to monitor Lengau and detect any issues.\n
•  Handle creation of user accounts on CHPC systems.\n
•  Resolve and update helpdesk tickets.\n
""")

    st.write("My main tool I use for work is MobaXterm, its a ssh client which you will be familiar with if you are a lengau user, but I am aware there are other apps that do the needed work for cluster login.")
    
    st.divider()

    st.title("Some Work examples / Projects")
    
    #Tab creation for custom display
    tab1, tab2 = st.tabs(["HyperThread Script", "Raspberry Pi Cluster"])
    with tab1:
        #Bash code snippet
        
        st.write("Below is a snippet of a bash script which I have made to check for hyperthreading in the cluster. There is probably a better way to do this but this is the method i have come up with and works as well as I need it to: ")
        st.code("""
                #!/bin/bash
    
    #This specifies the node ranges, skipping nodes 721-793 as those nodes are from rack 11.
    ranges=({0005..0720} {0793..1368})
    
    #This is specifying the email addresses that must get notified.
    emailfile=/root/admin_emails.txt
    recieve=$(paste -sd, "$emailfile")
    
    #Loops through the ranges mentioned above
    for x in "${ranges[@]}"; do
    
            #This command ssh's into the node then finds how many threads per core is active.
            #If there is more than 1 thread per core then a node has hyperthreading active.
            threadcheck=$(ssh -o ConnectTimeout=3 -o BatchMode=yes "cnode$x" lscpu | grep -F 'Thread(s) per core' |  awk -F':' '{print $2}')
            if (("$threadcheck" > 1 )); then
                    echo "Cnode$x has hyper-threading enabled."
                    #Echos the nodes to a file
                    echo "Cnode$x" >> hyperthreadNodes.txt
            fi
    
    done
    
    #This detects if the hypernode file exists or has data in it and sends the list to admins if data is found.
    if [ -s hyperthreadNodes.txt ]; then
            (
             echo " Here is the list of cnodes with hyperthreading enabled:"
             echo "====================================="
             cat hyperthreadNodes.txt
             #Sends a mail with the node list to the admins.
            ) | mail -s "HyperThreaded Nodes" "$recieve"
    fi
    #Removes the nodes file as the list has already been sent to admins.
    rm -f hyperthreadNodes.txt
    
                """, language="bash")

    with tab2:
        #Raspberry pi information
        st.write("I also have constructed a Raspberry Pi mini-cluster, which functions pretty much like a normal cluster. Connected together via a swtich.")
        st.image("Raspberry1.jpg", caption="Raspberry Pi Cluster: They are all connected via a ethernet switch meaning they share the same LAN.", width=700)
        st.write("There is 1 head node (Bottom left node in the left tower), which hosts all the TFTP, DHCP and NFS services. The top right node(in right tower) is the storage node, which has an attached hard drive in which said drive is mounted across the entire local network. For training before making the raspberry pi, I used Sebowa to practise simulating nodes in a cluster. Sebow is a localised cloud provided by NICIS which lets me create virtual machines online with the hardware requirements that I need.")
        st.image("Raspberry2.jpg", caption="Here is a photo of the cluster at the side, my laptop and a monitor when I used it to debug some errors when I could not SSH into the cluster", width=300)
        

elif menu == "Cluster Data":
    st.title("Cluster Data")
    st.sidebar.header("Data Selection")

    st.write("The Main cluster at the CHPC is called **Lengau**, it is a system comprised of Dell servers, powered by Intel processors. The cluster is managed by Bright Cluster Manager.")
    st.write("""
             The **Lengau Cluster** has: \n
             • **1368** Compute nodes and **9** GPU nodes. \n
             • **148 TB** of memory. \n
             • **1.029** Peta-flops of speed. \n
             • Infiniband connections. \n
             • **4 PB** of Lustre Storage.
             """)
    
    st.write("Here is a table of the cluster, just describing what type of processors ar used and other technical statistics.")
    #Dataframe for displaying the cluster data table
    st.dataframe(cluster_data, hide_index=True)
    
    #Images of the cluster       
    st.image(
        "https://cisp.cachefly.net/assets/articles/images/resized/0000556134_resized_lengausupercomputercsir06161022.jpg",
        caption="Lengau Cluster1", width = 600)
    st.image("https://static.wixstatic.com/media/a8718f_da3e722dbca14453ae686de9bd33713c~mv2.jpg/v1/fill/w_644,h_430,al_c,lg_1,q_80,enc_avif,quality_auto/a8718f_da3e722dbca14453ae686de9bd33713c~mv2.jpg",
             caption="Lengau Cluster2", width = 600)
    

    st.divider()
    
    st.write("Here is a chart of users that have logged into the lengau cluster, over the past 2 days.")
    #Small line chart showing the number of users on the system (feb 1 - feb 2)
    user_fig = px.line(login_data, x="Category", y="Users", title="Lengau cluster login from Feb 1-Feb 2 (Data from users.chpc.ac.za)")
    #Display plot
    st.plotly_chart(user_fig)        
        

elif menu == "Extra":
    st.title("Extra")
    
    st.write("This is the end of my profile, here is a picture of my late dog frankie: ")
    st.image("Frankie 005.jpg", caption="My dog Frankie", width = 600)
    
    
elif menu == "Contact":
    # Contact section
    st.title("Contact Information")
    
    email = "joshual1412@gmail.com"
    number = "0832930767"
    st.write(f"My number is: {number}")
    st.write(f"My email is {email}.")