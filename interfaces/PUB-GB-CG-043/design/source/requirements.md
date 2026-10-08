<!-- Converted from PUB-GB-CG-043-Web_To_Lead_Publisher_V0.1.docx (author A. Koyyada, 21/09/2026). Client principal values redacted. -->

**[Interface Design and]{.smallcaps}**

**[Specification (Publisher)]{.smallcaps}**

**[Calor GB]{.smallcaps}**

Author: Alekhya Koyyada

  ------------- ------------ ------------ -----------------------------------------
  **Version**   **Date**     **Author**   **Updates**

  1             21/09/2026   Alekhya      First Draft
                             Koyyada      

                                          
  ------------- ------------ ------------ -----------------------------------------

**\
**

**Instructions**

The guidelines for Integration Design Specification aim to provide a
complete design but lean. Hence the following instructions apply:

-   One single document must be created for the entire project.

-   One chapter per interface.

-   Do not capture redundant information.

-   Do not use hyperlinks as these tend to break; use reference numbers
    instead.

-   Populate sections as indicated below.

-   Do not remove any sections. In case of Not Applicable, just type
    N/A.

  -------------------------------------------------------------------------------------------------------------------------
  ![Warning with solid                                   Credentials (username and password) must not be written/stored in
  fill](media/image1.png){width="0.2956528871391076in"   this document. They must be collected and stored in a secure
  height="0.2956528871391076in"}                         fashion. In case of doubts on how to proceed, reach out your team
                                                         leader.
  ------------------------------------------------------ ------------------------------------------------------------------

  -------------------------------------------------------------------------------------------------------------------------

**[\
]{.smallcaps}**

# **Table of Contents** {#table-of-contents .TOC-Heading}

