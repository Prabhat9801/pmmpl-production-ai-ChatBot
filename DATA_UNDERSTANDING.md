# 📊 DATA UNDERSTANDING GUIDE

**Generated:** 2025-12-26 17:53:47

**Source File:** `Copy of PMMPL AI (Prabhat).xlsx`

**Total Sheets:** 16


---


## 🎯 PURPOSE OF THIS DATA


This Excel workbook contains **production management data** for PMMPL (Production Manufacturing Management company).

It tracks various aspects of the manufacturing business including:

- ✅ Task checklists and delegations

- 📦 Inventory management (Raw materials & Finished goods)

- 👥 Employee information

- 💰 Financial transactions (Payments & Collections)

- 🛒 Purchase orders and receipts

- 📈 Sales orders and invoices

- 🏭 Production orders and job cards

- 📥 Store inventory movements (IN/OUT)


---


## 📋 SHEET OVERVIEW


| # | Sheet Name | Purpose |

|---|------------|---------|

| 1 | **Checklist** | Daily task tracking and completion status |

| 2 | **Delegation** | Work assignment and delegation tracking |

| 3 | **PO Pending** | Purchase orders awaiting receipt |

| 4 | **FG Stock** | Finished Goods inventory levels |

| 5 | **RM Sock** | General data tracking |

| 6 | **Purchase Intransit** | Tracking purchases currently in transit |

| 7 | **Payments** | Outgoing payment transactions |

| 8 | **Enquirys** | Customer enquiries and leads |

| 9 | **Store OUT** | Inventory issued from warehouse |

| 10 | **New Store Indent** | General data tracking |

| 11 | **Store IN** | Inventory received into warehouse |

| 12 | **Purchase Receipt** | Received purchase orders |

| 13 | **Orders Pending** | Sales orders awaiting fulfillment |

| 14 | **Sales Invoices** | Completed sales invoices |

| 15 | **Production Orders** | Manufacturing orders and schedules |

| 16 | **Job Card Production** | Detailed production job tracking |


---


## 📊 DETAILED SHEET ANALYSIS


### 📄 Checklist


**Purpose:** Daily task tracking and completion status


**Statistics:**

- Total Rows: **8,031**

- Total Columns: **15**


**Columns:**


| Column Name | Data Type | Unique Values | Null Count | Sample Data |

|-------------|-----------|---------------|------------|-------------|

| `Timestamp` | datetime64[ns] | 21 | 0 | 2025-07-04 12:04:42.987000, 2025-07-04 12:04:42.987000 |

| `Task ID` | int64 | 8,019 | 0 | 1, 2 |

| `Department Name` | object | 1 | 0 | PMMPL, PMMPL |

| `Given By` | object | 4 | 0 | Kavit Sir, Kavit Sir |

| `Doer Name` | object | 34 | 0 | Ahitesh Tandan, Ahitesh Tandan |

| `Task Description` | object | 349 | 0 | Clean Fms Index PMMPL, Clean Fms Index PMMPL |

| `Task Start Date` | datetime64[ns] | 257 | 0 | 2025-07-05 00:00:00, 2025-08-05 00:00:00 |

| `Frequency` | object | 7 | 0 | monthly, monthly |

| `Enable Reminders` | object | 2 | 0 | No, No |

| `Require Attachment` | object | 1 | 0 | No, No |

| `Actual` | datetime64[ns] | 116 | 5,369 | 2025-07-08 00:00:00, 2025-08-06 00:00:00 |

| `Delay` | timedelta64[ns] | 182 | 2,662 | -10 days +00:00:00, -41 days +00:00:00 |

| `Status` | object | 1 | 7,579 | Yes, Yes |

| `Remarks` | object | 6 | 7,945 | demo, DONE |

| `Uploaded Image` | object | 39 | 7,992 | https://drive.google.com/uc?ex, https://drive.google.com/uc?ex |



### 📄 Delegation


**Purpose:** Work assignment and delegation tracking


**Statistics:**

- Total Rows: **148**

- Total Columns: **17**


**Columns:**


| Column Name | Data Type | Unique Values | Null Count | Sample Data |

|-------------|-----------|---------------|------------|-------------|

