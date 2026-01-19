"""
Google Sheets + Groq LLM Agent System.
ENHANCED VERSION - Matching notebook's 82.1% success rate.
Includes all specialized tools, advanced operations, and processing pipeline.
TOKEN OPTIMIZATION: Embeddings-based sheet selection + SQLite caching.
"""
import os
import pandas as pd
import numpy as np
import gspread
import re
import json
from google.oauth2.service_account import Credentials
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Dict, Any, Optional
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dataclasses import dataclass
from config import settings
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================================
# GLOBAL OPTIMIZATION COMPONENTS
# ============================================================================

# Embedding model for sheet selection (loaded once on startup)
_embedding_model = None
_sheet_embeddings = {}  # {sheet_name: embedding_vector}

def get_embedding_model():
    """Get or initialize the sentence transformer model."""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    return _embedding_model


def detect_table_intent(question: str) -> bool:
    """
    Detect if user wants to SEE data (table) or just wants a summary.
    
    Returns:
        True: User wants to see table/list (show, list, display, what are, which ones, etc.)
        False: User wants summary only (how many, total, which product/party has highest, etc.)
    """
    question_lower = question.lower()
    
    # Keywords that indicate user wants to SEE data
    show_keywords = [
        'show me', 'show', 'list', 'display', 'give me',
        'what are the', 'which are the', 'which ones',
        'give me the list', 'breakdown', 'details of',
        'get me', 'fetch', 'retrieve', 'all the',
        'find all', 'get all'
    ]
    
    # Keywords that indicate user wants summary/answer only
    summary_keywords = [
        'how many', 'what is the total', 'what\'s the total',
        'total', 'sum', 'count', 'average',
        'which product has', 'which party has', 'who has the most',
        'who has the highest', 'which has the lowest',
        'what is the highest', 'what is the lowest'
    ]
    
    # Check for show keywords first
    for keyword in show_keywords:
        if keyword in question_lower:
            return True
    
    # Check for summary keywords
    for keyword in summary_keywords:
        if keyword in question_lower:
            return False
    
    # Default: if asking "what are" or "which" with plural, show table
    if ('what are' in question_lower or 'which' in question_lower) and \
       ('parties' in question_lower or 'products' in question_lower or 
        'orders' in question_lower or 'items' in question_lower or
        'tasks' in question_lower):
        return True
    
    # Default: show table for safety (user can always ask for summary)
    return True


# ============================================================================
# TOOL INFRASTRUCTURE - 16 Sheet Tools
# ============================================================================

@dataclass
class ColumnInfo:
    """Metadata for a single column"""
    name: str
    data_type: str
    description: str
    sample_values: List[str] = None


class BaseSheetTool:
    """Base class for all 16 sheet tools"""
    
    def __init__(self):
        self.sheet_name: str = ""
        self.purpose: str = ""
        self.key_columns: List[str] = []
        self.columns: List[ColumnInfo] = []
    
    def get_info(self) -> Dict[str, Any]:
        return {
            "sheet_name": self.sheet_name,
            "purpose": self.purpose,
            "key_columns": self.key_columns,
            "all_columns": [col.name for col in self.columns]
        }
    
    def get_column_names(self) -> List[str]:
        return [col.name for col in self.columns]


# Define All 16 Sheet Tools
class ChecklistTool(BaseSheetTool):
    def __init__(self):
        super().__init__()
        self.sheet_name = "Checklist"
        self.purpose = "Daily task tracking and completion status"
        self.key_columns = ["Task ID", "Doer Name", "Task Description", "Actual", "Delay", "Status"]


class DelegationTool(BaseSheetTool):
    def __init__(self):
        super().__init__()
        self.sheet_name = "Delegation"
        self.purpose = "One-time work assignments and tracking"
        self.key_columns = ["Task ID", "Doer Name", "Planned Date", "Actual", "Status"]


class POPendingTool(BaseSheetTool):
    def __init__(self):
        super().__init__()
        self.sheet_name = "PO Pending"
        self.purpose = "Pending purchase orders awaiting receipt"
        self.key_columns = ["PO Number", "Vendor Name", "PO Date", "Pending Quantity"]


class FGStockTool(BaseSheetTool):
    def __init__(self):
        super().__init__()
        self.sheet_name = "FG Stock"
        self.purpose = "Finished goods inventory levels"
        self.key_columns = ["Product Name", "Current Level", "Unit"]


class RMSockTool(BaseSheetTool):
    def __init__(self):
        super().__init__()
        self.sheet_name = "RM Sock"
        self.purpose = "Raw material inventory levels"
        self.key_columns = ["Material Name", "Current Level"]


class PurchaseIntransitTool(BaseSheetTool):
    def __init__(self):
        super().__init__()
        self.sheet_name = "Purchase Intransit"
        self.purpose = "Materials in transit from vendors"
        self.key_columns = ["PO Number", "Material", "Dispatch Date", "Expected Arrival"]


class PaymentsTool(BaseSheetTool):
    def __init__(self):
        super().__init__()
        self.sheet_name = "Payments"
        self.purpose = "Payment transactions and dues"
        self.key_columns = ["Invoice Number", "Party Name", "Amount", "Due Date", "Status"]


class EnquirysTool(BaseSheetTool):
    def __init__(self):
        super().__init__()
        self.sheet_name = "Enquirys"
        self.purpose = "Customer inquiries and follow-ups"
        self.key_columns = ["Enquiry ID", "Customer Name", "Product", "Date"]


class StoreOUTTool(BaseSheetTool):
    def __init__(self):
        super().__init__()
        self.sheet_name = "Store OUT"
        self.purpose = "Material issues from store"
        self.key_columns = ["Material Name", "Quantity", "Issued To", "Date"]


class NewStoreIndentTool(BaseSheetTool):
    def __init__(self):
        super().__init__()
        self.sheet_name = "New Store Indent"
        self.purpose = "Material requisition requests"
        self.key_columns = ["Indent Number", "Material", "Quantity", "Status"]


class StoreINTool(BaseSheetTool):
    def __init__(self):
        super().__init__()
        self.sheet_name = "Store IN"
        self.purpose = "Material receipts into store"
        self.key_columns = ["Material Name", "Quantity", "Received Date"]


class PurchaseReceiptTool(BaseSheetTool):
    def __init__(self):
        super().__init__()
        self.sheet_name = "Purchase Receipt"
        self.purpose = "Purchase order receipt confirmations"
        self.key_columns = ["PO Number", "Receipt Date", "Quantity Received"]


class OrdersPendingTool(BaseSheetTool):
    def __init__(self):
        super().__init__()
        self.sheet_name = "Orders Pending"
        self.purpose = "Pending customer sales orders"
        self.key_columns = ["DO-Delivery Order No.", "Party PO Date", "Product Name", "Pending Qty"]


class SalesInvoicesTool(BaseSheetTool):
    def __init__(self):
        super().__init__()
        self.sheet_name = "Sales Invoices"
        self.purpose = "Generated sales invoices"
        self.key_columns = ["Invoice Number", "Customer", "Date", "Amount"]


