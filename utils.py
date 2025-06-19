import pandas as pd
import numpy as np
import re
from typing import Union, List

# =============================================================================
# SCORING CONFIGURATION CONSTANTS
# =============================================================================

# Industry scoring weights
WEIGHT_INDUSTRY_MATCH = 30          # Perfect industry match (target sectors)
WEIGHT_INDUSTRY_OTHER = 5           # Other defined industries

# Company size scoring weights (based on employee count)
WEIGHT_SIZE_ENTERPRISE = 25         # >200 employees
WEIGHT_SIZE_MID_MARKET = 15         # 50-200 employees  
WEIGHT_SIZE_SMALL_BUSINESS = 5      # <50 employees

# Revenue scoring weights
WEIGHT_REVENUE_HIGH = 25            # >$20M revenue
WEIGHT_REVENUE_MID = 15             # $5M-$20M revenue

# Contact quality scoring weights
WEIGHT_DECISION_MAKER = 20          # C-level, Founder titles
WEIGHT_INFLUENCER = 10              # Director, Head titles

# Data completeness scoring weights
WEIGHT_EMAIL_AVAILABLE = 10         # Has contact email
WEIGHT_LINKEDIN_AVAILABLE = 10      # Has LinkedIn profile

# Target industries for lead qualification
TARGET_INDUSTRIES = [
    'saas', 'fintech', 'healthtech', 'cloud computing', 
    'cybersecurity', 'artificial intelligence', 'data analytics'
]

# Decision maker keywords (case-insensitive matching)
DECISION_MAKER_KEYWORDS = ['ceo', 'founder', 'cto', 'ciso', 'chief', 'president']
INFLUENCER_KEYWORDS = ['owner', 'head', 'director', 'vp', 'vice president']

# Revenue thresholds
REVENUE_HIGH_THRESHOLD = 20_000_000  # $20M
REVENUE_MID_THRESHOLD = 5_000_000    # $5M

# Employee count thresholds
EMPLOYEES_ENTERPRISE_THRESHOLD = 200
EMPLOYEES_MID_MARKET_THRESHOLD = 50


# =============================================================================
# DATA NORMALIZATION FUNCTIONS
# =============================================================================

def normalize_industry(industry: Union[str, float]) -> str:
    """
    Normalize industry field for consistent matching.
    
    Args:
        industry: Raw industry string or NaN
        
    Returns:
        Normalized industry string (lowercase, stripped) or empty string
    """
    if pd.isna(industry):
        return ""
    
    return str(industry).lower().strip()


def normalize_revenue(revenue: Union[str, int, float]) -> float:
    """
    Convert revenue string formats to float values.
    Handles formats like: "$4.7B", "2.3M", "500K", "1000000"
    
    Args:
        revenue: Raw revenue value in various formats
        
    Returns:
        Revenue as float, or 0.0 if invalid/missing
    """
    if pd.isna(revenue):
        return 0.0
    
    try:
        # Convert to string and clean
        revenue_str = str(revenue).upper().replace('$', '').replace(',', '').strip()
        
        # Handle billion notation
        if 'B' in revenue_str:
            return float(revenue_str.replace('B', '')) * 1_000_000_000
        
        # Handle million notation  
        elif 'M' in revenue_str:
            return float(revenue_str.replace('M', '')) * 1_000_000
            
        # Handle thousand notation
        elif 'K' in revenue_str:
            return float(revenue_str.replace('K', '')) * 1_000
            
        # Handle plain numbers
        else:
            return float(revenue_str)
            
    except (ValueError, TypeError):
        return 0.0


def normalize_employee_count(employees: Union[str, int, float]) -> int:
    """
    Normalize employee count field to integer.
    
    Args:
        employees: Raw employee count value
        
    Returns:
        Employee count as integer, or 0 if invalid/missing
    """
    if pd.isna(employees):
        return 0
        
    try:
        # Handle string formats like "50-100", "100+"
        employees_str = str(employees).replace('+', '').replace(',', '')
        
        # Extract first number from ranges
        if '-' in employees_str:
            employees_str = employees_str.split('-')[0]
            
        return int(float(employees_str))
        
    except (ValueError, TypeError):
        return 0


# =============================================================================
# CORE SCORING FUNCTIONS
# =============================================================================

