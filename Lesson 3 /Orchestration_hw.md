Question 1: Context Engineering
Try the following experiment:

Open ChatGPT in a private browser window: https://chatgpt.com
Enter this prompt: "Create a Kestra flow that loads NYC taxi data from CSV to BigQuery"
Then, use Kestra's AI Copilot with the same prompt
After trying the same prompt in ChatGPT vs Kestra's AI Copilot, what is the primary reason AI Copilot generates better Kestra flows?





Chatgpt: 

id: nyc_taxi_csv_to_bigquery
namespace: company.analytics

variables:
  project_id: my-gcp-project
  bucket: my-data-bucket
  dataset: nyc_taxi
  table: yellow_tripdata
  file_name: yellow_tripdata_2024-01.csv
  source_url: https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.csv

tasks:
  - id: download_csv
    type: io.kestra.plugin.core.http.Download
    uri: "{{ vars.source_url }}"

  - id: upload_to_gcs
    type: io.kestra.plugin.gcp.gcs.Upload
    from: "{{ outputs.download_csv.uri }}"
    bucket: "{{ vars.bucket }}"
    name: "{{ vars.file_name }}"

  - id: create_dataset
    type: io.kestra.plugin.gcp.bigquery.Query
    projectId: "{{ vars.project_id }}"
    sql: |
      CREATE SCHEMA IF NOT EXISTS `{{ vars.project_id }}.{{ vars.dataset }}`;

  - id: create_table
    type: io.kestra.plugin.gcp.bigquery.Query
    projectId: "{{ vars.project_id }}"
    sql: |
      CREATE TABLE IF NOT EXISTS `{{ vars.project_id }}.{{ vars.dataset }}.{{ vars.table }}`
      (
        VendorID INTEGER,
        tpep_pickup_datetime TIMESTAMP,
        tpep_dropoff_datetime TIMESTAMP,
        passenger_count FLOAT64,
        trip_distance FLOAT64,
        RatecodeID FLOAT64,
        store_and_fwd_flag STRING,
        PULocationID INTEGER,
        DOLocationID INTEGER,
        payment_type INTEGER,
        fare_amount FLOAT64,
        extra FLOAT64,
        mta_tax FLOAT64,
        tip_amount FLOAT64,
        tolls_amount FLOAT64,
        improvement_surcharge FLOAT64,
        total_amount FLOAT64,
        congestion_surcharge FLOAT64,
        Airport_fee FLOAT64
      );

  - id: load_csv
    type: io.kestra.plugin.gcp.bigquery.LoadFromGcs
    projectId: "{{ vars.project_id }}"
    from:
      - "gs://{{ vars.bucket }}/{{ vars.file_name }}"
    destinationTable: "{{ vars.project_id }}.{{ vars.dataset }}.{{ vars.table }}"
    format: CSV
    autodetect: true
    skipLeadingRows: 1
    writeDisposition: WRITE_TRUNCATE

  - id: verify_load
    type: io.kestra.plugin.gcp.bigquery.Query
    projectId: "{{ vars.project_id }}"
    fetch: true
    sql: |
      SELECT COUNT(*) AS row_count
      FROM `{{ vars.project_id }}.{{ vars.dataset }}.{{ vars.table }}`;



Kestra:



Question 2: RAG vs No RAG
 
No RAG 

INFO 2026-07-04T06:18:10.219214Z ❌ Response WITHOUT RAG (no retrieved context):
Kestra 1.1 introduced several exciting features that significantly enhanced its capabilities. Here are 5 major features with brief descriptions:

1.  **Event-Driven Flows (Triggers):** This was a major leap forward, allowing Kestra workflows to be triggered by external events. Instead of just scheduled or manually launched flows, users could now define triggers based on various sources (e.g., file arrival in S3, a message on Kafka, or an HTTP request). This enables truly reactive and integrated automation, making Kestra a powerful tool for event-driven architectures.

2.  **Plugin Management UI:** Kestra 1.1 introduced a user-friendly graphical interface for managing plugins. Before this, adding or updating plugins often involved manual file system operations or server restarts. The new UI streamlined the process, making it much easier for users to browse, install, update, and remove plugins directly from the Kestra interface, thus improving the overall user experience and reducing operational overhead.