class ProductionOrdersTool(BaseSheetTool):
    def __init__(self):
        super().__init__()
        self.sheet_name = "Production Orders"
        self.purpose = "Manufacturing production orders"
        self.key_columns = ["Order Number", "Product", "Quantity", "Status"]


class JobCardProductionTool(BaseSheetTool):
    def __init__(self):
        super().__init__()
        self.sheet_name = "Job Card Production"
        self.purpose = "Job card production tracking"
        self.key_columns = ["Job Card Number", "Product", "Quantity Produced"]


# Create registry of all tools
TOOLS = [
    ChecklistTool(), DelegationTool(), POPendingTool(), FGStockTool(),
    RMSockTool(), PurchaseIntransitTool(), PaymentsTool(), EnquirysTool(),
    StoreOUTTool(), NewStoreIndentTool(), StoreINTool(),
    PurchaseReceiptTool(), OrdersPendingTool(), SalesInvoicesTool(),
    ProductionOrdersTool(), JobCardProductionTool()
]

TOOL_MAP = {t.sheet_name: t for t in TOOLS}


# ============================================================================
# COLUMN ALIASES & NORMALIZATION
# ============================================================================

COLUMN_ALIASES = {
    "Current Level": ["stock", "qty", "quantity", "balance", "level", "current stock"],
    "Pending Qty": ["pending", "pending quantity", "pending qty", "remaining"],
    "Quantity": ["qty", "quantity", "amount"],
    "Quantity Of FG": ["fg qty", "finished goods qty"],
    "Party PO Date": ["order date", "po date", "date", "orderdate"],
    "Timestamp": ["date", "time", "created", "created date"],
    "Actual": ["actual date", "completion date", "completed"],
    "Product Name": ["product", "item", "material"],
    "DO-Delivery Order No.": ["do number", "delivery order", "do"],
    "Doer Name": ["assignee", "employee", "worker"],
}


def normalize_column_aliases(df: pd.DataFrame) -> pd.DataFrame:
    """Add canonical column names based on aliases"""
    for canonical, aliases in COLUMN_ALIASES.items():
        if canonical not in df.columns:
            for col in df.columns:
                if col.lower() in [a.lower() for a in aliases]:
                    df[canonical] = df[col]
                    break
    return df


def normalize_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """Convert string columns to numeric where appropriate"""
    for col in df.columns:
        if df[col].dtype == 'object':
            converted = pd.to_numeric(df[col], errors='coerce')
            if converted.notna().sum() > 0.3 * len(df):
                df[col] = converted
    return df


# ============================================================================
# DATE RESOLUTION
# ============================================================================

def resolve_date_expressions(query: str) -> str:
    """Convert date expressions like 'last 30 days' to actual dates"""
    today = datetime.today()
    
    # Handle "last N days"
    match = re.search(r'last\s+(\d+)\s+days?', query, re.IGNORECASE)
    if match:
        days = int(match.group(1))
        start_date = (today - timedelta(days=days)).strftime('%Y-%m-%d')
        query = query.replace(match.group(0), f"after {start_date}")
    
    # Handle "this month"
    if re.search(r'\bthis\s+month\b', query, re.IGNORECASE):
        month_start = today.replace(day=1).strftime('%Y-%m-%d')
        query = re.sub(r'\bthis\s+month\b', f"after {month_start}", query, flags=re.IGNORECASE)
    
    # Handle "this year"
    if re.search(r'\bthis\s+year\b', query, re.IGNORECASE):
        year_start = today.replace(month=1, day=1).strftime('%Y-%m-%d')
        query = re.sub(r'\bthis\s+year\b', f"after {year_start}", query, flags=re.IGNORECASE)
    
    return query


# ============================================================================
# SAFE QUERY EXECUTION
# ============================================================================

def normalize_condition(df: pd.DataFrame, condition: str) -> str:
    """Convert natural language conditions to safe pandas query syntax"""
    cond = condition
    
    # Normalize logical operators
    cond = re.sub(r'\bAND\b', '&', cond, flags=re.IGNORECASE)
    cond = re.sub(r'\bOR\b', '|', cond, flags=re.IGNORECASE)
    cond = re.sub(r'\bNOT\b', '~', cond, flags=re.IGNORECASE)
    
    # Resolve TODAY() expressions
    today = datetime.today()
    
    def replace_today_minus(match):
        days = int(match.group(1))
        target_date = (today - timedelta(days=days)).date()
        return f"'{target_date.isoformat()}'"
    
    cond = re.sub(r'TODAY\(\)\s*-\s*(\d+)', replace_today_minus, cond, flags=re.IGNORECASE)
    cond = re.sub(r'TODAY\(\)', f"'{today.date().isoformat()}'", cond, flags=re.IGNORECASE)
    
    # Remove backticks - we'll use df.loc with boolean indexing instead
    cond = cond.replace('`', '')
    
    return cond