def calculate_industry_score(industry: str) -> int:
    """
    Calculate score based on industry fit.
    
    Args:
        industry: Normalized industry string
        
    Returns:
        Industry fit score
    """
    if not industry:
        return 0
        
    if industry in TARGET_INDUSTRIES:
        return WEIGHT_INDUSTRY_MATCH
    else:
        return WEIGHT_INDUSTRY_OTHER


def calculate_size_score(employee_count: int) -> int:
    """
    Calculate score based on company size (employee count).
    
    Args:
        employee_count: Number of employees
        
    Returns:
        Company size score
    """
    if employee_count > EMPLOYEES_ENTERPRISE_THRESHOLD:
        return WEIGHT_SIZE_ENTERPRISE
    elif employee_count >= EMPLOYEES_MID_MARKET_THRESHOLD:
        return WEIGHT_SIZE_MID_MARKET
    elif employee_count > 0:
        return WEIGHT_SIZE_SMALL_BUSINESS
    else:
        return 0


def calculate_revenue_score(revenue: float) -> int:
    """
    Calculate score based on company revenue.
    
    Args:
        revenue: Annual revenue in dollars
        
    Returns:
        Revenue-based score
    """
    if revenue > REVENUE_HIGH_THRESHOLD:
        return WEIGHT_REVENUE_HIGH
    elif revenue >= REVENUE_MID_THRESHOLD:
        return WEIGHT_REVENUE_MID
    else:
        return 0


def calculate_title_score(title: Union[str, float]) -> int:
    """
    Calculate score based on contact's job title/seniority.
    
    Args:
        title: Job title string
        
    Returns:
        Title-based score
    """
    if pd.isna(title):
        return 0
        
    title_lower = str(title).lower()
    
    # Check for decision maker keywords
    if any(keyword in title_lower for keyword in DECISION_MAKER_KEYWORDS):
        return WEIGHT_DECISION_MAKER
    
    # Check for influencer keywords  
    elif any(keyword in title_lower for keyword in INFLUENCER_KEYWORDS):
        return WEIGHT_INFLUENCER
    
    return 0


def calculate_completeness_score(email: Union[str, float], linkedin: Union[str, float]) -> int:
    """
    Calculate score based on data completeness.
    
    Args:
        email: Contact email address
        linkedin: LinkedIn profile URL
        
    Returns:
        Data completeness score
    """
    score = 0
    
    if pd.notna(email) and str(email).strip():
        score += WEIGHT_EMAIL_AVAILABLE
        
    if pd.notna(linkedin) and str(linkedin).strip():
        score += WEIGHT_LINKEDIN_AVAILABLE
        
    return score


def calculate_lead_score(row: pd.Series) -> int:
    """
    Calculate comprehensive lead score for a single lead.
    
    This function combines multiple scoring factors to produce a single
    lead quality score. Higher scores indicate higher-quality leads.
    
    Note: This rule-based approach can be extended with ML model predictions
    by replacing individual scoring functions with model outputs.
    
    Args:
        row: DataFrame row containing lead data
        
    Returns:
        Total lead score (0-100+ range)
    """
    try:
        # Normalize input fields
        industry = normalize_industry(row.get('Industry'))
        revenue = normalize_revenue(row.get('Revenue'))
        employee_count = normalize_employee_count(row.get('Employees Count'))
        
        # Calculate component scores
        industry_score = calculate_industry_score(industry)
        size_score = calculate_size_score(employee_count)
        revenue_score = calculate_revenue_score(revenue)
        title_score = calculate_title_score(row.get('Owner Title'))
        completeness_score = calculate_completeness_score(
            row.get('Owner Email'), 
            row.get('Owner LinkedIn')
        )
        
        # Future ML integration point:
        # ml_score = predict_lead_quality(row) if MODEL_ENABLED else 0
        
        total_score = (
            industry_score + 
            size_score + 
            revenue_score + 
            title_score + 
            completeness_score
        )
        
        return int(total_score)
        
    except Exception as e:
        # Log error in production system
        print(f"Warning: Error calculating score for lead: {e}")
        return 0


# =============================================================================
# DATA QUALITY FLAGS
# =============================================================================

