# SmartHomeAnalytics
Real-Time IoT Data Pipeline for Smart Home Analytics

# Real-Time IoT Data Pipeline for Smart Home Analytics

## Overview
This project simulates a smart home environment where IoT devices (e.g., thermostats, motion sensors, smart lights) send real-time data to Azure. The data is processed, stored, and visualized to provide insights like energy usage patterns, device health, and anomaly detection.

## Project Architecture
- **Data Ingestion:** IoT devices send data to Azure Event Hubs.
- **Data Processing:** Azure Stream Analytics processes the data in real-time.
- **Data Storage:** Processed data is stored in Azure Data Lake Storage (ADLS) and Azure Cosmos DB.
- **Data Visualization:** Power BI is used to create dashboards for analytics.
- **Orchestration:** Azure Data Factory orchestrates the pipeline.

## Prerequisites
- An Azure account
- Python installed on your local machine
- Azure Event Hubs SDK for Python
- Power BI Desktop installed

## Setup Instructions

### Step 1: Set Up Azure Environment
1. **Create an Azure Account:**
   - [Sign up for a free Azure account](https://azure.microsoft.com/free/).

2. **Create Resources:**
   - **Azure Event Hubs:** For real-time data ingestion.
   - **Azure Stream Analytics:** For real-time data processing.
   - **Azure Data Lake Storage (ADLS):** For storing raw and processed data.
   - **Azure Cosmos DB:** For storing processed data in a NoSQL format.
   - **Azure Data Factory:** For orchestrating the pipeline.
   - **Power BI:** For visualization.

### Step 2: Simulate IoT Data
1. **Prepare Your Environment:**
   - Ensure Python is installed on your local machine.
   - Install an IDE like Visual Studio Code or PyCharm.

2. **Install Azure Event Hubs SDK:**
   - Run the following command:
     ```bash
     pip install azure-eventhub
     ```

3. **Write the Python Script:**
   - Create a file `simulate_iot_data.py` with the following code:
     ```python
     import random
     import time
     from azure.eventhub import EventHubProducerClient, EventData

     connection_str = "<Event-Hubs-Connection-String>"
     eventhub_name = "<Event-Hub-Name>"

     producer = EventHubProducerClient.from_connection_string(connection_str, eventhub_name)

     def generate_iot_data():
         return {
             "device_id": random.randint(1, 100),
             "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
             "temperature": random.uniform(20, 30),
             "motion": random.choice([True, False]),
             "light_status": random.choice(["ON", "OFF"])
         }

     while True:
         event_data = EventData(str(generate_iot_data()))
         producer.send_batch([event_data])
         time.sleep(5)  # Send data every 5 seconds
     ```

4. **Configure and Run the Script:**
   - Replace `<Event-Hubs-Connection-String>` and `<Event-Hub-Name>` with your Event Hub details.
   - Run the script to send simulated IoT data to Azure Event Hubs:
     ```bash
     python simulate_iot_data.py
     ```

### Step 3: Ingest Data Using Azure Event Hubs
1. **Create an Event Hub:**
   - Go to Azure Portal → Event Hubs → Create a new Event Hub.
   - Set Partition Count and Message Retention.

### Step 4: Process Data Using Azure Stream Analytics

1. **Create a Stream Analytics Job:**
   - Go to Azure Portal → Stream Analytics → Create a new job.
   - **Subscription:** Select your Azure subscription.
   - **Resource Group:** `MySmartHomeProject`
   - **Job Name:** `MySmartHomeStreamAnalytics`
   - **Region:** Select the region closest to you.
   - **Hosting environment:** Select **Cloud**.
   - Review the configuration and click **Create**.

2. **Configure Event Hub Input:**
   - Navigate to your Stream Analytics job (`MySmartHomeStreamAnalytics`).
   - Under the **Job topology** section, click on **Inputs**.
   - Click on **Add stream input** and select **Event Hub**.
   - Configure the input settings as follows:
     - **Input alias:** `input-eventhub`
     - **Service Bus Namespace:** Select `MySmartHomeNamespace`.
     - **Event Hub Name:** Select `MySmartHomeEventHub`.
     - **Event Hub Policy Name:** Choose the shared access policy with `Listen` permissions.
     - **Event Hub Consumer Group:** `$Default` (or a custom consumer group if you created one).
     - **Event serialization format:** Select **JSON**.
     - **Encoding:** Set to `UTF-8`.

3. **Write the Stream Analytics Query:**
   - Under the **Job topology** section, click on **Query**.
   - Write the following query to process the data:
     ```sql
     SELECT
         device_id,
         temperature,
         motion,
         light_status,
         System.Timestamp AS processing_time
     INTO
         [output-adls]
     FROM
         [input-eventhub]
     WHERE
         temperature > 25
     ```

4. **Configure Outputs:**
   - **Output to Azure Data Lake Storage (ADLS):**
     - Under the **Job topology** section, click on **Outputs**.
     - Click on **Add** and select **Azure Data Lake Storage**.
     - Configure the output settings as follows:
       - **Output alias:** `output-adls`
       - **Subscription:** Select your Azure subscription.
       - **Storage Account:** `mysmarthomedatalake`
       - **Storage Path Prefix:** `processed-data/{date}/{time}` (customize as needed)
       - **Output Format:** JSON

   - **Output to Azure Cosmos DB:**
     - Under the **Job topology** section, click on **Outputs**.
     - Click on **Add** and select **Cosmos DB**.
     - Configure the output settings as follows:
       - **Output alias:** `output-cosmosdb`
       - **Subscription:** Select your Azure subscription.
       - **Database:** `SmartHomeAnalytics`
       - **Collection:** `ProcessedData`
       - **Account:** Select your Cosmos DB account (`mysmarthomecosmosdb`).
       - **Document ID:** Specify the unique identifier for documents (e.g., `device_id`).
       - **Partition Key:** `/device_id`
       - **Throughput:** Ensure throughput is set to handle your data ingestion needs.

5. **Start the Stream Analytics Job:**
   - Once you have configured the input, query, and outputs, click on **Overview** in the left-hand menu.
   - Click on **Start** to start the Stream Analytics job.

### **Step 5: Store Data in Azure Data Lake Storage and Cosmos DB**

#### **1\. Create ADLS and Cosmos DB Resources**

Since you've already created these resources, we'll proceed with configuring your Stream Analytics job to store the processed data.

#### **2\. Configure Output to Azure Data Lake Storage (ADLS)**

1. **Navigate to Your Stream Analytics Job:**  
   * Go to the Azure Portal and navigate to your Stream Analytics job (`MySmartHomeStreamAnalytics`).  
2. **Add Output to ADLS:**  
   * Under the **Job topology** section, click on **Outputs**.  
   * Click on **Add** and select **Azure Data Lake Storage**.  
   * Configure the output as follows:  
     * **Output alias:** `output-adls`  
     * **Subscription:** Select your Azure subscription.  
     * **Storage Account:** `mysmarthomedatalake`  
     * **Storage Path Prefix:** `processed-data/{date}/{time}` (customize as needed)  
     * **Output Format:** JSON

#### **3\. Configure Output to Azure Cosmos DB**

1. **Add Output to Cosmos DB:**  
   * Under the **Job topology** section, click on **Outputs**.  
   * Click on **Add** and select **Cosmos DB**.  
   * Configure the output as follows:  
     * **Output alias:** `output-cosmosdb`  
     * **Subscription:** Select your Azure subscription.  
     * **Database:** `SmartHomeAnalytics`  
     * **Collection:** `ProcessedData`  
     * **Account:** Select your Cosmos DB account (`mysmarthomecosmosdb`).  
     * **Document ID:** Specify the unique identifier for documents (e.g., `device_id`).  
     * **Partition Key:** `/device_id`  
     * **Throughput:** Ensure throughput is set to handle your data ingestion needs.

Once you have configured the outputs, your Stream Analytics job will store the processed data in Azure Data Lake Storage for batch analytics and in Azure Cosmos DB for real-time queries.

Next, we will set up the orchestration using Azure Data Factory.

### Step 6: Orchestrate the Pipeline Using Azure Data Factory

1. **Create a Data Factory:**
   - Go to Azure Portal → Data Factory → Create a new Data Factory.
   - **Subscription:** Select your Azure subscription.
   - **Resource Group:** `MySmartHomeProject`
   - **Name:** `MySmartHomeDataFactory`
   - **Region:** Select the region closest to you.
   - **Version:** V2
   - Review the configuration and click **Create**.

2. **Open Azure Data Factory Studio:**
   - Click on **Author & Monitor** to open Azure Data Factory Studio.

3. **Create a New Pipeline:**
   - In the left-hand menu, click on the **Author** icon (pen icon).
   - Right-click on **Pipelines** and select **New pipeline**.
   - **Name:** Enter a name for the pipeline (e.g., `IoTDataPipeline`).

4. **Add Event Hub Ingestion Activity:**
   - **Source:** Azure Event Hubs
     - Create a new linked service and configure your Event Hub details.
     - **Linked Service Configuration:**
       - **Name:** `EventHubLinkedService`
       - **Service Bus namespace:** Enter your Event Hub namespace (`MySmartHomeNamespace`).
       - **Event Hub name:** Enter your Event Hub name (`MySmartHomeEventHub`).
       - **Event Hub policy name:** Enter the shared access policy with `Listen` permissions.
       - **Event Hub consumer group:** Enter the consumer group name (e.g., `$Default` or a custom consumer group).
     - **Sink:** Azure Data Lake Storage Gen2
       - Create a new linked service and configure your Data Lake Storage details.
       - **Linked Service Configuration:**
         - **Name:** `ADLSLinkedService`
         - **Storage account name:** Enter your Data Lake Storage account name (`mysmarthomedatalake`).
       - **File path:** Enter the path where you want to store the ingested data (e.g., `raw-data/`).
       - **File format:** Choose the format for the ingested data (e.g., `DelimitedText` or `JSON`).

5. **Add Data Processing Activity:**
   - Click on the **+ (Add)** icon and select **Azure Stream Analytics**.
   - **Stream Analytics job name:** Select `MySmartHomeStreamAnalytics`.
   - Configure the activity to run your Stream Analytics job to process the ingested data.

6. **Add Data Storage Activities:**
   - In the same pipeline, add activities to store the processed data in Azure Data Lake Storage and Cosmos DB.
   - **Data Lake Storage (ADLS):**
     - **Source:** Stream Analytics output from ADLS.
     - **Sink type:** Azure Data Lake Storage Gen2
     - **Folder path:** Enter the path where you want to store the processed data (e.g., `processed-data/`).
   - **Cosmos DB:**
     - **Source:** Stream Analytics output from Cosmos DB.
     - **Sink type:** Azure Cosmos DB
     - **Connection:** Create a new linked service and configure your Cosmos DB details.
     - **Linked Service Configuration:**
       - **Database:** `SmartHomeAnalytics`
       - **Collection:** `ProcessedData`

7. **Schedule the Pipeline:**
   - Add a trigger to schedule the pipeline to run at regular intervals.
   - **Trigger Configuration:**
     - **Trigger type:** Choose **Schedule**.
     - **Start date:** Set the start date and time for the trigger.
     - **Recurrence:** Define the frequency (e.g., every hour).

8. **Publish the Pipeline:**
   - Validate, debug, and publish the pipeline.

### Step 7: Visualize Data Using Power BI

1. **Download and Install Power BI Desktop:**
   - Download Power BI Desktop from [here](https://powerbi.microsoft.com/desktop/).

2. **Connect Power BI Desktop to Azure Cosmos DB:**
   - Open Power BI Desktop.
   - Click on **Get Data** from the Home tab.
   - Select **Azure** and then **Azure Cosmos DB**.
   - Enter your Cosmos DB account URL and key.
   - Select the database (`SmartHomeAnalytics`) and container (`ProcessedData`) you created.

3. **Create Reports and Dashboards:**
   - Use the data fields from Cosmos DB to create visuals like charts, graphs, and tables.
   - Customize and format the visuals to best represent your data insights.

4. **Publish to Power BI Service:**
   - Once your report is ready, click on **Publish** from the Home tab.
   - Sign in to your Power BI account.
   - Select the workspace where you want to publish your report.

5. **Create Dashboards in Power BI Service:**
   - Go to [Power BI Service](https://app.powerbi.com/).
   - Navigate to the workspace where you published your report.
   - Pin the visuals from your report to create a dashboard.
   - Share the dashboard with others by providing access to your workspace.

## Project Deliverables

1. **GitHub Repository:**
   - Host the project
   - Python script for IoT data simulation.
   - Stream Analytics query.
   - Screenshots of the pipeline and dashboards.
   - Detailed README explaining the architecture and steps.

2. **Documentation:**
   - Write a blog post or LinkedIn article about the project.
3. **Demo:**
   - Prepare a 5-minute demo to showcase the project.

## Tools and Technologies Used
  - **Azure Services:** Event Hubs, Stream Analytics, Data Lake Storage, Cosmos DB, Data Factory, Power BI.
  - **Programming:** Python for data simulation.
  - **SQL:** for Stream Analytics queries.
  - **Visualization:** Power BI for dashboards.
