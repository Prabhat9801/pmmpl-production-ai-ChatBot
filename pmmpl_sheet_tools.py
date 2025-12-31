"""
PMMPL Production Management Data Tools
========================================

This module contains 16 specialized tools for accessing and querying data from
PMMPL's (Production Manufacturing Management) Excel workbook. Each tool corresponds
to a specific sheet and provides detailed information about its structure, purpose,
and data contents.

Source: Copy of PMMPL AI (Prabhat).xlsx
Total Sheets: 16
Data Points: 26,400+ rows across all sheets
Last Updated: 2025-12-26

Usage:
    from pmmpl_sheet_tools import ChecklistTool, DelegationTool, etc.
    
    # Example
    checklist = ChecklistTool()
    print(checklist.get_info())
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ColumnInfo:
    """Represents information about a single column in a sheet."""
    name: str
    data_type: str
    unique_values: int
    null_count: int
    sample_data: List[str]
    description: str


class BaseSheetTool:
    """Base class for all sheet tools with common functionality."""
    
    def __init__(self):
        self.sheet_name: str = ""
        self.purpose: str = ""
        self.total_rows: int = 0
        self.total_columns: int = 0
        self.columns: List[ColumnInfo] = []
    
    def get_info(self) -> Dict[str, Any]:
        """Returns complete information about the sheet."""
        return {
            "sheet_name": self.sheet_name,
            "purpose": self.purpose,
            "statistics": {
                "total_rows": self.total_rows,
                "total_columns": self.total_columns
            },
            "columns": [
                {
                    "name": col.name,
                    "type": col.data_type,
                    "unique_values": col.unique_values,
                    "null_count": col.null_count,
                    "description": col.description
                }
                for col in self.columns
            ]
        }
    
    def get_column_names(self) -> List[str]:
        """Returns list of all column names."""
        return [col.name for col in self.columns]
    
    def get_column_info(self, column_name: str) -> Optional[Dict[str, Any]]:
        """Returns detailed information about a specific column."""
        for col in self.columns:
            if col.name == column_name:
                return {
                    "name": col.name,
                    "data_type": col.data_type,
                    "unique_values": col.unique_values,
                    "null_count": col.null_count,
                    "sample_data": col.sample_data,
                    "description": col.description
                }
        return None


class ChecklistTool(BaseSheetTool):
    """
    Checklist Sheet Tool - Daily Task Tracking System
    ==================================================
    
    Purpose:
        Manages daily task tracking and completion status for PMMPL operations.
        Tracks task assignments, deadlines, completion dates, delays, and attachments.
    
    Key Features:
        - Task ID tracking with unique identifiers
        - Department-wise task organization
        - Task assignment tracking (Given By -> Doer Name)
        - Frequency management (daily, weekly, monthly, etc.)
        - Reminder system with enable/disable option
        - Attachment requirement tracking
        - Delay calculation and monitoring
        - Status tracking with remarks
        - Image upload capability for task completion proof
    
    Business Use Cases:
        - Monitor task completion rates
        - Track employee performance and workload
        - Identify bottlenecks and delays
        - Ensure compliance with task deadlines
        - Generate productivity reports
        - Maintain audit trail of completed tasks
    
    Statistics:
        - Total Rows: 8,031
        - Total Columns: 15
        - Unique Tasks: 8,019
        - Unique Doers: 34
        - Frequency Types: 7 (daily, weekly, monthly, etc.)
    
    Data Quality:
        - Actual completion date missing: 5,369 rows (66.8%)
        - Delay information missing: 2,662 rows (33.2%)
        - Status populated: 452 rows (5.6%)
        - Remarks available: 86 rows (1.1%)
        - Images uploaded: 39 rows (0.5%)
    """
    
    def __init__(self):
        super().__init__()
        self.sheet_name = "Checklist"
        self.purpose = "Daily task tracking and completion status"
        self.total_rows = 8031
        self.total_columns = 15
        
        self.columns = [
            ColumnInfo(
                name="Timestamp",
                data_type="datetime64[ns]",
                unique_values=21,
                null_count=0,
                sample_data=["2025-07-04 12:04:42.987000", "2025-07-04 12:04:42.987000"],
                description="Date and time when the task record was created in the system"
            ),
            ColumnInfo(
                name="Task ID",
                data_type="int64",
                unique_values=8019,
                null_count=0,
                sample_data=["1", "2"],
                description="Unique identifier for each task in the system"
            ),
            ColumnInfo(
                name="Department Name",
                data_type="object",
                unique_values=1,
                null_count=0,
                sample_data=["PMMPL", "PMMPL"],
                description="Department responsible for the task (currently all PMMPL)"
            ),
            ColumnInfo(
                name="Given By",
                data_type="object",
                unique_values=4,
                null_count=0,
                sample_data=["Kavit Sir", "Kavit Sir"],
                description="Name of the person who assigned/created the task"
            ),
            ColumnInfo(
                name="Doer Name",
                data_type="object",
                unique_values=34,
                null_count=0,
                sample_data=["Ahitesh Tandan", "Ahitesh Tandan"],
                description="Name of the employee assigned to complete the task"
            ),
            ColumnInfo(
                name="Task Description",
                data_type="object",
                unique_values=349,
                null_count=0,
                sample_data=["Clean Fms Index PMMPL", "Clean Fms Index PMMPL"],
                description="Detailed description of the task to be performed"
            ),
            ColumnInfo(
                name="Task Start Date",
                data_type="datetime64[ns]",
                unique_values=257,
                null_count=0,
                sample_data=["2025-07-05 00:00:00", "2025-08-05 00:00:00"],
                description="Date when the task is scheduled to start"
            ),
            ColumnInfo(
                name="Frequency",
                data_type="object",
                unique_values=7,
                null_count=0,
                sample_data=["monthly", "monthly"],
                description="How often the task repeats (daily, weekly, monthly, quarterly, yearly, one-time)"
            ),
            ColumnInfo(
                name="Enable Reminders",
                data_type="object",
                unique_values=2,
                null_count=0,
                sample_data=["No", "No"],
                description="Whether automatic reminders are enabled for this task (Yes/No)"
            ),
            ColumnInfo(
                name="Require Attachment",
                data_type="object",
                unique_values=1,
                null_count=0,
                sample_data=["No", "No"],
                description="Whether task completion requires an attachment/proof (Yes/No)"
            ),
            ColumnInfo(
                name="Actual",
                data_type="datetime64[ns]",
                unique_values=116,
                null_count=5369,
                sample_data=["2025-07-08 00:00:00", "2025-08-06 00:00:00"],
                description="Actual date when the task was completed"
            ),
            ColumnInfo(
                name="Delay",
                data_type="timedelta64[ns]",
                unique_values=182,
                null_count=2662,
                sample_data=["-10 days +00:00:00", "-41 days +00:00:00"],
                description="Time difference between planned and actual completion (negative means early, positive means late)"
            ),
            ColumnInfo(
                name="Status",
                data_type="object",
                unique_values=1,
                null_count=7579,
                sample_data=["Yes", "Yes"],
                description="Current status of task completion (Yes/No/Pending)"
            ),
            ColumnInfo(
                name="Remarks",
                data_type="object",
                unique_values=6,
                null_count=7945,
                sample_data=["demo", "DONE"],
                description="Additional comments or notes about task completion"
            ),
            ColumnInfo(
                name="Uploaded Image",
                data_type="object",
                unique_values=39,
                null_count=7992,
                sample_data=["https://drive.google.com/uc?ex", "https://drive.google.com/uc?ex"],
                description="Google Drive link to uploaded proof/image of task completion"
            )
        ]


class DelegationTool(BaseSheetTool):
    """
    Delegation Sheet Tool - Work Assignment Tracker
    ================================================
    
    Purpose:
        Manages work delegation and assignment tracking across departments.
        Tracks one-time tasks with planned dates, actual completion, and delays.
    
    Key Features:
        - Task delegation from manager to employees
        - One-time task management (non-recurring)
        - Planned vs Actual completion tracking
        - Delay calculation and monitoring
        - Status tracking (Done/Pending)
        - Reminder system
        - Extension tracking for delayed tasks
        - Reason tracking for delays
    
    Business Use Cases:
        - Monitor delegation effectiveness
        - Track special project assignments
        - Analyze task completion patterns
        - Identify bottlenecks in specific departments
        - Measure employee performance on delegated tasks
        - Audit trail for management decisions
    
    Statistics:
        - Total Rows: 148
        - Total Columns: 17
        - Unique Tasks: 145
        - Departments: 4 (REFRASYNTH, PMMPL, etc.)
        - Assigned Employees: 34
        - Tasks Completed: 79 (53.4%)
        - Tasks Pending: 69 (46.6%)
    
    Data Quality:
        - Planned dates: 100% populated
        - Actual completion: 53.4% completed
        - Delay tracking: 94.6% calculated
        - Reasons provided: 1 entry only
    """
    
    def __init__(self):
        super().__init__()
        self.sheet_name = "Delegation"
        self.purpose = "Work assignment and delegation tracking"
        self.total_rows = 148
        self.total_columns = 17
        
        self.columns = [
            ColumnInfo(
                name="Timestamp",
                data_type="object",
                unique_values=107,
                null_count=0,
                sample_data=["2025-07-06 00:00:00", "2022-11-09 10:54:31"],
                description="Date and time when the delegation was recorded"
            ),
            ColumnInfo(
                name="Task ID",
                data_type="int64",
                unique_values=145,
                null_count=0,
                sample_data=["2", "3"],
                description="Unique identifier for each delegated task"
            ),
            ColumnInfo(
                name="Department Name",
                data_type="object",
                unique_values=4,
                null_count=0,
                sample_data=["REFRASYNTH", "PMMPL"],
                description="Department to which the task is delegated"
            ),
            ColumnInfo(
                name="Given By",
                data_type="object",
                unique_values=3,
                null_count=0,
                sample_data=["Kavit Passary", "Kavit Passary"],
                description="Manager or supervisor who delegated the task"
            ),
            ColumnInfo(
                name="Doer Name",
                data_type="object",
                unique_values=34,
                null_count=0,
                sample_data=["Ahitesh Tandan", "Himani Pandey"],
                description="Employee assigned to complete the delegated task"
            ),
            ColumnInfo(
                name="Task Description",
                data_type="object",
                unique_values=142,
                null_count=0,
                sample_data=["Repair All Refrasynth System", "Vehicle tracker in all bikes"],
                description="Detailed description of the delegated task"
            ),
            ColumnInfo(
                name="Task Start Date",
                data_type="datetime64[ns]",
                unique_values=82,
                null_count=0,
                sample_data=["2025-07-06 00:00:00", "2023-11-18 00:00:00"],
                description="Date when the delegated task should begin"
            ),
            ColumnInfo(
                name="Frequency",
                data_type="object",
                unique_values=1,
                null_count=0,
                sample_data=["one-time", "one-time"],
                description="Task frequency - all delegations are one-time tasks"
            ),
            ColumnInfo(
                name="Enable Reminders",
                data_type="object",
                unique_values=1,
                null_count=0,
                sample_data=["Yes", "Yes"],
                description="Reminder system enabled for all delegated tasks"
            ),
            ColumnInfo(
                name="Require Attachment",
                data_type="object",
                unique_values=1,
                null_count=0,
                sample_data=["No", "No"],
                description="Whether completion proof is required"
            ),
            ColumnInfo(
                name="Planned Date",
                data_type="datetime64[ns]",
                unique_values=82,
                null_count=0,
                sample_data=["2025-07-06 00:00:00", "2023-11-18 00:00:00"],
                description="Target completion date for the delegated task"
            ),
            ColumnInfo(
                name="Actual",
                data_type="object",
                unique_values=33,
                null_count=69,
                sample_data=["2025-09-17 00:00:00", "2025-08-22 00:00:00"],
                description="Actual date when the task was completed"
            ),
            ColumnInfo(
                name="Delay",
                data_type="timedelta64[ns]",
                unique_values=95,
                null_count=8,
                sample_data=["73 days 00:00:00", "769 days 00:00:00"],
                description="Number of days delayed from planned date"
            ),
            ColumnInfo(
                name="Status",
                data_type="object",
                unique_values=1,
                null_count=69,
                sample_data=["Done", "Done"],
                description="Completion status of the delegated task"
            ),
            ColumnInfo(
                name="Update Date",
                data_type="float64",
                unique_values=0,
                null_count=148,
                sample_data=["-", "-"],
                description="Date when status was last updated (currently unused)"
            ),
            ColumnInfo(
                name="Reasons",
                data_type="object",
                unique_values=1,
                null_count=147,
                sample_data=["Refratech payment bot, hr lea"],
                description="Reasons for delays or issues in task completion"
            ),
            ColumnInfo(
                name="Total Extent",
                data_type="int64",
                unique_values=2,
                null_count=0,
                sample_data=["1", "0"],
                description="Number of extensions granted for the task"
            )
        ]


class POPendingTool(BaseSheetTool):
    """
    PO Pending Sheet Tool - Purchase Order Tracking
    ================================================
    
    Purpose:
        Manages pending purchase orders awaiting receipt. Tracks orders from placement
        to complete delivery, including partial shipments, payments, and cancellations.
    
    Key Features:
        - Purchase order lifecycle management
        - Indent number to PO number mapping
        - Supplier/Party management
        - Product specifications (Alumina %, Iron %, etc.)
        - Quantity tracking (ordered, lifted, pending, cancelled)
        - Rate and amount calculations
        - Lead time monitoring
        - Advance payment tracking
        - PO document storage (Google Drive links)
        - Partial delivery support
        - Order cancellation tracking
    
    Business Use Cases:
        - Monitor pending purchase orders
        - Track supplier performance and delivery times
        - Manage raw material procurement
        - Control advance payments to suppliers
        - Identify delayed or stuck orders
        - Calculate total purchase commitments
        - Maintain purchase order documentation
        - Audit procurement process
    
    Statistics:
        - Total Rows: 1,762
        - Total Columns: 20
        - Unique Suppliers: 71
        - Unique Products: 211
        - Completed Orders: 1,762 (100% marked as complete)
        - Average Lead Time: 15 days
        - Orders with Advance Payment: 131
    
    Data Quality:
        - PO Copy available: 93.8% (1,653 orders)
        - Alumina % data: 99.2%
        - Iron % data: 99.2%
        - Advance payment tracking: 7.4%
    """
    
    def __init__(self):
        super().__init__()
        self.sheet_name = "PO Pending"
        self.purpose = "Purchase orders awaiting receipt"
        self.total_rows = 1762
        self.total_columns = 20
        
        self.columns = [
            ColumnInfo(
                name="Timestamp",
                data_type="datetime64[ns]",
                unique_values=1762,
                null_count=0,
                sample_data=["2023-01-13 14:46:47.860000", "2023-01-13 14:47:48.551000"],
                description="Date and time when the PO record was created"
            ),
            ColumnInfo(
                name="Indent Number",
                data_type="object",
                unique_values=1762,
                null_count=0,
                sample_data=["RI-521", "RI-522"],
                description="Unique indent/requisition number for internal tracking"
            ),
            ColumnInfo(
                name="Have To Make Po",
                data_type="object",
                unique_values=2,
                null_count=0,
                sample_data=["Yes", "Yes"],
                description="Flag indicating whether PO needs to be created (Yes/No)"
            ),
            ColumnInfo(
                name="Party Name",
                data_type="object",
                unique_values=71,
                null_count=0,
                sample_data=["Dahmi Industries", "Dahmi Industries"],
                description="Name of the supplier/vendor party"
            ),
            ColumnInfo(
                name="Product Name",
                data_type="object",
                unique_values=211,
                null_count=0,
                sample_data=["Dahmi Pyro (0-1)", "Dahmi Pyro (1-3)"],
                description="Name and specification of the product being ordered"
            ),
            ColumnInfo(
                name="Quantity",
                data_type="float64",
                unique_values=279,
                null_count=14,
                sample_data=["40.0", "30.0"],
                description="Total quantity ordered in metric tons (MT)"
            ),
            ColumnInfo(
                name="Rate",
                data_type="float64",
                unique_values=387,
                null_count=14,
                sample_data=["10400.0", "10400.0"],
                description="Rate per metric ton (INR/MT)"
            ),
            ColumnInfo(
                name="Alumina %",
                data_type="float64",
                unique_values=55,
                null_count=14,
                sample_data=["38.0", "38.0"],
                description="Percentage of Alumina content in the raw material"
            ),
            ColumnInfo(
                name="Iron %",
                data_type="float64",
                unique_values=50,
                null_count=14,
                sample_data=["1.0", "1.0"],
                description="Percentage of Iron content in the raw material"
            ),
            ColumnInfo(
                name="Lead Time To Lift Total Qty",
                data_type="float64",
                unique_values=26,
                null_count=14,
                sample_data=["15.0", "15.0"],
                description="Expected number of days to receive complete order quantity"
            ),
            ColumnInfo(
                name="PO Copy",
                data_type="object",
                unique_values=1653,
                null_count=27,
                sample_data=["https://drive.google.com/open?", "https://drive.google.com/open?"],
                description="Google Drive link to the purchase order document"
            ),
            ColumnInfo(
                name="Total Amount",
                data_type="float64",
                unique_values=878,
                null_count=0,
                sample_data=["416000.0", "312000.0"],
                description="Total order amount (Quantity × Rate) in INR"
            ),
            ColumnInfo(
                name="Advance To Be Paid",
                data_type="object",
                unique_values=2,
                null_count=14,
                sample_data=["No", "No"],
                description="Whether advance payment is required (Yes/No)"
            ),
            ColumnInfo(
                name="To Be Paid Amount",
                data_type="float64",
                unique_values=87,
                null_count=1631,
                sample_data=["2246130.0", "737500.0"],
                description="Advance amount to be paid to supplier in INR"
            ),
            ColumnInfo(
                name="When To Be Paid",
                data_type="datetime64[ns]",
                unique_values=110,
                null_count=1631,
                sample_data=["2022-08-02 00:00:00", "2023-03-27 00:00:00"],
                description="Due date for advance payment"
            ),
            ColumnInfo(
                name="Notes",
                data_type="object",
                unique_values=350,
                null_count=426,
                sample_data=["0516", "0516"],
                description="Additional notes or reference numbers for the order"
            ),
            ColumnInfo(
                name="Total Lifted",
                data_type="float64",
                unique_values=989,
                null_count=0,
                sample_data=["32.503", "28.984"],
                description="Total quantity actually received/lifted so far in MT"
            ),
            ColumnInfo(
                name="Pending Qty",
                data_type="float64",
                unique_values=475,
                null_count=0,
                sample_data=["0.0", "0.0"],
                description="Remaining quantity yet to be received in MT"
            ),
            ColumnInfo(
                name="Order Cancel Qty",
                data_type="float64",
                unique_values=319,
                null_count=0,
                sample_data=["7.497", "1.016"],
                description="Quantity of order that was cancelled in MT"
            ),
            ColumnInfo(
                name="Status",
                data_type="object",
                unique_values=2,
                null_count=0,
                sample_data=["Complete", "Complete"],
                description="Overall status of the purchase order (Complete/Pending/Partial)"
            )
        ]


class FGStockTool(BaseSheetTool):
    """
    FG Stock Sheet Tool - Finished Goods Inventory
    ===============================================
    
    Purpose:
        Maintains current inventory levels of finished goods (FG) ready for sale.
        Real-time tracking of stock levels for all manufactured products.
    
    Key Features:
        - Real-time stock level tracking
        - Product-wise inventory management
        - Zero-stock identification
        - Stock availability for order fulfillment
        - Inventory valuation support
    
    Business Use Cases:
        - Monitor finished goods availability
        - Identify low-stock products for production planning
        - Support order promising and delivery commitments
        - Calculate inventory holding costs
        - Prevent stockouts and lost sales
        - Optimize production scheduling
        - Enable just-in-time manufacturing
    
    Statistics:
        - Total Rows: 104
        - Total Columns: 2
        - Unique Products: 104
        - Products with Zero Stock: Majority
        - Active Stock Items: ~51 products
    
    Data Quality:
        - Product names: 100% unique
        - Current level: 100% populated
        - Simple, clean structure
    """
    
    def __init__(self):
        super().__init__()
        self.sheet_name = "FG Stock"
        self.purpose = "Finished Goods inventory levels"
        self.total_rows = 104
        self.total_columns = 2
        
        self.columns = [
            ColumnInfo(
                name="Product Name",
                data_type="object",
                unique_values=104,
                null_count=0,
                sample_data=["90 S", "95 S"],
                description="Name/code of the finished goods product"
            ),
            ColumnInfo(
                name="Current Level",
                data_type="float64",
                unique_values=51,
                null_count=0,
                sample_data=["0.0", "0.0"],
                description="Current stock quantity available in metric tons (MT)"
            )
        ]


class RMSockTool(BaseSheetTool):
    """
    RM Sock Sheet Tool - Raw Material Inventory & Planning
    =======================================================
    
    Purpose:
        Manages raw material inventory levels and procurement planning. Calculates
        requirements based on production needs (full kitting) and current stock.
    
    Key Features:
        - Real-time raw material stock tracking
        - Color-coded inventory status (Red/Yellow/Green)
        - Full kitting calculation for FG + Semi-finished goods
        - Automatic indent requirement calculation
        - Procurement quantity recommendations
        - Negative stock alerts
    
    Business Use Cases:
        - Raw material availability monitoring
        - Production planning and scheduling
        - Procurement planning and requisition
        - Inventory optimization
        - Prevent production stoppage due to material shortage
        - Just-in-time inventory management
        - Cost control through optimal stocking
    
    Statistics:
        - Total Rows: 161
        - Total Columns: 6
        - Unique Items: 159
        - Color Codes: 4 (Red/Yellow/Green/etc.)
        - Items with Full Kitting Data: ~36
    
    Data Quality:
        - Item names: 100% unique
        - Current level: 100% calculated
        - Color coding: 100% applied
        - Calculated fields populated
    
    Important Notes:
        - Negative stock values indicate shortage/backlog
        - Full Kitting = Raw material needed for complete production
        - To Be Indented = Additional material to be requisitioned
        - To Be Lifted = Material already ordered but not received
    """
    
    def __init__(self):
        super().__init__()
        self.sheet_name = "RM Sock"
        self.purpose = "Raw Material inventory and planning"
        self.total_rows = 161
        self.total_columns = 6
        
        self.columns = [
            ColumnInfo(
                name="Item Name",
                data_type="object",
                unique_values=159,
                null_count=0,
                sample_data=["99 C Fired", "99 C Fines"],
                description="Name/code of the raw material item"
            ),
            ColumnInfo(
                name="Current Level",
                data_type="float64",
                unique_values=124,
                null_count=0,
                sample_data=["-7.283063041541027e-14", "3.552713678800501e-15"],
                description="Current stock level in metric tons (MT). Negative values indicate shortage."
            ),
            ColumnInfo(
                name="Colour Code",
                data_type="object",
                unique_values=4,
                null_count=0,
                sample_data=["Red", "Red"],
                description="Visual indicator of stock status: Red (Critical/Low), Yellow (Moderate), Green (Adequate)"
            ),
            ColumnInfo(
                name="Full Kitting FG + Semi",
                data_type="float64",
                unique_values=36,
                null_count=0,
                sample_data=["0.0", "0.0"],
                description="Total raw material quantity required for full production of finished goods and semi-finished items in MT"
            ),
            ColumnInfo(
                name="To Be Indented",
                data_type="float64",
                unique_values=124,
                null_count=0,
                sample_data=["7.283063041541027e-14", "-14.000000000000004"],
                description="Quantity that needs to be requisitioned/indented based on current level and full kitting requirements in MT"
            ),
            ColumnInfo(
                name="To Be Lifted",
                data_type="float64",
                unique_values=124,
                null_count=0,
                sample_data=["7.283063041541027e-14", "-3.552713678800501e-15"],
                description="Quantity already ordered (PO issued) but not yet received/lifted in MT"
            )
        ]


class PurchaseIntransitTool(BaseSheetTool):
    """
    Purchase Intransit Sheet Tool - Material In-Transit Tracking
    ============================================================
    
    Purpose:
        Tracks purchase orders that are currently in transit from supplier to factory.
        Monitors shipments, transportation details, and expected arrival dates.
    
    Key Features:
        - Real-time shipment tracking
        - Lift number (LN) and PO number linking
        - Truck and driver information
        - Transporter details and rates
        - Lead time monitoring
        - Bill and bilty document storage
        - Expected arrival date calculation
        - Material rate tracking
        - Transportation cost management
    
    Business Use Cases:
        - Track incoming material shipments
        - Monitor transportation performance
        - Estimate material arrival for production planning
        - Verify transportation costs
        - Maintain shipment documentation
        - Alert for delayed shipments
        - Coordinate warehouse receiving
        - Audit transportation charges
    
    Statistics:
        - Total Rows: 9 (active shipments)
        - Total Columns: 21
        - Unique Suppliers: 5
        - Unique Products: 9
        - Active Transporters: 3
        - Average Lead Time: 3 days
    
    Data Quality:
        - Lift numbers: 100% unique
        - Truck numbers: 77.8% available
        - Driver numbers: 11.1% available
        - Bill images: 66.7% uploaded
        - Transporter info: 77.8% available
    """
    
    def __init__(self):
        super().__init__()
        self.sheet_name = "Purchase Intransit"
        self.purpose = "Tracking purchases currently in transit"
        self.total_rows = 9
        self.total_columns = 21
        
        self.columns = [
            ColumnInfo(
                name="Timestamp",
                data_type="datetime64[ns]",
                unique_values=9,
                null_count=0,
                sample_data=["2025-07-01 12:48:21.895000", "2025-12-08 18:16:10.126000"],
                description="Date and time when the intransit record was created"
            ),
            ColumnInfo(
                name="LN-Lift Number",
                data_type="object",
                unique_values=9,
                null_count=0,
                sample_data=["LN-4104", "LN-4984"],
                description="Unique lift number for tracking this specific shipment"
            ),
            ColumnInfo(
                name="Type",
                data_type="object",
                unique_values=2,
                null_count=0,
                sample_data=["Independent", "Independent"],
                description="Type of lift - Independent or part of bulk order"
            ),
            ColumnInfo(
                name="Po Number",
                data_type="object",
                unique_values=9,
                null_count=0,
                sample_data=["RI-1929", "RI-2273"],
                description="Purchase order number associated with this shipment"
            ),
            ColumnInfo(
                name="Bill No.",
                data_type="int64",
                unique_values=7,
                null_count=0,
                sample_data=["0", "246"],
                description="Supplier bill/invoice number for this shipment"
            ),
            ColumnInfo(
                name="Party Name",
                data_type="object",
                unique_values=5,
                null_count=0,
                sample_data=["Passary Minerals Rourkela", "Peekay Petrochem Pvt Ltd"],
                description="Name of the supplier/party sending the material"
            ),
            ColumnInfo(
                name="Product Name",
                data_type="object",
                unique_values=9,
                null_count=0,
                sample_data=["Silliminite Sand", "Plastic Clay"],
                description="Name of the product/material being transported"
            ),
            ColumnInfo(
                name="Qty",
                data_type="float64",
                unique_values=8,
                null_count=0,
                sample_data=["0.0", "30.0"],
                description="Quantity being transported in metric tons (MT)"
            ),
            ColumnInfo(
                name="Area Lifting",
                data_type="object",
                unique_values=1,
                null_count=0,
                sample_data=["Supplying In Factory", "Supplying In Factory"],
                description="Delivery location - typically factory premises"
            ),
            ColumnInfo(
                name="Lead Time To Reach Factory",
                data_type="int64",
                unique_values=2,
                null_count=0,
                sample_data=["3", "3"],
                description="Expected number of days for material to reach factory"
            ),
            ColumnInfo(
                name="Truck No.",
                data_type="object",
                unique_values=6,
                null_count=2,
                sample_data=["OD07V8625", "WB57D6127"],
                description="Registration number of the truck carrying the material"
            ),
            ColumnInfo(
                name="Driver No.",
                data_type="float64",
                unique_values=1,
                null_count=8,
                sample_data=["9078791722.0"],
                description="Contact phone number of the truck driver"
            ),
            ColumnInfo(
                name="Transporter Name",
                data_type="object",
                unique_values=3,
                null_count=2,
                sample_data=["Ex Factory Transporter", "Ex Factory Transporter"],
                description="Name of the transportation company/service provider"
            ),
            ColumnInfo(
                name="Bill Image",
                data_type="object",
                unique_values=6,
                null_count=3,
                sample_data=["https://drive.google.com/open?", "https://drive.google.com/open?"],
                description="Google Drive link to supplier bill/invoice image"
            ),
            ColumnInfo(
                name="Bilty No.",
                data_type="float64",
                unique_values=0,
                null_count=9,
                sample_data=["-", "-"],
                description="Bilty/consignment note number (currently unused)"
            ),
            ColumnInfo(
                name="Type Of Rate",
                data_type="object",
                unique_values=2,
                null_count=2,
                sample_data=["Fixed Amount", "Fixed Amount"],
                description="Transportation rate type - Fixed Amount or Per Ton"
            ),
            ColumnInfo(
                name="Rate",
                data_type="float64",
                unique_values=1,
                null_count=8,
                sample_data=["1150.0"],
                description="Transportation rate/freight charges in INR"
            ),
            ColumnInfo(
                name="Truck Qty",
                data_type="float64",
                unique_values=7,
                null_count=2,
                sample_data=["0.0", "30.0"],
                description="Actual quantity loaded in truck in MT"
            ),
            ColumnInfo(
                name="Material Rate",
                data_type="int64",
                unique_values=9,
                null_count=0,
                sample_data=["0", "5100"],
                description="Rate per MT of the material in INR"
            ),
            ColumnInfo(
                name="Bilty Image",
                data_type="float64",
                unique_values=0,
                null_count=9,
                sample_data=["-", "-"],
                description="Image of bilty/consignment note (currently unused)"
            ),
            ColumnInfo(
                name="Expected Date To Reach",
                data_type="datetime64[ns]",
                unique_values=4,
                null_count=0,
                sample_data=["2025-07-04 00:00:00", "2025-12-11 00:00:00"],
                description="Calculated expected arrival date at factory"
            )
        ]


class PaymentsTool(BaseSheetTool):
    """
    Payments Sheet Tool - Accounts Payable Management
    ==================================================
    
    Purpose:
        Manages all outgoing payment transactions including supplier payments,
        advances, repairs, and other expenses. Tracks payment approvals and status.
    
    Key Features:
        - Payment number generation and tracking
        - Multiple FMS (Financial Management System) categories
        - Payee/vendor management
        - Amount tracking with remarks
        - Document attachment support
        - Planned vs actual payment dates
        - Approval workflow management
        - Payment status tracking (Approved/Rejected)
        - Link to source documents (PO, bills, etc.)
    
    Business Use Cases:
        - Accounts payable management
        - Supplier payment tracking
        - Advance payment monitoring
        - Expense management and control
        - Payment approval workflow
        - Cash flow planning and forecasting
        - Vendor payment history
        - Audit trail for financial transactions
        - Budget vs actual analysis
    
    Statistics:
        - Total Rows: 8,125
        - Total Columns: 12
        - Unique Payments: 8,125
        - FMS Categories: 41 different types
        - Unique Payees: 2,704
        - Approved Payments: 7,176 (88.3%)
        - Rejected Payments: Minimal
        - With Attachments: 4,256 (52.4%)
    
    Data Quality:
        - Payment numbers: 100% unique
        - Status flag: 97.5% marked "Yes"
        - Approval status: 88.3% processed
        - Planned dates: 71.6% set
        - Attachments: 52.4% available
    """
    
    def __init__(self):
        super().__init__()
        self.sheet_name = "Payments"
        self.purpose = "Outgoing payment transactions"
        self.total_rows = 8125
        self.total_columns = 12
        
        self.columns = [
            ColumnInfo(
                name="Timestamp",
                data_type="datetime64[ns]",
                unique_values=8125,
                null_count=0,
                sample_data=["2023-04-01 13:39:58.210000", "2023-04-01 13:48:12.559000"],
                description="Date and time when payment record was created"
            ),
            ColumnInfo(
                name="Payment Number",
                data_type="object",
                unique_values=8125,
                null_count=0,
                sample_data=["AP-02", "AP-03"],
                description="Unique accounts payable payment number"
            ),
            ColumnInfo(
                name="Status",
                data_type="object",
                unique_values=2,
                null_count=0,
                sample_data=["Yes", "Yes"],
                description="Initial status flag (Yes/No) - mostly Yes"
            ),
            ColumnInfo(
                name="Unique Number",
                data_type="object",
                unique_values=6737,
                null_count=3,
                sample_data=["RI-598", "0320"],
                description="Reference to source document (PO number, indent, bill number, etc.)"
            ),
            ColumnInfo(
                name="Fms Name",
                data_type="object",
                unique_values=41,
                null_count=4,
                sample_data=["Purchase FMS Po Advance", "Repair FMS"],
                description="Financial Management System category (Purchase, Repair, Salary, Transport, etc.)"
            ),
            ColumnInfo(
                name="Pay To",
                data_type="object",
                unique_values=2704,
                null_count=202,
                sample_data=["Thyme India Pvt Ltd", "Hindustan repairing center"],
                description="Name of payee/vendor/supplier receiving the payment"
            ),
            ColumnInfo(
                name="Amount To Be Paid",
                data_type="float64",
                unique_values=4172,
                null_count=203,
                sample_data=["729505.0", "3192.0"],
                description="Payment amount in INR"
            ),
            ColumnInfo(
                name="Remarks",
                data_type="object",
                unique_values=7146,
                null_count=199,
                sample_data=["For purchase of SMS Microsilic", "For Stitching machine no. (3.6"],
                description="Detailed payment purpose and notes"
            ),
            ColumnInfo(
                name="Any Attachments",
                data_type="object",
                unique_values=4256,
                null_count=3869,
                sample_data=["https://drive.google.com/open?", "https://drive.google.com/open?"],
                description="Google Drive links to bills, invoices, or supporting documents"
            ),
            ColumnInfo(
                name="Planned Date",
                data_type="datetime64[ns]",
                unique_values=888,
                null_count=231,
                sample_data=["2023-04-01 00:00:00", "2023-04-01 00:00:00"],
                description="Planned/scheduled date for making the payment"
            ),
            ColumnInfo(
                name="Approval Date",
                data_type="datetime64[ns]",
                unique_values=757,
                null_count=237,
                sample_data=["2023-04-01 00:00:00", "2023-04-01 00:00:00"],
                description="Date when payment was approved by authorized personnel"
            ),
            ColumnInfo(
                name="Status.1",
                data_type="object",
                unique_values=2,
                null_count=949,
                sample_data=["Rejected", "Approved"],
                description="Final approval status (Approved/Rejected)"
            )
        ]


class EnquirysTool(BaseSheetTool):
    """
    Enquirys Sheet Tool - Sales Lead & Quote Management
    ===================================================
    
    Purpose:
        Manages customer enquiries, quotes, and sales lead pipeline. Tracks from
        initial enquiry through quotation to order conversion.
    
    Key Features:
        - Enquiry number tracking
        - Multiple products per enquiry support
        - Hot/warm/cold lead classification
        - NBD (New Business Development) tracking
        - Location and application area capture
        - Sales person assignment
        - Multi-proposal comparison (up to 3 proposals)
        - Order conversion tracking
        - Document upload for specifications
        - Contact information management
        - Lead time estimation
    
    Business Use Cases:
        - Sales pipeline management
        - Lead tracking and conversion
        - Quote generation and comparison
        - Territory/sales person performance
        - Customer inquiry response
        - New business development monitoring
        - Department-wise demand analysis
        - Win/loss analysis
        - Revenue forecasting
    
    Statistics:
        - Total Rows: 230
        - Total Columns: 32
        - Unique Enquiries: 230
        - Firms: 3 (RKL, etc.)
        - Sales Personnel: 9
        - Unique Customers: 150
        - Departments: 10 (DRI, Blast Furnace, etc.)
        - Orders Received: 192 (83.5% conversion rate)
    
    Data Quality:
        - Enquiry numbers: 100% unique
        - Upload files: 99.6% attached
        - Contact info: 99% complete
        - Proposal amounts: 21% with detailed proposals
    """
    
    def __init__(self):
        super().__init__()
        self.sheet_name = "Enquirys"
        self.purpose = "Customer enquiries and leads"
        self.total_rows = 230
        self.total_columns = 32
        
        self.columns = [
            ColumnInfo(
                name="Timestamp",
                data_type="object",
                unique_values=114,
                null_count=0,
                sample_data=["2024-12-06 00:00:00", "2024-12-06 00:00:00"],
                description="Date and time when enquiry was recorded"
            ),
            ColumnInfo(
                name="Enquiry No.",
                data_type="object",
                unique_values=230,
                null_count=0,
                sample_data=["EN-2", "EN-3"],
                description="Unique enquiry number for tracking"
            ),
            ColumnInfo(
                name="Product No.",
                data_type="int64",
                unique_values=10,
                null_count=0,
                sample_data=["2", "3"],
                description="Product line number within the enquiry"
            ),
            ColumnInfo(
                name="Firm Name",
                data_type="object",
                unique_values=3,
                null_count=0,
                sample_data=["RKL", "RKL"],
                description="PMMPL firm handling the enquiry (RKL/others)"
            ),
            ColumnInfo(
                name="Enquiry status",
                data_type="object",
                unique_values=3,
                null_count=0,
                sample_data=["Hot ", "Hot "],
                description="Lead temperature: Hot (immediate), Warm (near-term), Cold (long-term)"
            ),
            ColumnInfo(
                name="Type Of Enquiry",
                data_type="object",
                unique_values=2,
                null_count=0,
                sample_data=["NBD OF CRR", "NBD OF CRR"],
                description="Source type: NBD (New Business Development), CRR (Customer Repeat Request), etc."
            ),
            ColumnInfo(
                name="Location",
                data_type="object",
                unique_values=170,
                null_count=0,
                sample_data=["SAMBALPUR", "Singhbhum (West), Jharkhand"],
                description="Customer location/site where material will be used"
            ),
            ColumnInfo(
                name="Name Of Sales Person",
                data_type="object",
                unique_values=9,
                null_count=0,
                sample_data=["AJAY GUPTA", "SITAL KAR"],
                description="Sales representative assigned to this enquiry"
            ),
            ColumnInfo(
                name="Party Name",
                data_type="object",
                unique_values=150,
                null_count=0,
                sample_data=["Aryan Ispat & Power P. Ltd", "RUNGTA MINES LTD"],
                description="Customer company name"
            ),
            ColumnInfo(
                name="Department",
                data_type="object",
                unique_values=10,
                null_count=0,
                sample_data=["DRI", "DRI"],
                description="Customer's department/plant type (DRI, Blast Furnace, Kiln, etc.)"
            ),
            ColumnInfo(
                name="Total Order Qty",
                data_type="object",
                unique_values=147,
                null_count=0,
                sample_data=["10", "385.5"],
                description="Total quantity requested across all products"
            ),
            ColumnInfo(
                name="Expected",
                data_type="object",
                unique_values=43,
                null_count=0,
                sample_data=["0", "0"],
                description="Expected order value or quantity"
            ),
            ColumnInfo(
                name="When Required",
                data_type="datetime64[ns]",
                unique_values=142,
                null_count=0,
                sample_data=["2024-06-11 00:00:00", "2024-06-11 00:00:00"],
                description="Customer's required delivery date"
            ),
            ColumnInfo(
                name="Area Of Application",
                data_type="object",
                unique_values=51,
                null_count=1,
                sample_data=["0", "ALL"],
                description="Specific application area within plant (Hot Face, Cold Face, etc.)"
            ),
            ColumnInfo(
                name="Upload File",
                data_type="object",
                unique_values=229,
                null_count=1,
                sample_data=["https://drive.google.com/file/", "https://drive.google.com/file/"],
                description="Customer specifications, drawings, or requirement documents"
            ),
            ColumnInfo(
                name="Contact Person Name",
                data_type="object",
                unique_values=174,
                null_count=2,
                sample_data=["Mr. Furkan Ali", "0"],
                description="Primary contact person at customer site"
            ),
            ColumnInfo(
                name="Contact Person Mobile No.",
                data_type="object",
                unique_values=115,
                null_count=2,
                sample_data=["7978297729", "0"],
                description="Mobile number of contact person"
            ),
            ColumnInfo(
                name="Email Id",
                data_type="object",
                unique_values=159,
                null_count=2,
                sample_data=["aryanpurchase@gmail.com", "srsplpurchase@gmail.com"],
                description="Email address of contact person"
            ),
            ColumnInfo(
                name="Lead Time For Convert In Order",
                data_type="object",
                unique_values=40,
                null_count=0,
                sample_data=["7", "15"],
                description="Expected days to convert enquiry into confirmed order"
            ),
            ColumnInfo(
                name="Did The Above Enquiry Come From Nbd Outgoing Sheet",
                data_type="object",
                unique_values=2,
                null_count=0,
                sample_data=["NO", "NO"],
                description="Whether enquiry originated from NBD outreach (YES/NO)"
            ),
            ColumnInfo(
                name="Offer No.",
                data_type="object",
                unique_values=183,
                null_count=0,
                sample_data=["51", "52"],
                description="Quotation/offer number issued to customer"
            ),
            ColumnInfo(
                name="Product Names",
                data_type="object",
                unique_values=65,
                null_count=0,
                sample_data=["Pasheat - K", "LCM - 75 AR With 1% SS Fiber"],
                description="Specific products quoted in the offer"
            ),
            ColumnInfo(
                name="Quetities",
                data_type="object",
                unique_values=116,
                null_count=0,
                sample_data=["5", "380"],
                description="Quantities for each product in the quote"
            ),
            ColumnInfo(
                name="Uom",
                data_type="object",
                unique_values=3,
                null_count=0,
                sample_data=["MT", "MT"],
                description="Unit of measurement (MT - Metric Ton, PCS - Pieces, etc.)"
            ),
            ColumnInfo(
                name="Proposal Amount 1",
                data_type="object",
                unique_values=47,
                null_count=182,
                sample_data=["2,54,67,000.00", "60755500"],
                description="First proposal/option amount in INR"
            ),
            ColumnInfo(
                name="Proposal Remarks 1",
                data_type="object",
                unique_values=38,
                null_count=187,
                sample_data=["Double Layer Casting with the", "Double Layer Casting with the"],
                description="Description of first proposal option"
            ),
            ColumnInfo(
                name="Proposal Amount 2",
                data_type="float64",
                unique_values=24,
                null_count=205,
                sample_data=["64464500.0", "32792000.0"],
                description="Second proposal/option amount in INR"
            ),
            ColumnInfo(
                name="Proposal Remarks 2",
                data_type="object",
                unique_values=25,
                null_count=205,
                sample_data=["Single Layer Casting", "Refractory thickness 230 mm"],
                description="Description of second proposal option"
            ),
            ColumnInfo(
                name="Proposal Amount 3",
                data_type="float64",
                unique_values=7,
                null_count=223,
                sample_data=["89565300.0", "5461200.0"],
                description="Third proposal/option amount in INR"
            ),
            ColumnInfo(
                name="Proposal Remarks 3",
                data_type="object",
                unique_values=7,
                null_count=223,
                sample_data=["As Per Your Requirement(propos", "For Single Layer Casting: -"],
                description="Description of third proposal option"
            ),
            ColumnInfo(
                name="G-mail",
                data_type="float64",
                unique_values=0,
                null_count=230,
                sample_data=["-", "-"],
                description="Additional email field (currently unused)"
            ),
            ColumnInfo(
                name="Status",
                data_type="object",
                unique_values=2,
                null_count=38,
                sample_data=["Order Received", "Order Received"],
                description="Final status: Order Received, Pending, Lost, etc."
            )
        ]


class StoreOUTTool(BaseSheetTool):
    """
    Store OUT Sheet Tool - Warehouse Issue Management
    ==================================================
    
    Purpose:
        Manages inventory issued from warehouse to production floor, departments,
        or other locations. Tracks requisitions, approvals, and actual issue times.
    
    Key Features:
        - Request number generation
        - Indentor identification
        - Department and area tracking
        - Product group head classification
        - Requested vs issued quantity tracking
        - Planned vs actual issue time monitoring
        - Delay calculation
        - Application number linking (for equipment/machine)
        - Multiple unit of measurement support
    
    Business Use Cases:
        - Warehouse material issue tracking
        - Production material requirement fulfillment
        - Inventory movement monitoring
        - Department-wise consumption analysis
        - Delay identification in material supply
        - Equipment spare parts tracking
        - Material requisition approval workflow
        - Stock accuracy maintenance
    
    Statistics:
        - Total Rows: 198
        - Total Columns: 17
        - Unique Requests: 198
        - Indentors: 12
        - Departments: 3 (Akoli, etc.)
        - Areas: 9
        - Product Groups: 18
        - Unique Products: 81
    
    Data Quality:
        - Request numbers: 100% unique
        - Planned times: 100% set
        - Actual out times: 100% recorded
        - Delay tracking: 60% calculated
        - Application numbers: 9.6% linked
    """
    
    def __init__(self):
        super().__init__()
        self.sheet_name = "Store OUT"
        self.purpose = "Inventory issued from warehouse"
        self.total_rows = 198
        self.total_columns = 17
        
        self.columns = [
            ColumnInfo(
                name="Timestamp",
                data_type="datetime64[ns]",
                unique_values=198,
                null_count=0,
                sample_data=["2024-02-29 11:29:05.776000", "2024-02-29 11:31:56.165000"],
                description="Date and time when issue request was created"
            ),
            ColumnInfo(
                name="Request Number",
                data_type="object",
                unique_values=198,
                null_count=0,
                sample_data=["SO-996", "SO-997"],
                description="Unique store out/issue request number"
            ),
            ColumnInfo(
                name="Indentor Name",
                data_type="object",
                unique_values=12,
                null_count=0,
                sample_data=["NAKUL VERMA", "NAKUL VERMA"],
                description="Name of person requesting the material"
            ),
            ColumnInfo(
                name="Department",
                data_type="object",
                unique_values=3,
                null_count=0,
                sample_data=["Akoli", "Akoli"],
                description="Department requesting the material"
            ),
            ColumnInfo(
                name="Area",
                data_type="object",
                unique_values=9,
                null_count=1,
                sample_data=["Factory Office", "Factory Office"],
                description="Specific area or location within department"
            ),
            ColumnInfo(
                name="Group Head",
                data_type="object",
                unique_values=18,
                null_count=0,
                sample_data=["ELECTRICAL", "NUT BOLT"],
                description="Product category/group (Electrical, Mechanical, Consumables, etc.)"
            ),
            ColumnInfo(
                name="Product Name",
                data_type="object",
                unique_values=81,
                null_count=0,
                sample_data=["Electric Tape", "Nut Bolt Visor 10x50"],
                description="Specific product/item name being requested"
            ),
            ColumnInfo(
                name="Qty Requested",
                data_type="float64",
                unique_values=22,
                null_count=0,
                sample_data=["2.0", "3.0"],
                description="Quantity requested by indentor"
            ),
            ColumnInfo(
                name="Unit Of Measurement",
                data_type="object",
                unique_values=10,
                null_count=1,
                sample_data=["PCS", "PCS"],
                description="Unit: PCS (Pieces), KG, LTR, MTR, etc."
            ),
            ColumnInfo(
                name="Application No.(If Aplicable)",
                data_type="float64",
                unique_values=1,
                null_count=179,
                sample_data=["66.0", "66.0"],
                description="Machine/equipment number where material will be used"
            ),
            ColumnInfo(
                name="Planned Time For Out",
                data_type="datetime64[ns]",
                unique_values=194,
                null_count=0,
                sample_data=["2024-03-01 11:29:00", "2024-03-01 11:31:00"],
                description="Scheduled date/time for material issue"
            ),
            ColumnInfo(
                name="Out Time",
                data_type="datetime64[ns]",
                unique_values=198,
                null_count=0,
                sample_data=["2024-03-13 13:59:41.772000", "2024-03-13 13:58:50.859000"],
                description="Actual date/time when material was issued"
            ),
            ColumnInfo(
                name="Delay",
                data_type="float64",
                unique_values=119,
                null_count=79,
                sample_data=["12.104650138884608", "12.102671979162551"],
                description="Delay in days between planned and actual issue time"
            ),
            ColumnInfo(
                name="Issue Status",
                data_type="object",
                unique_values=1,
                null_count=0,
                sample_data=["Issuing", "Issuing"],
                description="Current status of the issue request"
            ),
            ColumnInfo(
                name="Qty",
                data_type="int64",
                unique_values=21,
                null_count=0,
                sample_data=["2", "3"],
                description="Actual quantity issued"
            ),
            ColumnInfo(
                name="Unit Of Measurement.1",
                data_type="object",
                unique_values=5,
                null_count=0,
                sample_data=["PCS", "PCS"],
                description="Confirmed unit of measurement for issued quantity"
            ),
            ColumnInfo(
                name="Product Name.1",
                data_type="object",
                unique_values=81,
                null_count=0,
                sample_data=["Electric Tape", "Nut Bolt Visor 10x50"],
                description="Confirmed product name that was issued"
            )
        ]


class NewStoreIndentTool(BaseSheetTool):
    """
    New Store Indent Sheet Tool - Material Requisition Form
    ========================================================
    
    Purpose:
        Template/form sheet for creating new store indents/requisitions.
        Currently contains only the structure with #REF! errors indicating
        this is a template sheet with formula references.
    
    Key Features:
        - Indent creation template
        - Requisition structure definition
        - Field definitions for new requests
    
    Business Use Cases:
        - Template for new material requests
        - Standardized requisition format
        - Data entry structure
    
    Statistics:
        - Total Rows: 1
        - Total Columns: 10
        - Contains: Structure/template only
    """
    
    def __init__(self):
        super().__init__()
        self.sheet_name = "New Store Indent"
        self.purpose = "Template for new material requisitions"
        self.total_rows = 1
        self.total_columns = 10
        
        self.columns = [
            ColumnInfo(
                name="TimeStamp",
                data_type="object",
                unique_values=1,
                null_count=0,
                sample_data=["#REF!"],
                description="Date and time of indent"
            ),
            ColumnInfo(
                name="Indent No.",
                data_type="float64",
                unique_values=0,
                null_count=1,
                sample_data=["-"],
                description="Unique indent number"
            ),
            ColumnInfo(
                name="Indentor Name",
                data_type="float64",
                unique_values=0,
                null_count=1,
                sample_data=["-"],
                description="Name of person requesting material"
            ),
            ColumnInfo(
                name="Department",
                data_type="float64",
                unique_values=0,
                null_count=1,
                sample_data=["-"],
                description="Requesting department"
            ),
            ColumnInfo(
                name="Area Of Machine",
                data_type="float64",
                unique_values=0,
                null_count=1,
                sample_data=["-"],
                description="Machine or area where material is needed"
            ),
            ColumnInfo(
                name="Group Head",
                data_type="float64",
                unique_values=0,
                null_count=1,
                sample_data=["-"],
                description="Product group category"
            ),
            ColumnInfo(
                name="Product Name",
                data_type="float64",
                unique_values=0,
                null_count=1,
                sample_data=["-"],
                description="Name of product requested"
            ),
            ColumnInfo(
                name="Qty",
                data_type="float64",
                unique_values=0,
                null_count=1,
                sample_data=["-"],
                description="Quantity requested"
            ),
            ColumnInfo(
                name="Product Make Name/Specifications",
                data_type="float64",
                unique_values=0,
                null_count=1,
                sample_data=["-"],
                description="Specific make or technical specifications"
            ),
            ColumnInfo(
                name="Application Number",
                data_type="float64",
                unique_values=0,
                null_count=1,
                sample_data=["-"],
                description="Application or equipment reference number"
            )
        ]


class StoreINTool(BaseSheetTool):
    """
    Store IN Sheet Tool - Inventory Receipt Management
    ===================================================
    
    Purpose:
        Manages inventory received into the warehouse. Tracks bills, vendors,
        and product details for incoming stock. Like New Store Indent, this
        appears to be a template or recently cleared sheet.
    
    Key Features:
        - Inward inventory tracking
        - Bill and vendor details
        - Transportation and payment information
    
    Statistics:
        - Total Rows: 1
        - Total Columns: 15
        - Contains: Structure/template only
    """
    
    def __init__(self):
        super().__init__()
        self.sheet_name = "Store IN"
        self.purpose = "Inventory received into warehouse"
        self.total_rows = 1
        self.total_columns = 15
        
        self.columns = [
            ColumnInfo(
                name="Timestamp",
                data_type="object",
                unique_values=1,
                null_count=0,
                sample_data=["#REF!"],
                description="Date and time of receipt"
            ),
            ColumnInfo(
                name="Indent No.",
                data_type="float64",
                unique_values=0,
                null_count=1,
                sample_data=["-"],
                description="Reference indent number"
            ),
            ColumnInfo(
                name="Bill No.",
                data_type="float64",
                unique_values=0,
                null_count=1,
                sample_data=["-"],
                description="Vendor bill number"
            ),
            ColumnInfo(
                name="Vendor Name",
                data_type="float64",
                unique_values=0,
                null_count=1,
                sample_data=["-"],
                description="Name of supplier/vendor"
            ),
            ColumnInfo(
                name="Product Name",
                data_type="float64",
                unique_values=0,
                null_count=1,
                sample_data=["-"],
                description="Name of received product"
            ),
            ColumnInfo(
                name="Qty",
                data_type="float64",
                unique_values=0,
                null_count=1,
                sample_data=["-"],
                description="Quantity received"
            ),
            ColumnInfo(
                name="Type Of Bill",
                data_type="float64",
                unique_values=0,
                null_count=1,
                sample_data=["-"],
                description="Bill type classification"
            ),
            ColumnInfo(
                name="Bill Amount",
                data_type="float64",
                unique_values=0,
                null_count=1,
                sample_data=["-"],
                description="Total bill amount"
            ),
            ColumnInfo(
                name="Payment Type",
                data_type="float64",
                unique_values=0,
                null_count=1,
                sample_data=["-"],
                description="Method of payment"
            ),
            ColumnInfo(
                name="Advance Amount If Any",
                data_type="float64",
                unique_values=0,
                null_count=1,
                sample_data=["-"],
                description="Advance payment details"
            ),
            ColumnInfo(
                name="Photo Of Bill",
                data_type="float64",
                unique_values=0,
                null_count=1,
                sample_data=["-"],
                description="Image of the bill"
            ),
            ColumnInfo(
                name="Transportation Include",
                data_type="float64",
                unique_values=0,
                null_count=1,
                sample_data=["-"],
                description="Whether transportation is included"
            ),
            ColumnInfo(
                name="Transporter Name",
                data_type="float64",
                unique_values=0,
                null_count=1,
                sample_data=["-"],
                description="Name of transporter"
            ),
            ColumnInfo(
                name="Amount",
                data_type="float64",
                unique_values=0,
                null_count=1,
                sample_data=["-"],
                description="Amount details"
            ),
            ColumnInfo(
                name="Department",
                data_type="float64",
                unique_values=0,
                null_count=1,
                sample_data=["-"],
                description="Receiving department"
            )
        ]


class PurchaseReceiptTool(BaseSheetTool):
    """
    Purchase Receipt Sheet Tool - GRN (Goods Receipt Note) Helper
    =============================================================
    
    Purpose:
        Tracks received purchase orders (GRN details). Monitors quantity
        received vs billed, physical condition, and quality checks.
    
    Key Features:
        - Goods Receipt Note (GRN) tracking
        - PO and Bill mapping
        - Quantity verification (Billed vs Actual)
        - Quality/Physical condition check
        - Photographic evidence storage
        - Moisture check
    
    Statistics:
        - Total Rows: 198
        - Total Columns: 19
        - Unique Bills: 85
        - Material Images: 98% mapped
    """
    
    def __init__(self):
        super().__init__()
        self.sheet_name = "Purchase Receipt"
        self.purpose = "Received purchase orders tracking"
        self.total_rows = 198
        self.total_columns = 19
        
        self.columns = [
            ColumnInfo(
                name="Timestamp",
                data_type="datetime64[ns]",
                unique_values=198,
                null_count=0,
                sample_data=["2023-01-13 17:25:20", "2023-01-13 17:25:41"],
                description="Entry timestamp"
            ),
            ColumnInfo(
                name="Lift Number",
                data_type="object",
                unique_values=198,
                null_count=0,
                sample_data=["LN-14", "LN-13"],
                description="Unique lift/shipment identifier"
            ),
            ColumnInfo(
                name="PO Number",
                data_type="object",
                unique_values=91,
                null_count=0,
                sample_data=["RI-540", "RI-539"],
                description="Reference Purchase Order Number"
            ),
            ColumnInfo(
                name="Bill Number",
                data_type="int64",
                unique_values=85,
                null_count=0,
                sample_data=["1431", "1430"],
                description="Vendor Bill/Invoice Number"
            ),
            ColumnInfo(
                name="Party Name",
                data_type="object",
                unique_values=16,
                null_count=0,
                sample_data=["Passary Minerals Rourkela", "Passary Minerals Rourkela"],
                description="Supplier Name"
            ),
            ColumnInfo(
                name="Product Name",
                data_type="object",
                unique_values=52,
                null_count=0,
                sample_data=["P14 Clinker", "99 C Fired"],
                description="Received Product Name"
            ),
            ColumnInfo(
                name="Date Of Receiving",
                data_type="datetime64[ns]",
                unique_values=44,
                null_count=0,
                sample_data=["2023-01-09", "2023-01-13"],
                description="Date material was received"
            ),
            ColumnInfo(
                name="Total Bill Quantity",
                data_type="float64",
                unique_values=127,
                null_count=0,
                sample_data=["8.36", "4.82"],
                description="Quantity claimed in bill (MT)"
            ),
            ColumnInfo(
                name="Actual Quantity",
                data_type="float64",
                unique_values=158,
                null_count=0,
                sample_data=["8.36", "4.82"],
                description="Actual quantity verified (MT)"
            ),
            ColumnInfo(
                name="Qty Difference",
                data_type="float64",
                unique_values=65,
                null_count=0,
                sample_data=["0.0", "0.0"],
                description="Difference between billed and actual quantity"
            ),
            ColumnInfo(
                name="Physical Condition",
                data_type="object",
                unique_values=1,
                null_count=0,
                sample_data=["Good"],
                description="Condition of material (Good/Bad)"
            ),
            ColumnInfo(
                name="Moisture",
                data_type="object",
                unique_values=1,
                null_count=0,
                sample_data=["No"],
                description="Moisture content presence (Yes/No)"
            ),
            ColumnInfo(
                name="Physical Image Of Product",
                data_type="object",
                unique_values=195,
                null_count=1,
                sample_data=["https://drive.google.com/open?", "https://drive.google.com/open?"],
                description="Photo evidence of material"
            ),
            ColumnInfo(
                name="Image Of Weight Slip",
                data_type="object",
                unique_values=195,
                null_count=1,
                sample_data=["https://drive.google.com/open?", "https://drive.google.com/open?"],
                description="Photo evidence of weight slip"
            )
        ]


class OrdersPendingTool(BaseSheetTool):
    """
    Orders Pending Sheet Tool - Sales Order Backlog
    ===============================================
    
    Purpose:
        Manages outgoing sales orders that have not yet been fully delivered.
        Tracks order details, party information, specs, and delivery status.
    
    Key Features:
        - Delivery Order (DO) tracking
        - Party PO reference
        - Technical specs (Alumina, Iron %)
        - Payment terms and lead times
        - Delivery status tracking
    
    Statistics:
        - Total Rows: 1,773
        - Total Columns: 24
        - Active Orders: High volume
        - Unique Parties: 131
    """
    
    def __init__(self):
        super().__init__()
        self.sheet_name = "Orders Pending"
        self.purpose = "Sales orders awaiting fulfillment"
        self.total_rows = 1773
        self.total_columns = 24
        
        self.columns = [
            ColumnInfo(
                name="Timestamp",
                data_type="object",
                unique_values=1320,
                null_count=0,
                sample_data=["2022-12-24 13:35:06"],
                description="Order entry time"
            ),
            ColumnInfo(
                name="DO-Delivery Order No.",
                data_type="object",
                unique_values=1773,
                null_count=0,
                sample_data=["DO-959", "DO-960"],
                description="Internal Delivery Order Number"
            ),
            ColumnInfo(
                name="PARTY PO NO (As Per Po Exact)",
                data_type="object",
                unique_values=1078,
                null_count=0,
                sample_data=["SURYADEV/PASSARY/CASTABLES/PO/"],
                description="Customer Purchase Order Number"
            ),
            ColumnInfo(
                name="Party PO Date",
                data_type="object",
                unique_values=640,
                null_count=0,
                sample_data=["2022-05-28"],
                description="Date of customer PO"
            ),
            ColumnInfo(
                name="Party Names",
                data_type="object",
                unique_values=131,
                null_count=0,
                sample_data=["Suryadev Alloys And Power Priv"],
                description="Customer Name"
            ),
            ColumnInfo(
                name="Product Name",
                data_type="object",
                unique_values=156,
                null_count=0,
                sample_data=["Insulation Pad", "High Cast Special"],
                description="Ordered Product Name"
            ),
            ColumnInfo(
                name="Quantity",
                data_type="float64",
                unique_values=253,
                null_count=0,
                sample_data=["2.0", "56.0"],
                description="Ordered Quantity"
            ),
            ColumnInfo(
                name="Rate Of Material",
                data_type="object",
                unique_values=420,
                null_count=0,
                sample_data=["29500", "49700"],
                description="Unit Rate"
            ),
            ColumnInfo(
                name="Type Of Transporting",
                data_type="object",
                unique_values=3,
                null_count=1,
                sample_data=["For"],
                description="Transport terms (FOR/Ex-Works)"
            ),
            ColumnInfo(
                name="Upload SO",
                data_type="object",
                unique_values=1267,
                null_count=1,
                sample_data=["https://drive.google.com/open?"],
                description="Sales Order document link"
            ),
            ColumnInfo(
                name="Is This Order Through Some Agent",
                data_type="object",
                unique_values=2,
                null_count=11,
                sample_data=["No"],
                description="Agent involvement flag"
            ),
            ColumnInfo(
                name="Order Received From",
                data_type="object",
                unique_values=3,
                null_count=0,
                sample_data=["NBD & NBD OF CRR FMS"],
                description="Source of order"
            ),
            ColumnInfo(
                name="Type Of Measurement",
                data_type="object",
                unique_values=6,
                null_count=0,
                sample_data=["PCS", "MT"],
                description="Unit of Measurement"
            ),
            ColumnInfo(
                name="Contact Person Name",
                data_type="object",
                unique_values=429,
                null_count=1,
                sample_data=["MR. K SHIVA PRADEEP JI"],
                description="Customer contact person"
            ),
            ColumnInfo(
                name="Alumina%",
                data_type="object",
                unique_values=119,
                null_count=337,
                sample_data=["73-76"],
                description="Alumina content specification"
            ),
            ColumnInfo(
                name="Iron%",
                data_type="object",
                unique_values=117,
                null_count=322,
                sample_data=["1.5-1.8"],
                description="Iron content specification"
            ),
            ColumnInfo(
                name="Type Of PI",
                data_type="object",
                unique_values=5,
                null_count=6,
                sample_data=["Partly Advance Partly PI"],
                description="Payment terms type"
            ),
            ColumnInfo(
                name="Quantity Delivered",
                data_type="float64",
                unique_values=347,
                null_count=0,
                sample_data=["0.0", "56.0"],
                description="Quantity already delivered"
            ),
            ColumnInfo(
                name="Pending Qty",
                data_type="float64",
                unique_values=191,
                null_count=0,
                sample_data=["0.0"],
                description="Quantity yet to be delivered"
            ),
            ColumnInfo(
                name="Status",
                data_type="object",
                unique_values=2,
                null_count=0,
                sample_data=["Complete"],
                description="Order status"
            )
        ]


class SalesInvoicesTool(BaseSheetTool):
    """
    Sales Invoices Sheet Tool - Dispatched Orders
    =============================================
    
    Purpose:
        Records completed sales transactions and generated invoices.
        Tracks logistics, transporters, and delivered quantities.
    
    Key Features:
        - Invoice/Bill tracking
        - Logistics management (Transporter, Vehicle No)
        - Delivery confirmation
        - Financial record of sales
    
    Statistics:
        - Total Rows: 4,610
        - Total Columns: 12
    """
    
    def __init__(self):
        super().__init__()
        self.sheet_name = "Sales Invoices"
        self.purpose = "Completed sales invoices"
        self.total_rows = 4610
        self.total_columns = 12
        
        self.columns = [
            ColumnInfo(
                name="Timestamp",
                data_type="datetime64[ns]",
                unique_values=4610,
                null_count=0,
                sample_data=["2022-12-27 11:27:16"],
                description="Invoice creation time"
            ),
            ColumnInfo(
                name="Bill Date",
                data_type="datetime64[ns]",
                unique_values=947,
                null_count=0,
                sample_data=["2022-12-27"],
                description="Date of invoice"
            ),
            ColumnInfo(
                name="Delivery Order No.",
                data_type="object",
                unique_values=1681,
                null_count=0,
                sample_data=["DO-969"],
                description="Linked Delivery Order Number"
            ),
            ColumnInfo(
                name="Party Name",
                data_type="object",
                unique_values=128,
                null_count=0,
                sample_data=["Shree Shyam Sponge & Power Ltd"],
                description="Customer Name"
            ),
            ColumnInfo(
                name="Product Name",
                data_type="object",
                unique_values=148,
                null_count=0,
                sample_data=["LCM - 70 AR"],
                description="Sold Product Name"
            ),
            ColumnInfo(
                name="Quantity Delivered.",
                data_type="float64",
                unique_values=500,
                null_count=0,
                sample_data=["10.0"],
                description="Invoiced Quantity in MT"
            ),
            ColumnInfo(
                name="Bill No.",
                data_type="object",
                unique_values=1452,
                null_count=0,
                sample_data=["579", "580"],
                description="Invoice Number"
            ),
            ColumnInfo(
                name="Losgistic no.",
                data_type="object",
                unique_values=4604,
                null_count=0,
                sample_data=["LGST-854"],
                description="Logistics tracking number"
            ),
            ColumnInfo(
                name="Rate Of Material",
                data_type="float64",
                unique_values=286,
                null_count=0,
                sample_data=["39070.0"],
                description="Sold Rate per MT"
            ),
            ColumnInfo(
                name="Transporter Name",
                data_type="object",
                unique_values=73,
                null_count=937,
                sample_data=["Owned Truck"],
                description="Name of transporter"
            ),
            ColumnInfo(
                name="Vehicle Number.",
                data_type="object",
                unique_values=1365,
                null_count=0,
                sample_data=["CG04NT2527"],
                description="Vehicle registration number"
            )
        ]


class ProductionOrdersTool(BaseSheetTool):
    """
    Production Orders Sheet Tool - Manufacturing Schedule
    =====================================================
    
    Purpose:
        Manages production requests and manufacturing schedules.
        Tracks production planning, execution, and stock transfers.
    
    Key Features:
        - Production planning
        - Order to production mapping
        - Actual vs Planned production
        - Stock transfer tracking
        - Production status monitoring
    
    Statistics:
        - Total Rows: 851
        - Total Columns: 16
    """
    
    def __init__(self):
        super().__init__()
        self.sheet_name = "Production Orders"
        self.purpose = "Manufacturing orders and schedules"
        self.total_rows = 851
        self.total_columns = 16
        
        self.columns = [
            ColumnInfo(
                name="Timestamp",
                data_type="datetime64[ns]",
                unique_values=851,
                null_count=0,
                sample_data=["2023-01-04 12:53:05"],
                description="Order creation time"
            ),
            ColumnInfo(
                name="Delivery Order No.",
                data_type="object",
                unique_values=849,
                null_count=0,
                sample_data=["DO-985"],
                description="Linked Delivery Order"
            ),
            ColumnInfo(
                name="Party Name",
                data_type="object",
                unique_values=106,
                null_count=0,
                sample_data=["Singhal Enterprises Pvt Ltd."],
                description="Customer Name"
            ),
            ColumnInfo(
                name="Product Name",
                data_type="object",
                unique_values=84,
                null_count=0,
                sample_data=["Pasheat - C"],
                description="Product to manufacture"
            ),
            ColumnInfo(
                name="Order Quantity",
                data_type="float64",
                unique_values=178,
                null_count=0,
                sample_data=["20.0"],
                description="Required Quantity"
            ),
            ColumnInfo(
                name="Expected Delivery Date",
                data_type="datetime64[ns]",
                unique_values=415,
                null_count=0,
                sample_data=["2023-01-05"],
                description="Target completion date"
            ),
            ColumnInfo(
                name="Actual Production Planned",
                data_type="float64",
                unique_values=255,
                null_count=0,
                sample_data=["20.0"],
                description="Planned production quantity"
            ),
            ColumnInfo(
                name="Actual Production Done",
                data_type="float64",
                unique_values=336,
                null_count=0,
                sample_data=["20.6"],
                description="Completed production quantity"
            ),
            ColumnInfo(
                name="Quantity In Stock",
                data_type="float64",
                unique_values=328,
                null_count=0,
                sample_data=["0.6"],
                description="Available stock quantity"
            ),
            ColumnInfo(
                name="Production Pending",
                data_type="float64",
                unique_values=174,
                null_count=0,
                sample_data=["-0.6"],
                description="Quantity remaining to produce"
            ),
            ColumnInfo(
                name="Status",
                data_type="object",
                unique_values=2,
                null_count=0,
                sample_data=["Complete"],
                description="Production status"
            )
        ]


class JobCardProductionTool(BaseSheetTool):
    """
    Job Card Production Sheet Tool - Daily Mfg Records
    ==================================================
    
    Purpose:
        Detailed records of daily production jobs. Tracks supervisor
        responsibility and specific batch outputs.
    
    Key Features:
        - Job Card tracking
        - Supervisor assignment
        - Daily production logging
        - Batch quantity records
    
    Statistics:
        - Total Rows: 198
        - Total Columns: 8
    """
    
    def __init__(self):
        super().__init__()
        self.sheet_name = "Job Card Production"
        self.purpose = "Detailed production job tracking"
        self.total_rows = 198
        self.total_columns = 8
        
        self.columns = [
            ColumnInfo(
                name="Timestamp",
                data_type="datetime64[ns]",
                unique_values=198,
                null_count=0,
                sample_data=["2023-01-04 13:57:22"],
                description="Entry timestamp"
            ),
            ColumnInfo(
                name="Do Number",
                data_type="object",
                unique_values=70,
                null_count=0,
                sample_data=["DO-981"],
                description="Delivery Order Reference"
            ),
            ColumnInfo(
                name="Party Name",
                data_type="object",
                unique_values=34,
                null_count=0,
                sample_data=["V Raj Metaliks Pvt Ltd"],
                description="Client Name"
            ),
            ColumnInfo(
                name="Job Card No.",
                data_type="object",
                unique_values=145,
                null_count=0,
                sample_data=["JC-1217"],
                description="Unique Job Card Identifier"
            ),
            ColumnInfo(
                name="Date Of Production",
                data_type="datetime64[ns]",
                unique_values=80,
                null_count=0,
                sample_data=["2022-12-31"],
                description="Date production occurred"
            ),
            ColumnInfo(
                name="Name Of Supervisor",
                data_type="object",
                unique_values=3,
                null_count=0,
                sample_data=["Anand Vaishnav"],
                description="Supervisor on duty"
            ),
            ColumnInfo(
                name="Product Name",
                data_type="object",
                unique_values=17,
                null_count=0,
                sample_data=["Pasheat - C"],
                description="Manufactured Product"
            ),
            ColumnInfo(
                name="Quantity Of FG",
                data_type="float64",
                unique_values=44,
                null_count=0,
                sample_data=["4.12"],
                description="Quantity of Finished Goods produced"
            )
        ]