[1.1 PUB-GB-CG-043 [3](#pub-gb-cg-043)](\l)

[1.2 Requirements and Data Assessment
[4](#requirements-and-data-assessment)](\l)

[1.2.1 Business Requirements [4](#business-requirements)](\l)

[1.2.2 Non-Functional Requirements (NFR)
[4](#non-functional-requirements-nfr)](\l)

[1.2.3 Technical System Requirements
[5](#technical-system-requirements)](\l)

[1.2.4 Integration Artifacts [7](#_Toc525091560)](\l)

[1.3 Integration Design Specification
[8](#integration-design-specification)](\l)

[1.3.1 Solution Architecture [8](#solution-architecture)](\l)

[1.3.2 Interface Overview [9](#interface-overview)](\l)

[1.3.3 Tracking Field [10](#tracking-field)](\l)

[1.3.4 Exception Handling [10](#exception-handling)](\l)

[1.3.5 API Design Information [11](#api-design-information)](\l)

[API Design Sheet [12](#api-design-sheet)](\l)

[1.3.6 Design Decision [13](#design-decision)](\l)

## [PUB-GB-CG-043]{.smallcaps}

## Requirements and Data Assessment

### Business Requirements

**Interface Description**

This real-time integration interface is implemented to capture web form
submissions from Sitecore and send the data to Salesforce for Lead
creation.

**Business Requirement**

It is to Automate Lead/service request creation from selected web forms.

**Business Criticality**

The criticality of this interface is Medium.

**Process Description & End-to-End Process Identification**

**Short Description:**

This integration is responsible for sending data submitted by customers
through selected web forms through SiteCore to Salesforce via Boomi.

-   Sitecore sends the submitted form data to a Boomi REST API endpoint

-   **Processing:** Upon receiving the JSON payload, Boomi publishes the
    data to a Kafka topic, where it is consumed by a subscriber process.
    The subscriber listens for incoming payload and sends the data to
    Salesforce using the Salesforce Connector.

**E2E Interface Inventory SharePoint Link:**

**Timing and Triggering Requirements**

Event Driven -- Sitecore will invoke this service using Azure APIM via
Boomi Interface in real time.

**Business Units and Applications**

  -----------------------------------------------------------------------
  **Business Unit   **Business Unit   **Application     **Cloud / On
  Name**            Acronym**         Name**            Premise**
  ----------------- ----------------- ----------------- -----------------
  Calor GB          GB-CG             Sitecore          Cloud

  Calor GB          GB-CG             Salesforce        Cloud

  Calor GB          GB-CG             KAFKA             Cloud
  -----------------------------------------------------------------------

For global applications, use SHV Energy / GB-CG.

### Non-Functional Requirements (NFR)

  ------------------------------------------------------------------------
  **NFR**              **Description**               **Requirement**
  -------------------- ----------------------------- ---------------------
  **API Response       Response time expected by API 5s
  Time**                                             

  **API Max Response   Max. Response time expected   5s
  Time**               by API                        

  **API Volume**       This is the levels of load    60 per day
                       and concurrency under which   
                       our application has to        
                       perform                       

  **Integration        Integration schedule          N/A
  schedule**           requirements, if applicable   

  **Initial load       Volume of data in data volume The initial load will
  Volume/Frequency**   as well as number of          be similar to the
                       invocations for the initial   daily estimated.
                       (one-time) load               

  **Peak               Peak volume/frequency of data 75 /day
  Volume/Frequency**   in data volume as well as     
                       number of invocations         

  **Average            Average volume/frequency of   525 /week
  Volume/Frequency**   data in data volume as well   
                       as number of invocations      

  **Expected Volume    Expected volume natural       N/A
  Growth**             growth per month/year or      
                       growth spurts for example due 
                       to roll outs                  

  ***ANY OTHER...***                                 
  ------------------------------------------------------------------------

**Data Security**

Data will have the Customer Fields and is sensitive.

Sitecore to Azure APIM -- Oauth2.0

Boomi to SF-- SF Connector

**Data Format Validation**

Data validation is not part of Integration scope.

**Notes**

**·** Request JSON object is passed from Sitecore.

**·** For any connectivity error, Boomi will retry 3 times before
invoking the error handling process to notify the support teams.

Boomi process to be built as per guidelines outlined in [Boomi Best
Practices](https://shvenergy.sharepoint.com/:w:/s/NL_HQ-ICC-IntegrationTeam/ESauadDMDF5Fp_93Hd9ZU5QBeaBk7lIbe1BQ8h-t4h_oXg?e=83lIRd)

### Technical System Requirements

  -------------------------------------------------------------------------------------------------------------------------
  ![Warning with solid                                   Credentials (username and password) must not be written/stored in
  fill](media/image1.png){width="0.2956528871391076in"   this document. They must be collected and stored in a securely
  height="0.2956528871391076in"}                         fashion. In case of doubts on how to proceed, reach out your team
                                                         leader.
  ------------------------------------------------------ ------------------------------------------------------------------

  -------------------------------------------------------------------------------------------------------------------------

#### Boomi Connectors

  ---------------------------------------------------------------------------
  **Connected       **Connected   **Connector   **Is    **Connector Name**
  Application**     BU**          Type**        New**   
  ----------------- ------------- ------------- ------- ---------------------
  SF                GB-CG         Salesforce    No      \[SF_Connector\]

  Kafka             GB-CG         Kafka         No      \[Confluent_Kafka\]
  ---------------------------------------------------------------------------

#### Source -- Data Provider

This section captures the technical details which are required to
integrate with the target system. It includes requirements like
connection details, data format, encryption, and throughput
requirements.

System: Sitecore

Boomi REST API will be called by Sitecore to establish a connection. For
details, please refer to the API Section.

  ------------------------------------------------------------------------------------------------
  **Application/Connector                                        
  Name/FTP with Version**                                        
  ------------------------- ---------- ---------- -------------- ---------------------------------
  **Information**           **Dev**    **UAT**    **Pre-Prod**   **Production**

  Endpoint Suffix                                                 

  Authentication Type       Oauth2.0     Oauth2.0   NA             Oauth2.0

  Access Key                                                     
  ------------------------------------------------------------------------------------------------

Note: More details might be required depending on the application
involved and the Boomi connector used.

  -----------------------------------------------------------------------
  **Other Technical Requirements**                
  ----------------------------------------------- -----------------------
  Data Format Required (CSV, JSON, XML, etc.)     JSON

  Data Formatting Limitation -Any Special         NA
  Characters that Service cannot handle or need   
  transformation                                  

  Throughput Limit - Is there any limitation to   NA
  the number of records that can be processed at  
  a time                                          

  Can API get Exposed to Public Cloud             NA

  Any other Limitation                            NA 

  Any Data Encryption requirement e.g.            NA 

  Any Key or certificate Exchange required e.g.   NA
  PGP, SSL certificate                            
  -----------------------------------------------------------------------

#### Target -- Data Consumer

This section captures the technical details which are required to
integrate with the target system. It includes requirements like
connection details, data format, encryption, and throughput
requirements.

**System:** Kafka

+-------------+-------------+-------------+-------------+-------------+
| *           |             |             |             |             |
| *Applicatio |             |             |             |             |
| n/Connector |             |             |             |             |
| Name/FTP    |             |             |             |             |
| with        |             |             |             |             |
| Version**   |             |             |             |             |
+=============+=============+=============+=============+=============+
| **In        | **Dev**     | **UAT**     | *           | **P         |
| formation** |             |             | *Pre-Prod** | roduction** |
+-------------+-------------+-------------+-------------+-------------+
| Folder/File | Calor Group | Calor Group | NA          | Calor Group |
| Path/Root   | L           | L           |             | L           |
| folder      | imited/00-C | imited/00-C |             | imited/00-C |
|             | onnectionRe | onnectionRe |             | onnectionRe |
|             | sources/00- | sources/00- |             | sources/00- |
|             | Connections | Connections |             | Connections |
+-------------+-------------+-------------+-------------+-------------+
| User        | [REDACTED]       | [REDACTED]       | NA          | [REDACTED]       |
| name/Client | [REDACTED] | [REDACTED] |             | [REDACTED] |
| Principal   |             |             |             |             |
+-------------+-------------+-------------+-------------+-------------+
| Connection  | pkc         |             |   NA        | pkc         |
| String      | -lq8gm.west | pkc         |             | -lq8gm.west |
| /Broker     | europe.azur | -lq8gm.west |             | europe.azur |
| List        | e.confluent | europe.azur |             | e.confluent |
|             | .cloud:9092 | e.confluent |             | .cloud:9092 |
|             |             | .cloud:9092 |             |             |
+-------------+-------------+-------------+-------------+-------------+
| Password    | \           |             |   NA        |             |
|             | *\*\*\*\*\* | \<          |             | \<          |
|             | \*\*\*\*\*\ | Encrypted\> |             | Encrypted\> |
|             | *\*\*\*\*\* |             |             |             |
+-------------+-------------+-------------+-------------+-------------+
| Any Other   | Security    |   Security  |   NA        |   Security  |
| System      | Protocol:   | Protocol:   |             | Protocol:   |
| Specific    | SASL SSL    | SASL SSL    |             | SASL SSL    |
| Connection  |             |             |             |             |
| Details     | SASL        | SASL        |             | SASL        |
|             | Mechanism:  | Mechanism:  |             | Mechanism:  |
|             | Plain       | Plain       |             | Plain       |
|             |             |             |             |             |
|             | Polling     | Polling     |             | Polling     |
|             | Interval:   | Interval:   |             | Interval:   |
|             | 10000       | 10000       |             | 10000       |
|             |             |             |             |             |
|             | Polling     | Polling     |             | Polling     |
|             | Delay:      | Delay:      |             | Delay:      |
|             | 10000       | 10000       |             | 10000       |
+-------------+-------------+-------------+-------------+-------------+

Note: More details might be required depending on the application
involved and the Boomi connector used.

  -----------------------------------------------------------------------
  **Other Technical Requirements**                
  ----------------------------------------------- -----------------------
  Data Format Required (CSV, JSON, XML, etc.)     JSON

  Data Formatting Limitation -Any Special         NA
  Characters that Service cannot handle or need   
  transformation                                  

  Throughput Limit - Is there any limitation to   NA
  the number of records that can be processed at  
  a time                                          

  Can API get Exposed to Public Cloud             NA

  Any other Limitation                            NA

  Any Data Encryption requirement e.g.            NA 

  Any Key or certificate Exchange required e.g.   NA
  PGP, SSL certificate                            
  -----------------------------------------------------------------------

### Integration Artifacts

#### Data Profile

Oauth2 connection will follow the following (ignore curl commands)

Authentication call:

curl \--location \'<https://api-dev.shvenergy.com/auth/v1/token>\' \\

\--header \'Content-Type: application/x-www-form-urlencoded\' \\

\--data-urlencode \'grant_type=client_credentials\' \\

\--data-urlencode \'client_id=YOUR API ID HERE\' \\

\--data-urlencode \'client_secret=YOUR API KEY HERE\'

\]call with token:

curl \--location
\'<https://api-dev.shvenergy.com/gb-cg/sales-and-service-management-api/v1/leads>

\--header \'Content-Type: application/json\' \\

\--header \'Authorization: Bearer BEARER TOKEN RETURNED BY PREVIOUS
CALL\' \\

**Json Input :**

{

\"first-name\": \"Test\",

\"last-name\": \"LeadAPITesting1\",

\"phone\": \"07989480687\",

\"email\":
[[testleadapitesting1@calor.co.uk]{.underline}](mailto:testleadapitesting1@calor.co.uk),

\"postcode\": \"GL3 1DL\",

\"address-line-one\": \"Ref County Durham Dowco Hous\",

\"addional-comments\":\"Testing Lead, please ignore\",

\"form-source\":\"HE Fuel Switch Enquiry\"

\"lead-channel\": \[\"Webform\"\],

\"lead-source\": \[\"Digital\"\]

}

#### Mappings

[SUB-GB-CG-043_SiteCore_To_SF_Mapping.xlsx](https://shvenergy.sharepoint.com/:x:/r/sites/NL_HQ-ICC-IntegrationTeam/_layouts/15/Doc.aspx?sourcedoc=%7B2167FCC5-35F0-4866-BA52-6544DEEEAB45%7D&file=SUB-GB-CG-043_SiteCore_To_SF_Mapping.xlsx&action=default&mobileredirect=true&wdwpf=doclib-t)

#### Others

Provide whatever other artifacts are required within the context of this
document, either in line or include a document.

## Integration Design Specification

### Solution Architecture

The Interface Solution Architecture can be found here:

[ISA - Web to Lead Creation
Implementation.pptx](https://shvenergy.sharepoint.com/:p:/r/sites/NL_HQ-ICC-IntegrationTeam/_layouts/15/Doc.aspx?sourcedoc=%7BFB001FDF-38EE-4CD9-A541-DB121343A1AB%7D&file=ISA%20-%20Web%20to%20Lead%20Creation%20Implementation.pptx&action=edit&mobileredirect=true)

![](/media/image7.png){width="7.09375in" height="3.9791666666666665in"}

### Interface Overview

-   This is an asynchronous integration between Sitecore and Salesforce
    via Boomi. Details for the REST API to be exposed to Sitecore are
    mentioned in the API section.

-   Boomi listener process will get the JSON Template from Sitecore via
    APIM in the Request body

-   Boomi process
    \[Publisher\]-\[PUB-GB-CG-043\]-\[CreateLead-\[Customer
    Portal\]-\[GB-CG\] listens to the incoming JSON request and
    publishes it to Kafka Topic.

-   This Kafka Topic is listened to by the subscriber process
    \[Subscriber\]-\[SUB-GB-CG-043\]-\[CreateLead\]\]-\[Salesforce\]-\[GB-CG\],
    which will pass the data to SF for Lead creation.

```{=html}
<!-- -->
```
-   For any technical/process failures, Boomi process to captures the
    failures using the common framework for notification and logging
    facade for error handling.

-   With the first call API-M will generate the Authentication Token and
    by using that token API-M will call the Boomi process and pass the
    data.

  ------------------------------------------------------------------------
  **Boomi         
  Process -       
  Listener**      
  --------------- --------------------------------------------------------
  **Deployment    Boomi MCS - API / Real-Time Cluster
  Location**      

  **Account       Calorgrouplimited-3SH5SL
  Name**          

  **Boomi Folder  Calor Group Limited/02-Deployable/GB-CG/Enterprise
  Name**          Projects/Customer Portal/Publisher/PUB-GB-CG-043-leads

  **Boomi Process \[Publisher\]-\[PUB-GB-CG-043\]-\[leads\]-\[Customer
  Name**          Portal\]-\[GB-CG\]

  **Kafka Topic   **gb-cg.q.leads.in.insert**
  Name**          

  **Process       This integration is responsible for sending data to
  Description**   Salesforce for load creation.
  ------------------------------------------------------------------------

![](/media/image9.png){width="7.09375in" height="4.0625in"}

### Tracking Field

+----------------+------------------------------+----------------------+
| **Tracking     | **Profile Element**          | **Description**      |
| field**        |                              |                      |
+================+==============================+======================+
| Primarykey     | email                        | Customer email will  |
|                |                              | be passed            |
| Primary Value  | xxxxxxxx                     |                      |
+----------------+------------------------------+----------------------+

### Exception Handling

  ---------------------------------------------------------------------------
  **Exception       **001**
  Num.**            
  ----------------- ---------------------------------------------------------
  **Exception       Functional
  Type**            

  **Description**   Bad request

  **Tracking        Boomi / API tracking field for troubleshooting purposes
  Field**           

  **Error Code**    400

  **Action**        Since it is a business-related error, source/target team
                    will need to be notified

  **Remarks**       Any other comments required

  **Notification    Email address to notify, if required
  Address**         
  ---------------------------------------------------------------------------

  ---------------------------------------------------------------------------
  **Exception       **002**
  Num.**            
  ----------------- ---------------------------------------------------------
  **Exception       Technical
  Type**            

  **Description**   Unauthorized error

  **Tracking        Boomi / API tracking field for troubleshooting purposes
  Field**           

  **Error Code**    401

  **Action**        Action to be taken care

  **Remarks**       Any other comments required

  **Notification    Email address to notify, if required
  Address**         
  ---------------------------------------------------------------------------

  ---------------------------------------------------------------------------
  **Exception       **003**
  Num.**            
  ----------------- ---------------------------------------------------------
  **Exception       Technical
  Type**            

  **Description**   Description of the exception to be handled

  **Tracking        Boomi / API tracking field for troubleshooting purposes
  Field**           

  **Error Code**    500

  **Action**        Action to be taken care

  **Remarks**       Any other comments required

  **Notification    Email address to notify, if required
  Address**         
  ---------------------------------------------------------------------------

### API Design Information

  -----------------------------------------------------------------------
  ***This section must be filled in case of this specific interface being
  an API***.
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

#### API Information

This section must be filled with this specific interface being an API.
Document shows state which API Design principles and any deviation from
the principles to be used.

*Read API: Global API Principles and Standard V1.0.pdf*

+--------------------+-------------------------------------------------+
| **API Guidelines** | **Confirmation**                                |
+====================+=================================================+
| API Design         | **#01:** Primacy of the API Design Principles   |
| Principle          |                                                 |
|                    | **#02:** Identification of Enterprise APIs      |
|                    |                                                 |
|                    | **#03:** Product based approach                 |
|                    |                                                 |
|                    | **#04:** Contract first approach for Enterprise |
|                    | APIs.                                           |
|                    |                                                 |
|                    | **#05**: Functional scoping for Global APIs     |
|                    |                                                 |
|                    | **#06:** RESTful and stateless                  |
|                    |                                                 |
|                    | **#07:** Low latency for Synchronous APIs.      |
|                    |                                                 |
|                    | **#08**: Handling and intercepting of errors    |
|                    | and exceptions                                  |
|                    |                                                 |
|                    | **#09:** Three-tier API architecture**.**       |
|                    |                                                 |
|                    | **#10:** Designed for reuse                     |
|                    |                                                 |
|                    | **#11:** Secure by design                       |
+--------------------+-------------------------------------------------+
| Functional Scoping | Mixed / Composite Services / Atomic Services    |
+--------------------+-------------------------------------------------+
| Type of API        | UserAPI/BusinessAPI/SystemAPI                   |
+--------------------+-------------------------------------------------+
| Resource Path      | https:                                          |
| (Boomi)            | //\<host\>/{\<type\>}/{\<version\>}/\[\<domain\ |
|                    | >\]/\[\<businessUnit\>\]/\<collection\>/\[{id}\ |
|                    | \                                               |
|                    | \]/\<resource\>/\[{id}\]\                       |
|                    | \                                               |
|                    | h                                               |
|                    | ttps://\<host\>/\<domain\>/{\<version\>}/{\<bus |
|                    | inessUnit\>}/\<collection\>/\[{id}\]/\<resourc\ |
|                    | \                                               |
|                    | e\>/\[{id}\]\                                   |
|                    | \                                               |
|                    | htt                                             |
|                    | ps://\<host\>/{\<type\>}/\<domain\>/{\<version\ |
|                    | >}/{\<businessUnit\>}/\<collection\>/\[{id}\]/\ |
|                    | \                                               |
|                    | \<resource\>/\[{id}\]                           |
+--------------------+-------------------------------------------------+
| Resource Path      | [https://\<host\>/\<domain\>/{\<versio          |
| (APIM)             | n\>}/{\<businessUnit\>}/\<collection\>/\[{id}\] |
|                    | /\<resourc](https://<host>/<domain>/{<version>} |
|                    | /{<businessUnit>}/<collection>/[{id}]/<resourc) |
|                    |                                                 |
|                    | e\>/\[{id}\]                                    |
|                    |                                                 |
|                    | [https://\<host\>/{\<type\>}/\<domain\>/{       |
|                    | \<version\>}/{\<businessUnit\>}/\<collection\>/ |
|                    | \[{id}\]/](https://<host>/{<type>}/<domain>/{<v |
|                    | ersion>}/{<businessUnit>}/<collection>/[{id}]/) |
|                    |                                                 |
|                    | \<resource\>/\[{id}\]                           |
+--------------------+-------------------------------------------------+
| PAGINATION AND     | Yes/No                                          |
| PARTIAL RESPONSE   |                                                 |
+--------------------+-------------------------------------------------+
| Details of         |                                                 |
| PAGINATION AND     |                                                 |
| PARTIAL RESPONSE   |                                                 |
+--------------------+-------------------------------------------------+

### **API Design Sheet** {#api-design-sheet .unnumbered}

[API design
sheet_GB-CG_CaseCreate_SiteCore_to_SF_Business](https://shvenergy.sharepoint.com/sites/NL_HQ-ICC-IntegrationTeam/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FNL%5FHQ%2DICC%2DIntegrationTeam%2FShared%20Documents%2FEnterprise%20Projects%2FGB%2DCG%2FCalor%20Boost%20Project%202019%2FInterfaces%2FGeneric%5FCaseCreation%2FLow%20Level%20Design%2FIDS&viewid=5d9b27e6%2D7396%2D492d%2D990e%2D3ad8ecd3dbdb&OR=Teams%2DHL&CT=1715661741177)

###  {#section .unnumbered}

### Design Decision

Document here the exceptions to SHVE agreed with best practices and
design principles supported by the rationale for these.

  -----------------------------------------------------------------------
  **Design Decision**                 **Rationale**
  ----------------------------------- -----------------------------------
  REST API service is created and     A New REST API service URL with
  hosted In Boomi.                    POST endpoint to be created for
                                      web-to-lead creation to be called
                                      upon in Boomi as agreed with the
                                      Business.

                                      
  -----------------------------------------------------------------------

**End of section 1. Start Interface 2 in the next page.**

**End of section 1. Start Interface 2 in the next page.**