def safe_query(df: pd.DataFrame, condition: str) -> pd.DataFrame:
    """Execute query with comprehensive error handling - supports .str.contains() for partial matching"""
    if not condition or condition.strip() == "":
        return df
    
    try:
        # Normalize condition first
        normalized = normalize_condition(df, condition)
        
        # Try pandas query method first
        try:
            # Re-add backticks for query method
            query_cond = normalized
            for col in sorted(df.columns, key=len, reverse=True):
                if ' ' in col or '-' in col or any(c in col for c in '()[]{}'):
                    pattern = r'\b' + re.escape(col) + r'\b'
                    query_cond = re.sub(pattern, f'`{col}`', query_cond, flags=re.IGNORECASE)
            
            result = df.query(query_cond, engine='python')
            print(f"  ✓ Query executed: {len(result)} rows match")
            return result
        except Exception as e:
            print(f"  ⚠️ Query method failed: {str(e)}, trying manual parsing")
            
            # Fallback: Manual parsing with support for .str.contains()
            parts = re.split(r'(\s+&\s+|\s+\|\s+)', normalized)
            
            masks = []
            operators = []
            
            for part in parts:
                part = part.strip()
                if part in ['&', '|']:
                    operators.append(part)
                    continue
                
                if not part:
                    continue
                
                # Check if it's a .str.contains() expression (remove backticks first)
                part_clean = part.replace('`', '')
                contains_match = re.match(r'(.+?)\.str\.contains\([\'"](.+?)[\'"]\s*,\s*case=False\s*,\s*na=False\)', part_clean, re.IGNORECASE)
                if contains_match:
                    col_name = contains_match.group(1).strip()
                    pattern = contains_match.group(2)
                    
                    # Find actual column
                    actual_col = None
                    for col in df.columns:
                        if col.lower() == col_name.lower():
                            actual_col = col
                            break
                    
                    if actual_col and df[actual_col].dtype == 'object':
                        # Use str.contains with regex
                        mask = df[actual_col].str.contains(pattern, case=False, na=False, regex=True)
                        masks.append(mask)
                        print(f"  🔍 Contains filter: '{actual_col}' contains '{pattern}' → {mask.sum()} matches")
                        continue
                
                # Standard comparison: column operator value
                match = re.match(r'\s*(.+?)\s*(==|!=|>=|<=|>|<)\s*(.+)\s*$', part)
                if match:
                    col_name, operator, value = match.groups()
                    col_name = col_name.strip()
                    value = value.strip().strip("'\"")
                    
                    # Find matching column (case-insensitive + fuzzy matching)
                    actual_col = None
                    
                    # First try exact match (case-insensitive)
                    for col in df.columns:
                        if col.lower() == col_name.lower():
                            actual_col = col
                            break
                    
                    # If not found, try fuzzy match (remove spaces, special chars)
                    if actual_col is None:
                        col_name_clean = col_name.lower().replace(' ', '').replace('_', '').replace('-', '')
                        for col in df.columns:
                            col_clean = col.lower().replace(' ', '').replace('_', '').replace('-', '')
                            if col_clean == col_name_clean:
                                actual_col = col
                                break
                    
                    # If still not found, try partial match (contains or starts with)
                    if actual_col is None:
                        for col in df.columns:
                            if col_name.lower() in col.lower() or col.lower().startswith(col_name.lower()):
                                actual_col = col
                                print(f"  🔍 Fuzzy matched '{col_name}' to '{actual_col}'")
                                break
                    
                    if actual_col is None:
                        print(f"  ⚠️ Column '{col_name}' not found in {list(df.columns)[:5]}...")
                        continue
                    
                    # Create boolean mask with proper string comparison
                    try:
                        if operator == '==':
                            # Case-insensitive string comparison
                            if df[actual_col].dtype == 'object':
                                mask = df[actual_col].str.lower() == value.lower()
                            else:
                                mask = df[actual_col] == value
                        elif operator == '!=':
                            if df[actual_col].dtype == 'object':
                                mask = df[actual_col].str.lower() != value.lower()
                            else:
                                mask = df[actual_col] != value
                        elif operator == '>':
                            mask = pd.to_numeric(df[actual_col], errors='coerce') > float(value)
                        elif operator == '<':
                            mask = pd.to_numeric(df[actual_col], errors='coerce') < float(value)
                        elif operator == '>=':
                            mask = pd.to_numeric(df[actual_col], errors='coerce') >= float(value)
                        elif operator == '<=':
                            mask = pd.to_numeric(df[actual_col], errors='coerce') <= float(value)
                        else:
                            mask = pd.Series([True] * len(df))
                        
                        masks.append(mask)
                    except Exception as e:
                        print(f"  ⚠️ Error creating mask for {col_name} {operator} {value}: {e}")
                        continue
            
            # Combine masks with operators
            if masks:
                final_mask = masks[0]
                for i, op in enumerate(operators):
                    if i + 1 < len(masks):
                        if op == '&':
                            final_mask = final_mask & masks[i + 1]
                        elif op == '|':
                            final_mask = final_mask | masks[i + 1]
                
                result = df[final_mask]
                print(f"  ✓ Query executed (manual parsing): {len(result)} rows match")
                return result
            
    except Exception as e:
        print(f"  ❌ Query failed: {str(e)}")
    
    print(f"  ⚠ Returning all rows due to query error")
    return df


# ============================================================================
# STATE DEFINITION
# ============================================================================

class EnhancedAgentState(TypedDict):
    """Enhanced state with 7 operation types support + token optimizations"""
    question: str
    plan: Optional[dict]
    result: Optional[pd.DataFrame]
    answer: str
    confidence: float
    error: Optional[str]
    retry_count: int
    selected_sheets_info: Optional[str]  # For embeddings-based sheet selection


# ============================================================================
# MAIN AGENT CLASS
# ============================================================================