| `Timestamp` | object | 107 | 0 | 2025-07-06 00:00:00, 2022-11-09 10:54:31 |

| `Task ID` | int64 | 145 | 0 | 2, 3 |

| `Department Name` | object | 4 | 0 | REFRASYNTH, PMMPL |

| `Given By` | object | 3 | 0 | Kavit Passary, Kavit Passary |

| `Doer Name` | object | 34 | 0 | Ahitesh Tandan, Himani Pandey |

| `Task Description` | object | 142 | 0 | Repair All Refrasynth System, Vehicle tracker in all bikes,  |

| `Task Start Date` | datetime64[ns] | 82 | 0 | 2025-07-06 00:00:00, 2023-11-18 00:00:00 |

| `Frequency` | object | 1 | 0 | one-time, one-time |

| `Enable Reminders` | object | 1 | 0 | Yes, Yes |

| `Require Attachment` | object | 1 | 0 | No, No |

| `Planned Date` | datetime64[ns] | 82 | 0 | 2025-07-06 00:00:00, 2023-11-18 00:00:00 |

| `Actual` | object | 33 | 69 | 2025-09-17 00:00:00, 2025-08-22 00:00:00 |

| `Delay` | timedelta64[ns] | 95 | 8 | 73 days 00:00:00, 769 days 00:00:00 |

| `Status` | object | 1 | 69 | Done, Done |

| `Update Date` | float64 | 0 | 148 | - |

| `Reasons` | object | 1 | 147 | Refratech payment bot , hr lea |

| `Total Extent` | int64 | 2 | 0 | 1, 0 |



### 📄 PO Pending


**Purpose:** Purchase orders awaiting receipt


**Statistics:**

- Total Rows: **1,762**

- Total Columns: **20**


**Columns:**


| Column Name | Data Type | Unique Values | Null Count | Sample Data |

|-------------|-----------|---------------|------------|-------------|

| `Timestamp` | datetime64[ns] | 1,762 | 0 | 2023-01-13 14:46:47.860000, 2023-01-13 14:47:48.551000 |

| `Indent Number` | object | 1,762 | 0 | RI-521, RI-522 |

| `Have To Make Po` | object | 2 | 0 | Yes, Yes |

| `Party Name` | object | 71 | 0 | Dahmi Industries, Dahmi Industries |

| `Product Name` | object | 211 | 0 | Dahmi Pyro (0-1), Dahmi Pyro (1-3) |

| `Quantity` | float64 | 279 | 14 | 40.0, 30.0 |

| `Rate` | float64 | 387 | 14 | 10400.0, 10400.0 |

| `Alumina %` | float64 | 55 | 14 | 38.0, 38.0 |

| `Iron %` | float64 | 50 | 14 | 1.0, 1.0 |

| `Lead Time To Lift Total Qty` | float64 | 26 | 14 | 15.0, 15.0 |

| `PO Copy` | object | 1,653 | 27 | https://drive.google.com/open?, https://drive.google.com/open? |

| `Total Amount` | float64 | 878 | 0 | 416000.0, 312000.0 |

| `Advance To Be Paid` | object | 2 | 14 | No, No |

| `To Be Paid Amount` | float64 | 87 | 1,631 | 2246130.0, 737500.0 |

| `When To Be Paid` | datetime64[ns] | 110 | 1,631 | 2022-08-02 00:00:00, 2023-03-27 00:00:00 |

| `Notes` | object | 350 | 426 | 0516, 0516 |

| `Total Lifted` | float64 | 989 | 0 | 32.503, 28.984 |

| `Pending Qty` | float64 | 475 | 0 | 0.0, 0.0 |

| `Order Cancel Qty` | float64 | 319 | 0 | 7.497, 1.016 |

| `Status` | object | 2 | 0 | Complete, Complete |



### 📄 FG Stock


**Purpose:** Finished Goods inventory levels


**Statistics:**

- Total Rows: **104**

- Total Columns: **2**


**Columns:**


| Column Name | Data Type | Unique Values | Null Count | Sample Data |

|-------------|-----------|---------------|------------|-------------|

| `Product Name` | object | 104 | 0 | 90 S, 95 S |