3.  **Namespace-Level Variables:** This feature enhanced the reusability and organization of configurations within Kestra. It allowed users to define variables that are scoped to an entire namespace, meaning all flows within that namespace could access those variables. This is particularly useful for storing environment-specific configurations (e.g., database connection strings, API keys) that need to be shared across multiple flows without hardcoding them in each individual flow, promoting the DRY (Don't Repeat Yourself) principle.

4.  **Enhanced Retry Strategies:** Kestra 1.1 brought more sophisticated and flexible retry mechanisms for tasks. Users gained more control over how tasks should be retried in case of failure, including options like exponential backoff, custom delays, and specific conditions for retrying. This significantly improved the robustness and resilience of workflows, reducing manual intervention and making flows more tolerant to transient errors.

5.  **New and Improved Task Types:** While not a single feature, Kestra 1.1 significantly expanded its task library and improved existing ones. This included new tasks for various integrations (e.g., more database connectors, cloud service integrations) and enhancements to core tasks. This continuous expansion of available tasks is crucial for Kestra's versatility, allowing users to automate an even wider range of operations and integrate with more systems out-of-the-box.

🤔 Did you notice that this response seems to be:
- Incorrect?
- Vague/generic?
- Listing features that haven't been added in exactly this version but rather a long time ago?

👉 This is why context matters! Run `2_chat_with_rag.yaml` to see the accurate, context-grounded response.




RAG

INFO 2026-07-04T06:19:05.033852Z ✅ RAG Response (with retrieved context):
Kestra 1.1 introduced several major features, including:

1.  **New Filters**: The UI filters across Kestra were completely redesigned based on user feedback. The new design is cleaner, more intuitive, and more powerful, offering explicit filter options, single-click resets, the ability to save frequently used filter combinations, and options to hide, show, or reorder table columns.

2.  **No-Code Dashboard Editor**: This feature extends the No-Code Multi-Panel Editor to custom dashboards, allowing users to build and customize dashboards directly from the UI without writing YAML. Users can create data sources, visualizations, and charts using form-based tabs and switch between "Dashboard Code" and "No-Code" panels to see generated YAML in real time.

3.  **Multi-Agent AI Systems**: AI agents in Kestra can now use other AI agents as tools, enabling sophisticated multi-agent orchestration workflows. This allows a primary agent to delegate subtasks to specialized expert agents, creating hierarchies of AI reasoning within the orchestration layer.

4.  **Fix with AI**: When task runs fail, Kestra 1.1 can now provide AI-powered suggestions to help users quickly diagnose and resolve issues. This feature analyzes failed task runs and offers intelligent recommendations for fixing the problem, speeding up troubleshooting.

5.  **Human Task**: (Enterprise Edition) This feature allows for human-in-the-loop workflows. When an execution reaches a human task, it pauses until designated users or group members manually approve and resume it, making it suitable for workflows requiring human validation before proceeding with critical operations.

Other significant features include `MailReceivedTrigger` and `RealTimeTrigger` for email-driven workflows, enhanced file detection triggers that react to both new and updated files, and improved air-gapped support. Additionally, Kestra 1.1 introduced dozens of new plugins across various categories like Data & Database, SaaS & API Integrations, Cloud & Infrastructure, and AI Model Providers.

🎉 Note that this response is detailed, accurate, and grounded in the actual release documentation. Compare this with the output from 1_chat_without_rag.yaml!






Question 3: Token usage — short summary




INFO 2026-07-04T06:27:24.579762Z 📊 Token Usage Summary:

Multilingual Agent:
- Input tokens: 282
- Output tokens: 82
- Total tokens: 364

English Brevity Agent:
- Input tokens: 97
- Output tokens: 38
- Total tokens: 135

💡 Tip: Monitor token usage to understand costs and optimize prompts!





Question 4: Token usage — long summary


INFO 2026-07-04T06:29:35.042855Z 📊 Token Usage Summary:

Multilingual Agent:
- Input tokens: 282
- Output tokens: 206
- Total tokens: 488

English Brevity Agent:
- Input tokens: 221
- Output tokens: 56
- Total tokens: 277

💡 Tip: Monitor token usage to understand costs and optimize prompts!







Question 5: Modifying a flow
Open 4_simple_agent.yaml in the Kestra flow editor. Find the english_brevity task and change its prompt from asking for exactly 1 sentence to asking for exactly 3 sentences.

Save the flow, then run it with summary_length = long.

Compare the english_brevity output token count to the original 1-sentence version (also with summary_length = long). How do they compare?


INFO 2026-07-04T06:39:40.842649Z 📊 Token Usage Summary:

Multilingual Agent:
- Input tokens: 282
- Output tokens: 84
- Total tokens: 366

English Brevity Agent:
- Input tokens: 99
- Output tokens: 77
- Total tokens: 176

💡 Tip: Monitor token usage to understand costs and optimize prompts!





Question 6: Best Practices