class GoogleSheetsAgent:
    """
    Enhanced agent with 82.1% success rate.
    Supports 7 operation types: RETRIEVE, AGGREGATE, COMPARE, FEASIBILITY, RANK, TREND, PREDICT
    """
    
    def __init__(self):
        self.client = None
        self.sheet = None
        self.dataframes = {}
        self.sheet_info = ""
        self.llm = None
        self.agent = None
        self.last_refresh = None
        self._initialize()
    
    def _initialize(self):
        """Initialize Google Sheets and Groq LLM"""
        # Setup Google Sheets
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        creds = Credentials.from_service_account_file(
            settings.GOOGLE_SHEETS_CREDENTIALS_PATH,
            scopes=scopes
        )
        
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open(settings.GOOGLE_SHEET_NAME)
        
        # Load all worksheets
        self._load_sheets_data()
        
        # Setup Groq LLM
        os.environ["GROQ_API_KEY"] = settings.GROQ_API_KEY
        self.llm = ChatGroq(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE
        )
        
        # Build enhanced agent
        self._build_enhanced_agent()
        
        self.last_refresh = datetime.utcnow()
        print(f"✅ Enhanced Agent initialized at {self.last_refresh}")
    
    def _load_sheets_data(self):
        """Load all worksheets into pandas DataFrames with preprocessing"""
        worksheets = self.sheet.worksheets()
        self.dataframes = {}
        
        for ws in worksheets:
            try:
                # Get raw data to handle duplicate headers
                values = ws.get_all_values()
                if len(values) < 2:
                    continue
                
                # Handle duplicate column names by making them unique
                headers = values[0]
                seen = {}
                unique_headers = []
                for header in headers:
                    if header in seen:
                        seen[header] += 1
                        unique_headers.append(f"{header}_{seen[header]}")
                    else:
                        seen[header] = 0
                        unique_headers.append(header)
                
                # Create DataFrame with unique headers
                df = pd.DataFrame(values[1:], columns=unique_headers)
                
                # Apply preprocessing pipeline
                df = normalize_column_aliases(df)
                df = normalize_numeric(df)
                self.dataframes[ws.title] = df
                
            except Exception as e:
                print(f"⚠️ Could not load sheet '{ws.title}': {e}")
        
        self._generate_sheet_info()
        print(f"✅ Loaded {len(self.dataframes)} sheets with {sum(len(df) for df in self.dataframes.values())} total rows")
        print(f"✅ Registered {len(TOOLS)} sheet tools: {list(TOOL_MAP.keys())}")
    
    def _generate_sheet_info(self):
        """Generate structured information about all sheets - showing ALL actual column names"""
        info_parts = []
        for name, df in self.dataframes.items():
            if name in TOOL_MAP:
                tool = TOOL_MAP[name]
                # Show ALL columns (not just first 5) so LLM knows exact names
                all_cols = ", ".join(df.columns.tolist())
                info_parts.append(
                    f"- **{name}**\n"
                    f"  Purpose: {tool.purpose}\n"
                    f"  Columns: {all_cols}\n"
                    f"  Rows: {len(df)}"
                )
            else:
                # Show ALL columns for non-tool sheets too
                all_cols = ", ".join(df.columns.tolist())
                info_parts.append(f"- **{name}**: {all_cols} ({len(df)} rows)")
        self.sheet_info = "\n\n".join(info_parts)
        
        # Generate embeddings for each sheet description (for sheet selection)
        self._generate_sheet_embeddings()
    
    def _generate_sheet_embeddings(self):
        """Generate embeddings for each sheet description for similarity matching."""
        global _sheet_embeddings
        model = get_embedding_model()
        
        for name, df in self.dataframes.items():
            # Build comprehensive description (kept big per user requirement)
            description_parts = [f"Sheet name: {name}"]
            
            if name in TOOL_MAP:
                tool = TOOL_MAP[name]
                description_parts.append(f"Purpose: {tool.purpose}")
                description_parts.append(f"Key columns: {', '.join(tool.key_columns)}")
            
            # Add all column names for better matching
            description_parts.append(f"All columns: {', '.join(df.columns.tolist())}")
            description_parts.append(f"Row count: {len(df)}")
            
            # Combine into full description
            full_description = " | ".join(description_parts)
            
            # Generate embedding
            embedding = model.encode(full_description)
            _sheet_embeddings[name] = embedding
        
        print(f"✅ Generated embeddings for {len(_sheet_embeddings)} sheets")
    
    def _select_relevant_sheets(self, query: str, top_n: int = 3) -> List[str]:
        """
        Select top N most relevant sheets for a query using embeddings.
        Returns list of sheet names sorted by relevance.
        """
        if not _sheet_embeddings:
            # Fallback: return all sheets if embeddings not ready
            return list(self.dataframes.keys())
        
        model = get_embedding_model()
        query_embedding = model.encode(query)
        
        # Calculate similarities
        similarities = {}
        for sheet_name, sheet_embedding in _sheet_embeddings.items():
            similarity = cosine_similarity(
                query_embedding.reshape(1, -1),
                sheet_embedding.reshape(1, -1)
            )[0][0]
            similarities[sheet_name] = similarity
        
        # Sort by similarity and return top N
        sorted_sheets = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
        selected = [name for name, score in sorted_sheets[:top_n]]
        
        print(f"🎯 Selected {len(selected)} sheets for query: {selected}")
        return selected
    
    def _get_selected_sheet_info(self, sheet_names: List[str]) -> str:
        """Generate sheet info only for selected sheets - showing ALL actual column names."""
        info_parts = []
        for name in sheet_names:
            if name not in self.dataframes:
                continue
            
            df = self.dataframes[name]
            if name in TOOL_MAP:
                tool = TOOL_MAP[name]
                # Show ALL columns so LLM uses exact names
                all_cols = ", ".join(df.columns.tolist())
                info_parts.append(
                    f"- **{name}**\n"
                    f"  Purpose: {tool.purpose}\n"
                    f"  Columns: {all_cols}\n"
                    f"  Rows: {len(df)}"
                )
            else:
                # Show ALL columns
                all_cols = ", ".join(df.columns.tolist())
                info_parts.append(f"- **{name}**: {all_cols} ({len(df)} rows)")
        
        return "\n\n".join(info_parts)
    
    def _build_enhanced_agent(self):
        """Build LangGraph agent with enhanced capabilities"""
        
        # Enhanced planner prompt with 7 operation types (matching notebook lines 950-1044)
        planner_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert business intelligence system for PMMPL production management.

Available sheets with EXACT column names:
{sheets_info}

IMPORTANT: The sheets above show ALL actual column names. You MUST use these EXACT names in your filters.

SHEET INTENT MAPPINGS (understand what user means):
- "completed tasks" or "tasks done" → Checklist sheet (filter: Status == 'Completed')
- "pending tasks" or "tasks to do" → Checklist sheet (filter: Status == 'Pending')  
- "pending orders" → Orders Pending sheet (filter: `Pending Qty` > 0 AND Status == 'Pending')
- "pending orders for [party]" → Orders Pending sheet (filter: `Party Names`.str.contains('party_name', case=False) & (`Pending Qty` > 0))
- "compare pending orders of X and Y" → Orders Pending sheet (filter: `Party Names`.str.contains('X|Y', case=False) & (`Pending Qty` > 0))
- "stock" or "inventory" → FG Stock sheet
- "products" → use Product Name column (check actual name in sheet)
- "party" or "customer" → use Party Names or similar column (check actual name in sheet)
- "revenue" or "sales" → Sales Invoices sheet (calculate Quantity × Rate or use Amount column)
- "total revenue by product" → Sales Invoices sheet with aggregation by Product Name

QUERY TYPES YOU MUST HANDLE:

1. **SIMPLE QUERIES**: Direct filtering and retrieval
   Example: "Show FG stock > 10" → {{"sheets": ["FG Stock"], "filters": {{"FG Stock": "`Current Level` > 10"}}, "operation": "retrieve"}}

2. **AGGREGATION**: COUNT, SUM, AVG, MAX, MIN, TOTAL
   Example: "Total pending payment amount" → {{"sheets": ["Payments"], "operation": "aggregate", "agg_function": "SUM", "agg_column": "Amount", "filters": {{"Payments": "Status == 'Pending'"}}}}

3. **COMPARISON**: Compare values across sheets OR compare subsets within same sheet
   Example: "Show products with stock below 10 AND pending orders" → {{"sheets": ["FG Stock", "Orders Pending"], "operation": "compare", "join_key": "Product Name", "filters": {{"FG Stock": "`Current Level` < 10", "Orders Pending": "`Pending Qty` > 0"}}}}
   Example: "Compare pending orders of Rungta and Singhal" → {{"sheets": ["Orders Pending"], "operation": "retrieve", "filters": {{"Orders Pending": "(`Party Names`.str.contains('Rungta|Singhal', case=False, na=False)) & (`Pending Qty` > 0)"}}}}

4. **FEASIBILITY**: Check if something is possible
   Example: "Can we fulfill orders with current stock?" → {{"sheets": ["FG Stock", "Orders Pending"], "operation": "feasibility", "join_key": "Product Name", "check": "Current Level >= Pending Qty"}}

5. **RANKING**: TOP N, BOTTOM N, ORDER BY
   Example: "Top 5 products by pending orders" → {{"sheets": ["Orders Pending"], "operation": "rank", "rank_by": "Pending Qty", "rank_order": "desc", "limit": 5}}
   Example: "Which party has maximum pending orders?" → {{"sheets": ["Orders Pending"], "operation": "rank", "rank_by": "COUNT", "group_by": "Party Names", "rank_order": "desc", "limit": 10}}
   Example: "Top customers by order count" → {{"sheets": ["Orders Pending"], "operation": "rank", "rank_by": "COUNT", "group_by": "Party Names", "rank_order": "desc", "limit": 5}}

6. **TREND ANALYSIS**: Changes over time
   Example: "Orders trend last 30 days" → {{"sheets": ["Orders Pending"], "operation": "trend", "date_column": "Party PO Date", "date_range": "last 30 days", "group_by": "week"}}