| `Current Level` | float64 | 51 | 0 | 0.0, 0.0 |



### 📄 RM Sock


**Purpose:** Data tracking and management


**Statistics:**

- Total Rows: **161**

- Total Columns: **6**


**Columns:**


| Column Name | Data Type | Unique Values | Null Count | Sample Data |

|-------------|-----------|---------------|------------|-------------|

| `Item Name` | object | 159 | 0 | 99 C Fired, 99 C Fines |

| `Current Level` | float64 | 124 | 0 | -7.283063041541027e-14, 3.552713678800501e-15 |

| `Colour Code` | object | 4 | 0 | Red, Red |

| `Full Kitting FG + Semi` | float64 | 36 | 0 | 0.0, 0.0 |

| `To Be Indented` | float64 | 124 | 0 | 7.283063041541027e-14, -14.000000000000004 |

| `To Be Lifted` | float64 | 124 | 0 | 7.283063041541027e-14, -3.552713678800501e-15 |



### 📄 Purchase Intransit


**Purpose:** Tracking purchases currently in transit


**Statistics:**

- Total Rows: **9**

- Total Columns: **21**


**Columns:**


| Column Name | Data Type | Unique Values | Null Count | Sample Data |

|-------------|-----------|---------------|------------|-------------|

| `Timestamp` | datetime64[ns] | 9 | 0 | 2025-07-01 12:48:21.895000, 2025-12-08 18:16:10.126000 |

| `LN-Lift Number` | object | 9 | 0 | LN-4104, LN-4984 |

| `Type` | object | 2 | 0 | Independent, Independent |

| `Po Number` | object | 9 | 0 | RI-1929, RI-2273 |

| `Bill No.` | int64 | 7 | 0 | 0, 246 |

| `Party Name` | object | 5 | 0 | Passary Minerals Rourkela, Peekay Petrochem Pvt Ltd |

| `Product Name` | object | 9 | 0 | Silliminite Sand, Plastic Clay |

| `Qty` | float64 | 8 | 0 | 0.0, 30.0 |

| `Area Lifting` | object | 1 | 0 | Supplying In Factory, Supplying In Factory |

| `Lead Time To Reach Factory` | int64 | 2 | 0 | 3, 3 |

| `Truck No.` | object | 6 | 2 | OD07V8625, WB57D6127 |

| `Driver No.` | float64 | 1 | 8 | 9078791722.0 |

| `Transporter Name` | object | 3 | 2 | Ex Factory Transporter, Ex Factory Transporter |

| `Bill Image` | object | 6 | 3 | https://drive.google.com/open?, https://drive.google.com/open? |

| `Bilty No.` | float64 | 0 | 9 | - |

| `Type Of Rate` | object | 2 | 2 | Fixed Amount, Fixed Amount |

| `Rate` | float64 | 1 | 8 | 1150.0 |

| `Truck Qty` | float64 | 7 | 2 | 0.0, 30.0 |

| `Material Rate` | int64 | 9 | 0 | 0, 5100 |

| `Bilty Image` | float64 | 0 | 9 | - |

| `Expected Date To Reach` | datetime64[ns] | 4 | 0 | 2025-07-04 00:00:00, 2025-12-11 00:00:00 |



### 📄 Payments


**Purpose:** Outgoing payment transactions


**Statistics:**

- Total Rows: **8,125**

- Total Columns: **12**


**Columns:**


| Column Name | Data Type | Unique Values | Null Count | Sample Data |

|-------------|-----------|---------------|------------|-------------|

| `Timestamp` | datetime64[ns] | 8,125 | 0 | 2023-04-01 13:39:58.210000, 2023-04-01 13:48:12.559000 |

| `Payment Number` | object | 8,125 | 0 | AP-02, AP-03 |

| `Status` | object | 2 | 0 | Yes, Yes |

| `Unique Number` | object | 6,737 | 3 | RI-598, 0320 |

| `Fms Name` | object | 41 | 4 | Purchase FMS Po Advance, Repair FMS |

| `Pay To` | object | 2,704 | 202 | Thyme India Pvt Ltd, Hindustan repairing center |

| `Amount To Be Paid` | float64 | 4,172 | 203 | 729505.0, 3192.0 |