def generate_quality_flags(row: pd.Series) -> str:
    """
    Generate data quality flags for lead record.
    
    Identifies missing or problematic data fields that could impact
    lead qualification or outreach effectiveness.
    
    Args:
        row: DataFrame row containing lead data
        
    Returns:
        Comma-separated string of quality flags, or empty string
    """
    flags = []
    
    # Critical contact information
    if pd.isna(row.get('Owner Email')) or not str(row.get('Owner Email', '')).strip():
        flags.append('Missing Email')
        
    if pd.isna(row.get('Owner Name')) or not str(row.get('Owner Name', '')).strip():
        flags.append('Missing Contact Name')
    
    # Company qualification data
    if pd.isna(row.get('Industry')) or not str(row.get('Industry', '')).strip():
        flags.append('Missing Industry')
        
    # Size/revenue indicators (need at least one)
    has_employee_data = pd.notna(row.get('Employees Count')) and row.get('Employees Count', 0) > 0
    has_revenue_data = pd.notna(row.get('Revenue')) and normalize_revenue(row.get('Revenue')) > 0
    
    if not has_employee_data and not has_revenue_data:
        flags.append('Missing Size/Revenue Data')
    
    # LinkedIn for social selling
    if pd.isna(row.get('Company LinkedIn')) or not str(row.get('Company LinkedIn', '')).strip():
        flags.append('Missing Company LinkedIn')
        
    # Job title for personalization
    if pd.isna(row.get('Owner Title')) or not str(row.get('Owner Title', '')).strip():
        flags.append('Missing Job Title')
    
    return ', '.join(flags)


# =============================================================================
# MAIN PROCESSING FUNCTION
# =============================================================================

def process_leads(df: pd.DataFrame) -> pd.DataFrame:
    """
    Main function to process and score lead data.
    
    Applies lead scoring algorithm and quality flagging to the entire
    dataset, then sorts by score for prioritization.
    
    Args:
        df: Raw DataFrame from CSV file
        
    Returns:
        Processed DataFrame with Score and Flags columns, sorted by priority
    """
    if df.empty:
        return df
    
    # Create working copy to avoid modification warnings
    processed_df = df.copy()
    
    # Apply scoring and flagging
    processed_df['Score'] = processed_df.apply(calculate_lead_score, axis=1)
    processed_df['Flags'] = processed_df.apply(generate_quality_flags, axis=1)
    
    # Sort by score (highest first) for priority ranking
    processed_df = processed_df.sort_values(
        by='Score', 
        ascending=False
    ).reset_index(drop=True)
    
    # Reorder columns for better readability
    priority_columns = [
        'Score', 'Flags', 'Company', 'Industry', 
        'Employees Count', 'Revenue', 'Owner Name', 'Owner Title'
    ]
    
    # Get remaining columns
    other_columns = [col for col in processed_df.columns if col not in priority_columns]
    
    # Reorder with priority columns first
    final_column_order = priority_columns + other_columns
    processed_df = processed_df[[col for col in final_column_order if col in processed_df.columns]]
    
    return processed_df


# =============================================================================
# UTILITY FUNCTIONS FOR ANALYSIS
# =============================================================================

def get_scoring_summary() -> dict:
    """
    Return summary of scoring configuration for documentation/debugging.
    
    Returns:
        Dictionary containing scoring weights and thresholds
    """
    return {
        'scoring_weights': {
            'industry_match': WEIGHT_INDUSTRY_MATCH,
            'industry_other': WEIGHT_INDUSTRY_OTHER,
            'size_enterprise': WEIGHT_SIZE_ENTERPRISE,
            'size_mid_market': WEIGHT_SIZE_MID_MARKET,
            'size_small': WEIGHT_SIZE_SMALL_BUSINESS,
            'revenue_high': WEIGHT_REVENUE_HIGH,
            'revenue_mid': WEIGHT_REVENUE_MID,
            'decision_maker': WEIGHT_DECISION_MAKER,
            'influencer': WEIGHT_INFLUENCER,
            'email_complete': WEIGHT_EMAIL_AVAILABLE,
            'linkedin_complete': WEIGHT_LINKEDIN_AVAILABLE
        },
        'thresholds': {
            'revenue_high': REVENUE_HIGH_THRESHOLD,
            'revenue_mid': REVENUE_MID_THRESHOLD,
            'employees_enterprise': EMPLOYEES_ENTERPRISE_THRESHOLD,
            'employees_mid_market': EMPLOYEES_MID_MARKET_THRESHOLD
        },
        'target_industries': TARGET_INDUSTRIES
    }