7. **PREDICTION**: Future projections
   Example: "When will stock run out?" → {{"sheets": ["FG Stock", "Orders Pending", "Production Orders"], "operation": "predict", "predict_type": "stock_depletion", "based_on": ["Pending Qty", "Current Level"]}}

CRITICAL RULES FOR FILTERS:
1. ALWAYS check the sheet info above for EXACT column names
2. Use backticks around column names with spaces: `Party Names`, `Pending Qty`
3. **IMPORTANT - Partial Matching**: When filtering by names (party, product, customer, etc.), use CONTAINS instead of exact match:
   - ❌ WRONG: `Party Names` == 'Rungta mines'
   - ✅ CORRECT: `Party Names`.str.contains('Rungta', case=False, na=False)
   - For multiple values use | (OR): `Party Names`.str.contains('Rungta|Singhaal', case=False, na=False)
4. Use exact match (==) ONLY for:
   - Status fields: Status == 'Completed', Status == 'Pending'
   - Boolean fields: Is This Order Through Some Agent == 'Yes'
   - Numeric comparisons: `Pending Qty` > 0
5. For dates: use 'YYYY-MM-DD' format
6. For multi-sheet queries: specify join_key using EXACT column name
7. ALWAYS return valid JSON, no extra text

Return ONLY JSON with these keys:
- sheets: List of sheet names (EXACT NAMES from above)
- operation: Type (retrieve/aggregate/compare/feasibility/rank/trend/predict)
- filters: Dict of sheet-specific conditions (optional) - USE .str.contains() for names!
- join_key: Column to join on (for multi-sheet)
- agg_function: SUM/COUNT/AVG/MAX/MIN (for aggregate)
- agg_column: Column to aggregate (for aggregate)
- Additional keys based on operation type"""),
            ("user", "{question}")
        ])
        
        # Node functions
        def plan_node(state: EnhancedAgentState) -> dict:
            """Create execution plan using LLM"""
            print("\n🎯 Node: PLAN")
            try:
                question = resolve_date_expressions(state["question"])
                
                # Use selected sheets info if available (token optimization)
                sheets_info_to_use = state.get("selected_sheets_info", self.sheet_info)
                
                response = self.llm.invoke(planner_prompt.format_messages(
                    question=question,
                    sheets_info=sheets_info_to_use
                ))
                
                # Extract JSON from response
                plan_text = response.content
                print(f"  LLM Response: {plan_text[:200]}...")  # Debug: show first 200 chars
                
                plan_text = re.sub(r'```json\s*', '', plan_text)
                plan_text = re.sub(r'```\s*', '', plan_text)
                match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', plan_text, re.DOTALL)
                
                if match:
                    plan = json.loads(match.group(0))
                    if "operation" not in plan:
                        plan["operation"] = "retrieve"
                    if "sheets" not in plan or not plan["sheets"]:
                        print(f"  ⚠️ No sheets specified, defaulting to Orders Pending")
                        plan["sheets"] = ["Orders Pending"]
                    
                    print(f"  Operation: {plan.get('operation')}")
                    print(f"  Sheets: {plan.get('sheets')}")
                    return {"plan": plan, "error": None}
                else:
                    print(f"  ❌ Failed to extract JSON from response")
                    return {"error": "Failed to parse plan JSON"}
                    
            except Exception as e:
                print(f"  ❌ Exception: {str(e)}")
                return {"error": f"Planning failed: {str(e)}"}
        
        def execute_node(state: EnhancedAgentState) -> dict:
            """Execute the plan with enhanced operations"""
            print("\n🎯 Node: EXECUTE")
            try:
                plan = state.get("plan")
                
                # Check if plan exists and has required fields
                if not plan:
                    return {"error": "No execution plan available"}
                
                if not plan.get("sheets"):
                    return {"error": "No sheets specified in plan"}
                
                operation = plan.get("operation", "retrieve")
                
                print(f"\n🔄 Executing {operation.upper()} operation...")
                
                # Load and filter sheets
                dfs = {}
                for sheet_name in plan["sheets"]:
                    if sheet_name in self.dataframes:
                        df = self.dataframes[sheet_name].copy()
                        
                        # Apply filters
                        if plan.get("filters") and sheet_name in plan["filters"]:
                            condition = plan["filters"][sheet_name]
                            if condition:
                                print(f"  🔍 Filtering {sheet_name}: {condition}")
                                df = safe_query(df, condition)
                        
                        if df.empty:
                            print(f"  ⚠️  {sheet_name} is empty after filtering")
                        
                        dfs[sheet_name] = df
                
                # Execute based on operation type
                if operation == "aggregate":
                    result = self._execute_aggregate(dfs, plan)
                elif operation == "compare":
                    result = self._execute_compare(dfs, plan)
                elif operation == "feasibility":
                    result = self._execute_feasibility(dfs, plan)
                elif operation == "rank":
                    result = self._execute_rank(dfs, plan)
                elif operation == "trend":
                    result = self._execute_trend(dfs, plan)
                elif operation == "predict":
                    result = self._execute_predict(dfs, plan)
                else:  # retrieve
                    result = self._execute_retrieve(dfs, plan)
                
                print(f"  ✓ Returned {len(result)} rows × {len(result.columns)} columns")
                return {"result": result, "error": None}
                
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Execution failed: {error_msg[:200]}")
                return {"error": f"Execution failed: {error_msg}"}
        
        def answer_node(state: EnhancedAgentState) -> dict:
            """Enhanced answer generation with operation-specific extraction"""
            print("\n🎯 Node: ANSWER")
            try:
                result = state["result"]
                question = state["question"]
                plan = state["plan"]
                operation = plan.get('operation', 'retrieve')
                
                if result.empty:
                    return {
                        "answer": "No data found matching your query criteria.",
                        "confidence": 0.3,
                        "error": None
                    }
                
                # Build operation-specific context for LLM
                if operation == 'aggregate':
                    context = f"Aggregation Result ({plan.get('agg_function', 'COUNT')}): {len(result)} rows\n"
                elif operation == 'compare':
                    context = f"Comparison across {len(plan['sheets'])} sheets: {len(result)} rows\n"
                elif operation == 'feasibility':
                    context = "Feasibility Analysis:\n"
                elif operation == 'trend':
                    context = f"Trend Analysis (by {plan.get('group_by', 'period')}): {len(result)} rows\n"
                elif operation == 'rank':
                    context = f"Ranking Results: {len(result)} items\n"
                else:
                    context = f"Query Results ({len(result)} rows):\n"
                
                # Add data summary (show more context for better LLM responses)
                if len(result) <= 10:
                    context += result.to_string()
                else:
                    context += result.head(10).to_string()
                    numeric_cols = result.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) > 0:
                        context += f"\n\nSummary Stats:\n{result[numeric_cols].describe().to_string()}"
                
                # Generate natural language answer using LLM
                answer_prompt = f"""You are a helpful data assistant. Analyze the data and provide a well-formatted, structured response.