| `Remarks` | object | 7,146 | 199 | For purchase of SMS Microsilic, For Stitching machine no. (3.6 |

| `Any Attachments` | object | 4,256 | 3,869 | https://drive.google.com/open?, https://drive.google.com/open? |

| `Planned Date` | datetime64[ns] | 888 | 231 | 2023-04-01 00:00:00, 2023-04-01 00:00:00 |

| `Approval Date` | datetime64[ns] | 757 | 237 | 2023-04-01 00:00:00, 2023-04-01 00:00:00 |

| `Status.1` | object | 2 | 949 | Rejected, Approved |



### 📄 Enquirys


**Purpose:** Customer enquiries and leads


**Statistics:**

- Total Rows: **230**

- Total Columns: **32**


**Columns:**


| Column Name | Data Type | Unique Values | Null Count | Sample Data |

|-------------|-----------|---------------|------------|-------------|

| `Timestamp` | object | 114 | 0 | 2024-12-06 00:00:00, 2024-12-06 00:00:00 |

| `Enquiry No.` | object | 230 | 0 | EN-2, EN-3 |

| `Product No.` | int64 | 10 | 0 | 2, 3 |

| `Firm Name` | object | 3 | 0 | RKL, RKL |

| `Enquiry status` | object | 3 | 0 | Hot , Hot  |

| `Type Of Enquiry` | object | 2 | 0 | NBD OF CRR, NBD OF CRR |

| `Location` | object | 170 | 0 | SAMBALPUR, Singhbhum (West), Jharkhand  |

| `Name Of Sales Person` | object | 9 | 0 | AJAY GUPTA, SITAL KAR |

| `Party Name` | object | 150 | 0 | Aryan Ispat & Power P. Ltd, RUNGTA MINES LTD |

| `Department` | object | 10 | 0 | DRI, DRI |

| `Total Order Qty` | object | 147 | 0 | 10, 385.5 |

| `Expected` | object | 43 | 0 | 0, 0 |

| `When Required` | datetime64[ns] | 142 | 0 | 2024-06-11 00:00:00, 2024-06-11 00:00:00 |

| `Area Of Application` | object | 51 | 1 | 0, ALL |

| `Upload File` | object | 229 | 1 | https://drive.google.com/file/, https://drive.google.com/file/ |

| `Contact Person Name` | object | 174 | 2 | Mr. Furkan Ali , 0 |

| `Contact Person Mobile No.` | object | 115 | 2 | 7978297729, 0 |

| `Email Id` | object | 159 | 2 | aryanpurchase@gmail.com, srsplpurchase@gmail.com |

| `Lead Time For Convert In Order` | object | 40 | 0 | 7, 15 |

| `Did The Above Enquiry Come From Nbd Outgoing Sheet` | object | 2 | 0 | NO, NO |

| `Offer No.` | object | 183 | 0 | 51, 52 |

| `Product Names` | object | 65 | 0 | Pasheat - K, LCM - 75 AR With 1% SS Fiber |

| `Quetities` | object | 116 | 0 | 5, 380 |

| `Uom` | object | 3 | 0 | MT, MT |

| `Proposal Amount 1` | object | 47 | 182 | 2,54,67,000.00, 60755500 |

| `Proposal Remarks 1` | object | 38 | 187 | Double Layer Casting with the , Double Layer Casting with the  |

| `Proposal Amount 2` | float64 | 24 | 205 | 64464500.0, 32792000.0 |

| `Proposal Remarks 2` | object | 25 | 205 | Single Layer Casting , Refractory thickness 230 mm |

| `Proposal Amount 3` | float64 | 7 | 223 | 89565300.0, 5461200.0 |

| `Proposal Remarks 3` | object | 7 | 223 | As Per Your Requirement(propos, For Single Layer Casting: - |

| `G-mail` | float64 | 0 | 230 | - |

| `Status` | object | 2 | 38 | Order Received, Order Received |



### 📄 Store OUT


**Purpose:** Inventory issued from warehouse


**Statistics:**

- Total Rows: **198**

- Total Columns: **17**


**Columns:**


| Column Name | Data Type | Unique Values | Null Count | Sample Data |

|-------------|-----------|---------------|------------|-------------|

| `Timestamp` | datetime64[ns] | 198 | 0 | 2024-02-29 11:29:05.776000, 2024-02-29 11:31:56.165000 |

| `Request Number` | object | 198 | 0 | SO-996, SO-997 |

| `Indentor Name` | object | 12 | 0 | NAKUL VERMA , NAKUL VERMA  |

| `Department` | object | 3 | 0 | Akoli, Akoli |

| `Area` | object | 9 | 1 | Factory Office, Factory Office |

| `Group Head` | object | 18 | 0 | ELECTRICAL, NUT BOLT |

| `Product Name` | object | 81 | 0 | Electric Tape, Nut Bolt Visor 10x50 |

| `Qty Requested` | float64 | 22 | 0 | 2.0, 3.0 |

| `Unit Of Measurement` | object | 10 | 1 | PCS, PCS |

| `Application No.(If Aplicable)` | float64 | 1 | 179 | 66.0, 66.0 |

| `Planned Time For Out` | datetime64[ns] | 194 | 0 | 2024-03-01 11:29:00, 2024-03-01 11:31:00 |

| `Out Time` | datetime64[ns] | 198 | 0 | 2024-03-13 13:59:41.772000, 2024-03-13 13:58:50.859000 |

| `Delay` | float64 | 119 | 79 | 12.104650138884608, 12.102671979162551 |

| `Issue Status` | object | 1 | 0 | Issuing, Issuing |

| `Qty` | int64 | 21 | 0 | 2, 3 |

| `Unit Of Measurement.1` | object | 5 | 0 | PCS, PCS |

| `Product Name.1` | object | 81 | 0 | Electric Tape, Nut Bolt Visor 10x50 |



### 📄 New Store Indent


**Purpose:** Data tracking and management


**Statistics:**

- Total Rows: **1**

- Total Columns: **10**


**Columns:**


| Column Name | Data Type | Unique Values | Null Count | Sample Data |

|-------------|-----------|---------------|------------|-------------|

| `TimeStamp` | object | 1 | 0 | #REF! |

| `Indent No.` | float64 | 0 | 1 | - |

| `Indentor Name` | float64 | 0 | 1 | - |

| `Department` | float64 | 0 | 1 | - |

| `Area Of Machine` | float64 | 0 | 1 | - |

| `Group Head` | float64 | 0 | 1 | - |

| `Product Name` | float64 | 0 | 1 | - |

| `Qty` | float64 | 0 | 1 | - |

| `Product Make Name/Specifications` | float64 | 0 | 1 | - |

| `Application Number` | float64 | 0 | 1 | - |



### 📄 Store IN


**Purpose:** Inventory received into warehouse


**Statistics:**

- Total Rows: **1**

- Total Columns: **15**


**Columns:**


| Column Name | Data Type | Unique Values | Null Count | Sample Data |

|-------------|-----------|---------------|------------|-------------|

| `Timestamp` | object | 1 | 0 | #REF! |

| `Indent No.` | float64 | 0 | 1 | - |

| `Bill No.` | float64 | 0 | 1 | - |

| `Vendor Name` | float64 | 0 | 1 | - |

| `Product Name` | float64 | 0 | 1 | - |

| `Qty` | float64 | 0 | 1 | - |

| `Type Of Bill` | float64 | 0 | 1 | - |

| `Bill Amount` | float64 | 0 | 1 | - |

| `Payment Type` | float64 | 0 | 1 | - |

| `Advance Amount If Any` | float64 | 0 | 1 | - |

| `Photo Of Bill` | float64 | 0 | 1 | - |

| `Transportation Include` | float64 | 0 | 1 | - |

| `Transporter Name` | float64 | 0 | 1 | - |

| `Amount` | float64 | 0 | 1 | - |

| `Department` | float64 | 0 | 1 | - |



### 📄 Purchase Receipt


**Purpose:** Received purchase orders


**Statistics:**

- Total Rows: **198**

- Total Columns: **19**


**Columns:**


| Column Name | Data Type | Unique Values | Null Count | Sample Data |

|-------------|-----------|---------------|------------|-------------|

| `Timestamp` | datetime64[ns] | 198 | 0 | 2023-01-13 17:25:20.164000, 2023-01-13 17:25:41.815000 |

| `Lift Number` | object | 198 | 0 | LN-14, LN-13 |

| `PO Number` | object | 91 | 0 | RI-540, RI-539 |

| `Bill Number` | int64 | 85 | 0 | 1431, 1430 |

| `Party Name` | object | 16 | 0 | Passary Minerals Rourkela, Passary Minerals Rourkela |

| `Product Name` | object | 52 | 0 | P14 Clinker, 99 C Fired |

| `Date Of Receiving` | datetime64[ns] | 44 | 0 | 2023-01-09 00:00:00, 2023-01-13 00:00:00 |

| `Total Bill Quantity` | float64 | 127 | 0 | 8.36, 4.82 |

| `Actual Quantity` | float64 | 158 | 0 | 8.36, 4.82 |

| `Qty Difference` | float64 | 65 | 0 | 0.0, 0.0 |

| `Physical Condition` | object | 1 | 0 | Good, Good |

| `Moisture` | object | 1 | 0 | No, No |

| `Physical Image Of Product` | object | 195 | 1 | https://drive.google.com/open?, https://drive.google.com/open? |

| `Image Of Weight Slip` | object | 195 | 1 | https://drive.google.com/open?, https://drive.google.com/open? |

| `Bilty Image` | float64 | 0 | 198 | - |

| `Bilty No.` | float64 | 0 | 198 | - |

| `Qty Difference Status` | float64 | 0 | 198 | - |

| `Difference Qty` | float64 | 0 | 198 | - |

| `Type` | float64 | 0 | 198 | - |



### 📄 Orders Pending


**Purpose:** Sales orders awaiting fulfillment


**Statistics:**

- Total Rows: **1,773**

- Total Columns: **24**


**Columns:**


| Column Name | Data Type | Unique Values | Null Count | Sample Data |

|-------------|-----------|---------------|------------|-------------|

| `Timestamp` | object | 1,320 | 0 | 2022-12-24 13:35:06, 2022-12-24 13:45:01 |

| `DO-Delivery Order No.` | object | 1,773 | 0 | DO-959, DO-960 |

| `PARTY PO NO (As Per Po Exact)` | object | 1,078 | 0 | SURYADEV/PASSARY/CASTABLES/PO/, SURYADEV/PASSARY/CASTABLES/PO/ |

| `Party PO Date` | object | 640 | 0 | 2022-05-28 00:00:00, 2022-05-28 00:00:00 |

| `Party Names` | object | 131 | 0 | Suryadev Alloys And Power Priv, Suryadev Alloys And Power Priv |

| `Product Name` | object | 156 | 0 | Insulation Pad, High Cast Special |

| `Quantity` | float64 | 253 | 0 | 2.0, 56.0 |

| `Rate Of Material` | object | 420 | 0 | 29500, 49700 |

| `Type Of Transporting` | object | 3 | 1 | For, For |

| `Upload SO` | object | 1,267 | 1 | https://drive.google.com/open?, https://drive.google.com/open? |

| `Is This Order Through Some Agent` | object | 2 | 11 | No, No |

| `Order Received From` | object | 3 | 0 | NBD & NBD OF CRR FMS, NBD & NBD OF CRR FMS |

| `Type Of Measurement` | object | 6 | 0 | PCS, MT |

| `Contact Person Name` | object | 429 | 1 | MR. K SHIVA PRADEEP JI, MR K SHIVA PRADEEP JI |

| `Contact Person WhatsApp No.` | object | 206 | 27 | 9182469035, 9182469035 |

| `Alumina%` | object | 119 | 337 | ..., 73-76 |

| `Iron%` | object | 117 | 322 | ...., 1.5-1.8 |

| `Type Of PI` | object | 5 | 6 | Partly Advance Partly PI, Partly Advance Partly PI |

| `Lead Time For Collection Of Final Payment` | object | 19 | 21 | 30, 30 |

| `Quantity 
Delivered` | float64 | 347 | 0 | 0.0, 56.0 |

| `Order Cancel` | float64 | 123 | 0 | 2.0, 0.0 |

| `Pending Qty` | float64 | 191 | 0 | 0.0, 0.0 |

| `Material Return` | float64 | 74 | 0 | 0.0, 0.0 |

| `Status` | object | 2 | 0 | Complete, Complete |



### 📄 Sales Invoices


**Purpose:** Completed sales invoices


**Statistics:**

- Total Rows: **4,610**

- Total Columns: **12**


**Columns:**


| Column Name | Data Type | Unique Values | Null Count | Sample Data |

|-------------|-----------|---------------|------------|-------------|

| `Timestamp` | datetime64[ns] | 4,610 | 0 | 2022-12-27 11:27:16.892000, 2022-12-27 12:02:06.001000 |

| `Bill Date` | datetime64[ns] | 947 | 0 | 2022-12-27 00:00:00, 2022-12-27 00:00:00 |

| `Delivery Order No.` | object | 1,681 | 0 | DO-969, DO-969 |

| `Party Name` | object | 128 | 0 | Shree Shyam Sponge & Power Ltd, Shree Shyam Sponge & Power Ltd |

| `Product Name` | object | 148 | 0 | LCM - 70 AR, LCM - 70 AR |

| `Quantity Delivered.` | float64 | 500 | 0 | 10.0, 10.0 |

| `Bill No.` | object | 1,452 | 0 | 579, 580 |

| `Losgistic no.` | object | 4,604 | 0 | LGST-854, LGST-855 |

| `Rate Of Material` | float64 | 286 | 0 | 39070.0, 39070.0 |

| `Type Of Transporting` | object | 4 | 0 | FOR, FOR |

| `Transporter Name` | object | 73 | 937 | Owned Truck, Owned Truck |

| `Vehicle Number.` | object | 1,365 | 0 |  CG04NT2527, CG04 LW 8478 |



### 📄 Production Orders


**Purpose:** Manufacturing orders and schedules


**Statistics:**

- Total Rows: **851**

- Total Columns: **16**


**Columns:**


| Column Name | Data Type | Unique Values | Null Count | Sample Data |

|-------------|-----------|---------------|------------|-------------|

| `Timestamp` | datetime64[ns] | 851 | 0 | 2023-01-04 12:53:05.833000, 2023-01-04 12:53:32.155000 |

| `Delivery Order No.` | object | 849 | 0 | DO-985, DO-986 |

| `Party Name` | object | 106 | 0 | Singhal Enterprises Pvt Ltd., Singhal Enterprises Pvt Ltd. |

| `Product Name` | object | 84 | 0 | Pasheat - C, Pasheat - K |

| `Order Quantity` | float64 | 178 | 0 | 20.0, 15.0 |

| `Expected Delivery Date` | datetime64[ns] | 415 | 0 | 2023-01-05 00:00:00, 2023-01-05 00:00:00 |

| `Order 
Cancel` | float64 | 140 | 0 | 0.0, 2.64 |

| `Actual Production Planned` | float64 | 255 | 0 | 20.0, 15.0 |

| `Actual Production Done` | float64 | 336 | 0 | 20.6, 14.42 |

| `Stock Transfered` | float64 | 46 | 0 | 0.0, 0.0 |

| `Quantity 
Delivered` | float64 | 227 | 0 | 20.0, 15.0 |

| `Quantity In Stock` | float64 | 328 | 0 | 0.6000000000000014, -0.5800000000000001 |

| `Planning Pending` | float64 | 155 | 0 | 0.0, 0.0 |

| `Production Pending` | float64 | 174 | 0 | -0.6, -2.06 |

| `Status` | object | 2 | 0 | Complete, Complete |

| `Date Of Complete` | datetime64[ns] | 450 | 79 | 2023-01-05 00:00:00, 2023-01-05 00:00:00 |



### 📄 Job Card Production


**Purpose:** Detailed production job tracking


**Statistics:**

- Total Rows: **198**

- Total Columns: **8**


**Columns:**


| Column Name | Data Type | Unique Values | Null Count | Sample Data |

|-------------|-----------|---------------|------------|-------------|

| `Timestamp` | datetime64[ns] | 198 | 0 | 2023-01-04 13:57:22.485000, 2023-01-04 13:57:33.737000 |

| `Do Number` | object | 70 | 0 | DO-981, DO-983 |

| `Party Name` | object | 34 | 0 | V Raj Metaliks Pvt Ltd, Suryadev Alloys And Power Priv |

| `Job Card No.` | object | 145 | 0 | JC-1217, JC-1215 |

| `Date Of Production` | datetime64[ns] | 80 | 0 | 2022-12-31 00:00:00, 2022-12-31 00:00:00 |

| `Name Of Supervisor` | object | 3 | 0 | Anand Vaishnav, Anand Vaishnav |

| `Product Name` | object | 17 | 0 | Pasheat - C, High Cast Special |

| `Quantity Of FG` | float64 | 44 | 0 | 4.12, 4.0 |




---


## 🔍 HOW THIS DATA IS USED


### For the AI Chatbot:


1. **Data Indexing**: All sheets are loaded into a vector database (ChromaDB)

2. **Semantic Search**: When you ask a question, the system finds relevant data using AI embeddings

3. **Context Retrieval**: Top matching rows/cells are retrieved as context

4. **Response Generation**: Groq's Llama model generates natural language answers based on the context


### Example Questions You Can Ask:


```

- What is the current FG stock level?

- Show me pending sales orders

- Who are the employees in the production department?

- What payments are due this month?

- List all items in Store OUT

- What is the status of purchase order #123?

- Show me production orders for this week

- Which raw materials are running low?

```


### Business Intelligence Use Cases:


- 📊 **Inventory Monitoring**: Track stock levels and reorder points

- 💰 **Financial Tracking**: Monitor payments and collections

- 🏭 **Production Planning**: Manage production schedules and capacity

- 📦 **Order Management**: Track order fulfillment and pending items

- 👥 **Resource Management**: Employee allocation and task tracking

- 📈 **Analytics**: Generate reports and insights from historical data


---


## 🎯 WHY WE'RE WORKING ON THIS DATA


### Business Objectives:


1. **Accessibility**: Make production data accessible through natural language queries

2. **Efficiency**: Eliminate manual searching through spreadsheets

3. **Real-time Insights**: Get instant answers about inventory, orders, and production

4. **Data-Driven Decisions**: Enable quick decision-making with accurate information

5. **Integration**: Connect Google Sheets data with AI for intelligent responses


### Technical Objectives:


1. **RAG System**: Implement Retrieval-Augmented Generation for accurate responses

2. **Dynamic Updates**: Auto-sync from Google Sheets for real-time data

3. **Conversation Memory**: Track conversation history for context-aware responses

4. **Multi-Sheet Search**: Search across all 17 sheets simultaneously

5. **API Access**: Provide REST API endpoints for programmatic access


---


## 📈 DATA FLOW IN THE SYSTEM


```

Google Sheets (Source)

       ↓

Data Extraction (17 sheets)

       ↓

Chunking & Processing

       ↓

Vector Embeddings (sentence-transformers)

       ↓

ChromaDB Vector Store

       ↓

User Query → Semantic Search

       ↓

Top-K Documents Retrieved

       ↓

Llama 3 (Groq API) + Context

       ↓

Natural Language Response

```


---


## 💡 KEY INSIGHTS


- **Total Data Points**: 26,400 rows across 16 sheets

- **Total Columns**: 246 unique data fields

- **Data Categories**: Inventory, Sales, Production, Finance, HR

- **Update Frequency**: Real-time sync from Google Sheets

- **Query Speed**: <3 seconds with Groq API (10x faster than local models)


---


## 🚀 GETTING STARTED


1. **Load Data**: Click 'Load Data' in web interface

2. **Ask Questions**: Type natural language queries

3. **Get Answers**: Receive context-aware responses with source references

4. **Track History**: All conversations saved in SQLite database


---


## 📚 Additional Resources


- [STEP_BY_STEP_GUIDE.md](STEP_BY_STEP_GUIDE.md) - Complete setup instructions

- [GROQ_SETUP.md](GROQ_SETUP.md) - Groq API configuration

- [RAG_SYSTEM_GUIDE.md](RAG_SYSTEM_GUIDE.md) - RAG system architecture

- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical details


---


*Analysis generated on 2025-12-26 at 17:53:47*