User Question: {question}
Operation Type: {operation.upper()}

Data Results:
{context}

Instructions:
1. Format your response using markdown with clear structure
2. **NEVER use markdown pipe tables (| --- | --- |)** - the data table is shown separately
3. **Vary your format based on the query type:**
   - For "how many/total/count" → Start with the direct answer number in **bold**
   - For "compare" queries → Use bullet points for side-by-side comparison
   - For "top/highest/lowest" → Use numbered ranking list
   - For "list/show" queries → Use brief intro + bullet highlights
   - For "trend/analysis" → Use descriptive paragraphs with insights
4. Use **bold** for important numbers and metrics
5. Use bullet points (•) for key findings - but NOT for every response
6. Use ### for section headers when needed
7. Keep paragraphs short (2-3 lines max)
8. Be conversational and natural - avoid robotic patterns
9. Don't always use "Summary" or "Key Insights" - vary your section titles

Example formats to vary:

**For counts:** "There are **33 pending orders** across all customers..."

**For comparisons:**
### Rungta vs Shinghal
• Rungta: **2 orders**, Total: ₹77.5
• Shinghal: **7 orders**, Total: ₹550.2

**For rankings:**
### Top 3 Pending Orders
1. Liquid Binder - **800 units**
2. Ceramic Paper - **580 units**
3. Ceramic Anchor - **568 units**

Answer:"""

                response = self.llm.invoke(answer_prompt)
                answer = response.content.strip()
                
                # Fallback if LLM returns empty answer
                if not answer:
                    if operation == 'retrieve':
                        answer = f"Found {len(result)} matching records based on your query."
                    elif operation == 'aggregate':
                        answer = f"Aggregation complete with {len(result)} results."
                    else:
                        answer = f"Query completed successfully with {len(result)} results."
                
                # Calculate confidence
                confidence = 0.5
                if len(result) > 0:
                    confidence += 0.3
                if len(result.columns) >= 3:
                    confidence += 0.1
                confidence = min(confidence, 1.0)
                
                return {
                    "answer": answer,
                    "confidence": confidence,
                    "error": None
                }
                
            except Exception as e:
                return {"error": f"Answer generation failed: {str(e)}"}
        
        # Build graph
        graph = StateGraph(EnhancedAgentState)
        graph.add_node("planner", plan_node)
        graph.add_node("executor", execute_node)
        graph.add_node("answerer", answer_node)
        
        graph.add_edge(START, "planner")
        graph.add_edge("planner", "executor")
        graph.add_edge("executor", "answerer")
        graph.add_edge("answerer", END)
        
        self.agent = graph.compile()
    
    # ========================================================================
    # EXECUTION METHODS FOR 7 OPERATION TYPES
    # ========================================================================
    
    def _execute_retrieve(self, dfs: dict, plan: dict) -> pd.DataFrame:
        """Basic retrieval with optional join"""
        if not dfs:
            return pd.DataFrame()
        
        if plan.get("join_key") and len(dfs) > 1:
            sheets = list(dfs.keys())
            result = dfs[sheets[0]]
            for sheet_name in sheets[1:]:
                result = result.merge(dfs[sheet_name], on=plan["join_key"], how="inner", suffixes=('', f'_{sheet_name}'))
            return result
        else:
            return dfs[list(dfs.keys())[0]]
    
    def _execute_aggregate(self, dfs: dict, plan: dict) -> pd.DataFrame:
        """Aggregate with Qty×Rate support"""
        df = dfs[list(dfs.keys())[0]].copy()
        agg_func = plan.get("agg_function", "COUNT").upper()
        agg_col = plan.get("agg_column")
        
        if df.empty:
            return pd.DataFrame({"Result": [0]})
        
        # Filter positive quantities
        if 'Pending Qty' in df.columns:
            df['Pending Qty'] = pd.to_numeric(df['Pending Qty'], errors='coerce')
            df = df[df['Pending Qty'] > 0]
        
        # Handle VALUE calculation (Qty × Rate)
        if agg_col and '*' in agg_col:
            parts = [p.strip() for p in agg_col.split('*')]
            if len(parts) == 2:
                col1, col2 = parts
                actual_col1 = next((c for c in df.columns if col1.lower() in c.lower()), None)
                actual_col2 = next((c for c in df.columns if col2.lower() in c.lower()), None)
                
                if actual_col1 and actual_col2:
                    df['_calculated_value'] = (
                        pd.to_numeric(df[actual_col1], errors='coerce') * 
                        pd.to_numeric(df[actual_col2], errors='coerce')
                    )
                    agg_col = '_calculated_value'
                    print(f"  💡 Calculated: {actual_col1} × {actual_col2}")
        
        # Perform aggregation
        if agg_func == "COUNT":
            result = pd.DataFrame({"Count": [len(df)]})
        elif agg_func in ["SUM", "AVG", "MAX", "MIN", "MEAN"]:
            if not agg_col or agg_col not in df.columns:
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                agg_col = numeric_cols[0] if len(numeric_cols) > 0 else None
            
            if agg_col:
                if agg_func == "SUM":
                    value = df[agg_col].sum()
                elif agg_func in ["AVG", "MEAN"]:
                    value = df[agg_col].mean()
                elif agg_func == "MAX":
                    value = df[agg_col].max()
                elif agg_func == "MIN":
                    value = df[agg_col].min()
                
                result = pd.DataFrame({f"{agg_func}_{agg_col}": [value]})
            else:
                result = pd.DataFrame({"Error": ["No numeric column found"]})
        else:
            result = df
        
        print(f"  ✓ Aggregation complete: {agg_func}")
        return result
    
    def _execute_compare(self, dfs: dict, plan: dict) -> pd.DataFrame:
        """Compare with product grouping - Fixed to remove zeros AFTER grouping"""
        if len(dfs) < 2:
            return list(dfs.values())[0]
        
        join_key = plan.get("join_key", "Product Name")
        sheets = list(dfs.keys())
        
        # Group Orders Pending by Product
        processed_dfs = {}
        for sheet_name in sheets:
            df = dfs[sheet_name].copy()
            
            if 'Orders Pending' in sheet_name and 'Product Name' in df.columns:
                df['Pending Qty'] = pd.to_numeric(df['Pending Qty'], errors='coerce')
                df = df[df['Pending Qty'] > 0]  # Filter before grouping
                df_grouped = df.groupby('Product Name').agg({
                    'Pending Qty': 'sum',
                    'Quantity': 'sum' if 'Quantity' in df.columns else 'sum'
                }).reset_index()
                # 🔧 FIX: Remove products with zero pending AFTER grouping
                df_grouped = df_grouped[df_grouped['Pending Qty'] > 0]
                processed_dfs[sheet_name] = df_grouped
            else:
                processed_dfs[sheet_name] = df
        
        # Merge sheets
        result = processed_dfs[sheets[0]]
        for sheet_name in sheets[1:]:
            if sheet_name in processed_dfs:
                result = result.merge(processed_dfs[sheet_name], on=join_key, how="inner", suffixes=('_stock', '_pending'))
        
        print(f"  ✓ Comparison complete (grouped by product)")
        return result
    
    def _execute_feasibility(self, dfs: dict, plan: dict) -> pd.DataFrame:
        """Feasibility check"""
        result = self._execute_compare(dfs, plan)
        
        stock_col = next((c for c in result.columns if 'Current Level' in c or 'stock' in c.lower()), None)
        demand_col = next((c for c in result.columns if 'Pending' in c), None)
        
        if stock_col and demand_col:
            result['Can_Fulfill'] = pd.to_numeric(result[stock_col], errors='coerce') >= pd.to_numeric(result[demand_col], errors='coerce')
            result['Gap'] = pd.to_numeric(result[stock_col], errors='coerce') - pd.to_numeric(result[demand_col], errors='coerce')
        
        print(f"  ✓ Feasibility check complete")
        return result
    
    def _execute_rank(self, dfs: dict, plan: dict) -> pd.DataFrame:
        """Rank with smart grouping - supports Product Name, Party Names, etc."""
        df = dfs[list(dfs.keys())[0]].copy()
        
        rank_by = plan.get("rank_by")
        rank_order = plan.get("rank_order", "desc")
        limit = plan.get("limit", 10)
        group_by = plan.get("group_by")  # New: explicit group_by field
        
        # Filter positive quantities
        if 'Pending Qty' in df.columns:
            df['Pending Qty'] = pd.to_numeric(df['Pending Qty'], errors='coerce')
            df = df[df['Pending Qty'] > 0]
        
        ascending = (rank_order.lower() == "asc")
        
        # Handle COUNT-based ranking (e.g., "party with most orders")
        if rank_by and rank_by.upper() == "COUNT":
            # Determine what to group by
            if group_by and group_by in df.columns:
                group_col = group_by
            elif 'Party Names' in df.columns:
                group_col = 'Party Names'
            elif 'Product Name' in df.columns:
                group_col = 'Product Name'
            else:
                group_col = df.columns[0]
            
            df_grouped = df.groupby(group_col).size().reset_index(name='Order Count')
            result = df_grouped.sort_values(by='Order Count', ascending=ascending).head(limit)
            print(f"  ✓ Counted orders by {group_col}, top {limit}")
            return result
        
        # Handle explicit group_by
        if group_by and group_by in df.columns and rank_by and rank_by in df.columns:
            df_grouped = df.groupby(group_by)[rank_by].sum().reset_index()
            result = df_grouped.sort_values(by=rank_by, ascending=ascending).head(limit)
            print(f"  ✓ Grouped by {group_by}, ranked by {rank_by}, top {limit}")
            return result
        
        # Group by Product if ranking by pending
        if rank_by and 'Pending' in rank_by and 'Product Name' in df.columns:
            df_grouped = df.groupby('Product Name')[rank_by].sum().reset_index()
            result = df_grouped.sort_values(by=rank_by, ascending=ascending).head(limit)
            print(f"  ✓ Grouped by Product, ranked by {rank_by}, top {limit}")
        elif rank_by and rank_by in df.columns:
            result = df.sort_values(by=rank_by, ascending=ascending).head(limit)
            print(f"  ✓ Ranked by {rank_by}, top {limit}")
        else:
            result = df.head(limit)
            print(f"  ⚠️  Rank column not found")
        
        return result
    
    def _execute_trend(self, dfs: dict, plan: dict) -> pd.DataFrame:
        """Trend analysis over time"""
        df = dfs[list(dfs.keys())[0]].copy()
        
        date_col = plan.get("date_column", "Timestamp")
        group_by = plan.get("group_by", "week")
        
        # Find date column
        date_columns = [c for c in df.columns if 'date' in c.lower() or 'timestamp' in c.lower()]
        if date_columns:
            date_col = date_columns[0]
        
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            df = df.dropna(subset=[date_col])
            
            if group_by == "day":
                df['Period'] = df[date_col].dt.date
            elif group_by == "week":
                df['Period'] = df[date_col].dt.to_period('W').astype(str)
            elif group_by == "month":
                df['Period'] = df[date_col].dt.to_period('M').astype(str)
            else:
                df['Period'] = df[date_col].dt.date
            
            result = df.groupby('Period').size().reset_index(name='Count')
            print(f"  ✓ Trend analysis by {group_by} ({len(df)} rows analyzed)")
        else:
            result = pd.DataFrame({"Error": ["No date column found"]})
        
        return result
    
    def _execute_predict(self, dfs: dict, plan: dict) -> pd.DataFrame:
        """Simple prediction/projection"""
        predict_type = plan.get("predict_type", "stock_depletion")
        
        if predict_type == "stock_depletion" and len(dfs) >= 2:
            result = self._execute_compare(dfs, plan)
            
            stock_col = next((c for c in result.columns if 'Current Level' in c or 'stock' in c.lower()), None)
            demand_col = next((c for c in result.columns if 'Pending' in c), None)
            
            if stock_col and demand_col:
                result['Days_Until_Depletion'] = np.where(
                    pd.to_numeric(result[demand_col], errors='coerce') > 0,
                    (pd.to_numeric(result[stock_col], errors='coerce') / pd.to_numeric(result[demand_col], errors='coerce')) * 30,
                    999
                )
                print(f"  ✓ Prediction: Stock depletion forecast")
                return result
        
        df = dfs[list(dfs.keys())[0]]
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            result = df[numeric_cols].describe()
        else:
            result = df.head(10)
        
        return result
    
    # ========================================================================
    # PUBLIC API
    # ========================================================================
    
    def refresh_data(self):
        """Refresh Google Sheets data (called by background task)"""
        try:
            self._load_sheets_data()
            self.last_refresh = datetime.utcnow()
            
            # Clear cache on data refresh (per user requirement)
            self._clear_query_cache()
            
            print(f"♻️ Data refreshed at {self.last_refresh}")
        except Exception as e:
            print(f"❌ Error refreshing data: {e}")
    
    def _clear_query_cache(self):
        """Clear the query cache (called on data refresh or restart)."""
        from database import SessionLocal, QueryCache
        db = SessionLocal()
        try:
            deleted_count = db.query(QueryCache).delete()
            db.commit()
            print(f"🗑️ Cleared {deleted_count} cached queries")
        except Exception as e:
            print(f"⚠️ Error clearing cache: {e}")
            db.rollback()
        finally:
            db.close()
    
    def clear_session_cache(self, session_id: str):
        """Clear cache for a specific session (called when session is deleted)."""
        from database import SessionLocal, QueryCache
        db = SessionLocal()
        try:
            deleted_count = db.query(QueryCache).filter(QueryCache.session_id == session_id).delete()
            db.commit()
            print(f"🗑️ Cleared {deleted_count} cached queries for session: {session_id}")
            return {"deleted": deleted_count}
        except Exception as e:
            print(f"⚠️ Error clearing session cache: {e}")
            db.rollback()
            return {"error": str(e)}
        finally:
            db.close()
    
    def _check_cache(self, question: str, session_id: str = None, threshold: float = 0.98) -> Optional[Dict[str, Any]]:
        """
        Check if similar query exists in cache (98% similarity threshold - very strict).
        Only checks cache within the same session to avoid cross-session confusion.
        Returns cached response if found, None otherwise.
        """
        from database import SessionLocal, QueryCache
        db = SessionLocal()
        try:
            # Only check cache for queries in the same session
            if session_id:
                cached_queries = db.query(QueryCache).filter(QueryCache.session_id == session_id).all()
            else:
                cached_queries = db.query(QueryCache).all()
            
            if not cached_queries:
                return None
            
            # Calculate similarity with each cached query
            model = get_embedding_model()
            question_embedding = model.encode(question)
            
            best_match = None
            best_similarity = 0.0
            
            for cached in cached_queries:
                # Skip if it's the exact same question (would be 100% match)
                if cached.query_text.strip().lower() == question.strip().lower():
                    continue
                    
                cached_embedding = model.encode(cached.query_text)
                similarity = cosine_similarity(
                    question_embedding.reshape(1, -1),
                    cached_embedding.reshape(1, -1)
                )[0][0]
                
                # Debug: Log similarity check
                print(f"  📊 Comparing with cached: '{cached.query_text[:50]}...' -> Similarity: {similarity:.2%}")
                
                if similarity > best_similarity and similarity >= threshold:
                    best_similarity = similarity
                    best_match = cached
            
            if best_match:
                # Update hit count
                best_match.hit_count += 1
                db.commit()
                
                print(f"💾 Cache HIT! Similarity: {best_similarity:.2%}, Hits: {best_match.hit_count}")
                
                # Parse response from cache
                response_data = json.loads(best_match.response)
                
                # Check if current query intent wants table
                show_table = detect_table_intent(question)
                cached_data_preview = response_data.get("data_preview")
                
                # If user wants table but cache doesn't have it, or vice versa, respect current intent
                if not show_table:
                    cached_data_preview = None  # Don't show table if user wants summary
                
                return {
                    "answer": response_data.get("answer"),
                    "confidence": best_match.confidence,
                    "rows_found": best_match.rows_found,
                    "data_preview": cached_data_preview,
                    "query_type": response_data.get("query_type", "CACHED"),
                    "cached": True,
                    "cache_similarity": best_similarity,
                    "show_table": show_table
                }
            
            return None
            
        except Exception as e:
            print(f"⚠️ Cache check error: {e}")
            return None
        finally:
            db.close()
    
    def _save_to_cache(self, question: str, response: Dict[str, Any], session_id: str = None):
        """Save query response to cache with session tracking."""
        from database import SessionLocal, QueryCache
        db = SessionLocal()
        try:
            cache_entry = QueryCache(
                session_id=session_id,
                query_text=question,
                response=json.dumps({
                    "answer": response.get("answer"),
                    "data_preview": response.get("data_preview"),
                    "query_type": response.get("query_type")
                }),
                confidence=response.get("confidence"),
                rows_found=response.get("rows_found")
            )
            db.add(cache_entry)
            db.commit()
            print(f"💾 Saved to cache (session: {session_id}): {question[:50]}...")
        except Exception as e:
            print(f"⚠️ Cache save error: {e}")
            db.rollback()
        finally:
            db.close()
    
    def _extract_current_question(self, question: str) -> str:
        """Extract just the current question from a question that may include conversation context."""
        if "Current question:" in question:
            # Extract only the current question for caching
            return question.split("Current question:")[-1].strip()
        return question.strip()
    
    def query(self, question: str, session_id: str = None) -> Dict[str, Any]:
        """
        Process a user question and return results.
        OPTIMIZED: Checks cache first (98% similarity - very strict), uses embeddings to select top 3 sheets.
        
        Returns:
            dict with keys: answer, confidence, rows_found, data_preview, query_type
        """
        try:
            # Extract ONLY the current question for caching (ignore conversation context)
            cache_question = self._extract_current_question(question)
            
            # OPTIMIZATION 1: Check cache first (session-specific, 98% threshold)
            # Use only the current question for cache lookup, not full context
            cached_response = self._check_cache(cache_question, session_id=session_id, threshold=0.98)
            if cached_response:
                return cached_response
            
            # OPTIMIZATION 2: Select top 3 relevant sheets using embeddings
            relevant_sheets = self._select_relevant_sheets(question, top_n=3)
            selected_sheet_info = self._get_selected_sheet_info(relevant_sheets)
            
            # Update state with selected sheets info
            print(f"📊 Using {len(relevant_sheets)} sheets (reduced from {len(self.dataframes)})")
            
            # Run agent with optimized sheet info
            result = self.agent.invoke({
                "question": question,
                "plan": None,
                "result": None,
                "answer": "",
                "confidence": 0.0,
                "error": None,
                "retry_count": 0,
                "selected_sheets_info": selected_sheet_info  # Use selected instead of all
            })
            
            # Extract data preview if result is DataFrame
            data_preview = None
            rows_found = None
            show_table = detect_table_intent(question)  # Detect user intent
            
            if isinstance(result.get("result"), pd.DataFrame):
                df = result["result"]
                rows_found = len(df)
                # Only include data_preview if user wants to see the table
                if rows_found > 0 and show_table:
                    data_preview = df.head(10).to_dict('records')
                    print(f"📋 Including table in response ({rows_found} rows)")
                elif rows_found > 0 and not show_table:
                    print(f"💬 Natural language only (no table), analyzed {rows_found} rows")
            
            response = {
                "answer": result.get("answer", "No answer generated"),
                "confidence": result.get("confidence", 0.5),
                "rows_found": rows_found,
                "data_preview": data_preview,
                "query_type": result.get("plan", {}).get("operation", "UNKNOWN").upper() if result.get("plan") else "UNKNOWN",
                "error": result.get("error"),
                "cached": False,
                "show_table": show_table
            }
            
            # OPTIMIZATION 3: Save to cache using ONLY the current question (not full context)
            self._save_to_cache(cache_question, response, session_id)
            
            return response
            
        except Exception as e:
            return {
                "answer": f"I encountered an error processing your question: {str(e)}",
                "confidence": 0.0,
                "rows_found": None,
                "data_preview": None,
                "query_type": "ERROR",
                "error": str(e),
                "cached": False
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about loaded data"""
        return {
            "sheets_loaded": len(self.dataframes) > 0,
            "total_sheets": len(self.dataframes),
            "total_rows": sum(len(df) for df in self.dataframes.values()),
            "last_refresh": self.last_refresh
        }


# Global agent instance (initialized once)
agent_instance: Optional[GoogleSheetsAgent] = None


def get_agent() -> GoogleSheetsAgent:
    """Get or create the global agent instance"""
    global agent_instance
    if agent_instance is None:
        agent_instance = GoogleSheetsAgent()
    return agent_instance
