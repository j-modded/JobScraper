from jobspy import scrape_jobs
import pandas as pd
from datetime import datetime
import sys
import os
import re
from jobs_config import get_job_class
from language_config import get_language_config, DEFAULT_LANGUAGE

# Configuration - Hardcoded
SITES = ["linkedin"]
RESULTS_WANTED = 500
HOURS_OLD = 168  # Last 7 days
DEFAULT_RESULTS_FOLDER = "results"


def prepare_dataframe_for_save(df):
    """
    Prepare dataframe for saving by:
    1. Sorting by date_posted (newest first)
    2. Excluding description and company_logo columns
    3. Reordering columns: site, title, company, location, date_posted, job_url, job_url_direct, then rest
    4. Adding a space after each URL
    """
    if len(df) == 0:
        return df
    
    # Sort by date_posted (newest first)
    if 'date_posted' in df.columns:
        df = df.sort_values('date_posted', ascending=False, na_position='last').reset_index(drop=True)
    
    # Add space after URLs
    if 'job_url' in df.columns:
        df['job_url'] = df['job_url'].fillna('').astype(str) + ' '
    if 'job_url_direct' in df.columns:
        df['job_url_direct'] = df['job_url_direct'].fillna('').astype(str) + ' '
    
    # Columns to exclude
    exclude_cols = ['description', 'company_logo']
    
    # Drop excluded columns
    df = df.drop(columns=exclude_cols, errors='ignore')
    
    # Define the priority column order
    priority_cols = ['site', 'title', 'company', 'location', 'date_posted', 'job_url', 'job_url_direct']
    
    # Get remaining columns (not in priority list)
    remaining_cols = [col for col in df.columns if col not in priority_cols]
    
    # Combine: priority columns first, then remaining
    ordered_cols = priority_cols + remaining_cols
    
    # Reorder dataframe with only columns that exist
    ordered_cols = [col for col in ordered_cols if col in df.columns]
    df = df[ordered_cols]
    
    return df


def log_time(message):
    """Log message with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def ensure_results_folder(job_type):
    """Create results folder structure if it doesn't exist.
    
    Creates: results/{JOB_TYPE}/
    
    Args:
        job_type: The job type (e.g., "AIjobs", "PMjobs")
    """
    job_folder = os.path.join(DEFAULT_RESULTS_FOLDER, job_type)
    if not os.path.exists(job_folder):
        os.makedirs(job_folder)
        log_time(f"Created folder: {job_folder}")
    return job_folder


def filter_language_requirements(df, language_code):
    """Filter out jobs requiring advanced language requirements.
    
    Based on the specified language, filters out jobs that require
    C1/C2 level proficiency or other advanced language skills.
    
    Note: Filters based on job title since description field is often empty
    from the scraper. This still catches explicit language requirements in titles.
    
    Args:
        df: DataFrame with job listings
        language_code: Language code (e.g., "DE", "IT")
        
    Returns:
        Filtered DataFrame
    """
    log_time(f"Filtering out jobs with advanced {language_code} language requirements...")
    
    # Get language-specific required keywords
    lang_config = get_language_config(language_code)
    required_keywords = lang_config.required_keywords
    
    df_before = len(df)
    
    # Build regex patterns that catch word variations
    final_patterns = []
    for kw in required_keywords:
        if "Deutsch" in kw:
            # For keywords with "Deutsch", escape everything and then replace 
            # "Deutsch" with a pattern that matches variations (deutsch, deutschen, deutsche-, etc.)
            escaped = re.escape(kw)
            # Replace the escaped "Deutsch" with flexible pattern
            pattern = escaped.replace("Deutsch", "Deutsch[a-z-]*")
            final_patterns.append(pattern)
        elif "Italiano" in kw:
            # Similar pattern for Italian
            escaped = re.escape(kw)
            pattern = escaped.replace("Italiano", "Italiano[a-z-]*")
            final_patterns.append(pattern)
        else:
            final_patterns.append(re.escape(kw))
    
    combined_pattern = "|".join(final_patterns)
    
    # Search in both title and description (description is often empty)
    title_match = df["title"].str.contains(combined_pattern, case=False, na=False, regex=True)
    desc_match = df["description"].str.contains(combined_pattern, case=False, na=False, regex=True)
    df = df[~(title_match | desc_match)]
    log_time(f"Filtered out {df_before - len(df)} jobs with {language_code} language requirements")
    return df


def filter_by_location(df, custom_locations=None, is_working_student=False):
    """
    Filter jobs by location (optional).
    
    Args:
        df: DataFrame with job listings
        custom_locations: Optional list of location strings to filter by (e.g., ["Hamburg", "Bremen"])
        is_working_student: Boolean indicating whether to include remote jobs (True for WS, False otherwise)
        
    Returns:
        Filtered DataFrame (original if no custom_locations provided)
    """
    if not custom_locations or len(custom_locations) == 0:
        log_time("No location filter applied (location-agnostic search)")
        return df
    
    log_time(f"Filtering for location: {', '.join(custom_locations)}")
    escaped_locations = [re.escape(loc) for loc in custom_locations]
    location_pattern = "|".join(escaped_locations)
    location_match = df["location"].str.contains(location_pattern, case=False, na=False, regex=True)
    
    if is_working_student:
        log_time(f"Including remote jobs for working student positions...")
        is_remote = df["is_remote"].fillna(False) == True
        df = df[location_match | is_remote]
    else:
        df = df[location_match]
    
    return df


def separate_working_student_jobs(df, language_code):
    """
    Separate working student jobs from non-working student jobs.
    
    Args:
        df: DataFrame with job listings
        language_code: Language code (e.g., "DE", "IT")
        
    Returns:
        Tuple of (working_student_df, non_working_student_df)
    """
    log_time("Separating working student jobs from other jobs...")
    lang_config = get_language_config(language_code)
    student_keywords = lang_config.student_keywords
    
    escaped_keywords = [re.escape(kw) for kw in student_keywords]
    student_pattern = "|".join(escaped_keywords)
    student_job_mask = df["title"].str.contains(student_pattern, case=False, na=False, regex=True)
    
    df_working_student = df[student_job_mask]
    df_non_working_student = df[~student_job_mask]
    
    log_time(f"Working student jobs: {len(df_working_student)}")
    log_time(f"Non-working student jobs: {len(df_non_working_student)}")
    
    return df_working_student, df_non_working_student


def scrape_jobs_for_terms(search_terms, search_location, language_code):
    """Scrape jobs for given search terms.
    
    Args:
        search_terms: List of search terms
        search_location: Location to search (e.g., "Germany", "Italy")
        language_code: Language code for logging (e.g., "DE", "IT")
        
    Returns:
        List of DataFrames with job results
    """
    all_jobs = []
    
    log_time(f"Starting scraping for {len(search_terms)} search term(s)")
    
    for term in search_terms:
        log_time(f"\nSearching for: {term}")
        
        for site in SITES:
            log_time(f"  Trying {site}...")
            search_start = datetime.now()
            try:
                jobs = scrape_jobs(
                    site_name=[site],
                    search_term=term,
                    location=search_location,
                    results_wanted=RESULTS_WANTED,
                    hours_old=HOURS_OLD,
                    linkedin_fetch_description=True,
                    description_format="markdown"
                )
                
                search_duration = (datetime.now() - search_start).total_seconds()
                if jobs is not None and len(jobs) > 0:
                    all_jobs.append(jobs)
                    log_time(f"    [OK] {site}: Found {len(jobs)} jobs in {search_duration:.1f}s")
                else:
                    log_time(f"    [--] {site}: No jobs found ({search_duration:.1f}s)")
            except Exception as e:
                search_duration = (datetime.now() - search_start).total_seconds()
                log_time(f"    [ER] {site}: Error - {str(e)[:50]} ({search_duration:.1f}s)")
    
    return all_jobs


def process_and_save_results(job_class, include_ws, include_nonws, language_code, custom_locations=None):
    """Main processing function.
    
    Args:
        job_class: JobClass instance
        include_ws: Boolean to include working student jobs
        include_nonws: Boolean to include non-working student jobs
        language_code: Language code (e.g., "DE", "IT")
        custom_locations: Optional list of locations to filter by (e.g., ["Hamburg", "Bremen"])
    """
    
    # Get job-type-specific folder
    job_folder = ensure_results_folder(job_class.name)
    
    # Get language-specific configuration
    lang_config = get_language_config(language_code)
    
    log_time(f"=== Starting Job Scraper for {job_class.name} ({language_code}) ===")
    log_time(f"Search terms: {', '.join(job_class.search_terms[:3])}{'...' if len(job_class.search_terms) > 3 else ''}")
    log_time(f"Language: {lang_config.name}")
    log_time(f"Include working student: {include_ws}")
    log_time(f"Include non-working student: {include_nonws}")
    if custom_locations:
        log_time(f"Location filter: {', '.join(custom_locations)}")
    
    # Scrape jobs - use country-wide location, filter by location afterwards if provided
    all_jobs = scrape_jobs_for_terms(job_class.search_terms, lang_config.country_search_location, language_code)
    
    if not all_jobs:
        log_time("No jobs found. Exiting.")
        return
    
    log_time("\n=== Processing Results ===")
    log_time("Concatenating results...")
    df = pd.concat(all_jobs, ignore_index=True)
    
    # Remove duplicates
    log_time("Removing duplicates...")
    df_before = len(df)
    df = df.drop_duplicates(subset=["title", "company", "location"])
    log_time(f"Removed {df_before - len(df)} duplicates")
    log_time(f"Total jobs scraped: {len(df)}")
    
    # Filter out language-specific requirements
    df = filter_language_requirements(df, language_code)
    
    # Separate working student jobs from non-working student jobs
    df_working_student, df_non_working_student = separate_working_student_jobs(df, language_code)
    
    # Apply location filtering (only if custom_locations provided)
    if include_ws:
        df_working_student = filter_by_location(df_working_student, custom_locations=custom_locations, is_working_student=True)
        if custom_locations:
            log_time(f"Working student jobs after location filter: {len(df_working_student)}")
    
    if include_nonws:
        df_non_working_student = filter_by_location(df_non_working_student, custom_locations=custom_locations, is_working_student=False)
        if custom_locations:
            log_time(f"Non-working student jobs after location filter: {len(df_non_working_student)}")
    
    # Save results
    log_time("\n=== Saving Results ===")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    total_saved = 0
    
    # Prepare dataframes for saving (exclude description and company_logo, reorder columns)
    df_ws_save = prepare_dataframe_for_save(df_working_student.copy()) if len(df_working_student) > 0 else df_working_student
    df_nonws_save = prepare_dataframe_for_save(df_non_working_student.copy()) if len(df_non_working_student) > 0 else df_non_working_student
    
    if include_ws and len(df_working_student) > 0:
        output_file = os.path.join(job_folder, f"{timestamp}_{job_class.name}_workingstudent-{language_code}.csv")
        df_ws_save.to_csv(output_file, index=False)
        log_time(f"[OK] Saved {len(df_working_student)} working student jobs to {output_file}")
        total_saved += len(df_working_student)
    elif include_ws:
        log_time("No working student jobs to save")
    
    if include_nonws and len(df_non_working_student) > 0:
        output_file = os.path.join(job_folder, f"{timestamp}_{job_class.name}_fulltime-{language_code}.csv")
        df_nonws_save.to_csv(output_file, index=False)
        log_time(f"[OK] Saved {len(df_non_working_student)} non-working student jobs to {output_file}")
        total_saved += len(df_non_working_student)
    elif include_nonws:
        log_time("No non-working student jobs to save")
    
    log_time(f"Total jobs saved: {total_saved}")
    log_time("=== Job Scraper Completed ===")


def print_usage():
    """Print usage information."""
    print("\nUsage: python job_scraper.py <JOB_TYPE> [WS] [nonWS] [--lang LANGUAGE_CODE] [--location LOCATION1 LOCATION2 ...]")
    print("\nArguments:")
    print("  JOB_TYPE:           Type of jobs to scrape (e.g., AIjobs, PMjobs)")
    print("  WS:                 Include working student jobs (optional)")
    print("  nonWS:              Include non-working student jobs (optional)")
    print("  --lang CODE:        Language code for filtering (optional, default: DE)")
    print("                      Supported: DE (German), IT (Italian)")
    print("  --location PLACES:  Location filter for jobs (optional, space-separated)")
    print("                      Example: --location Hamburg Bremen")
    print("                      If not provided, searches all locations globally")
    print("\nExamples:")
    print("  python job_scraper.py PMjobs WS nonWS                              # Global search, default language (DE)")
    print("  python job_scraper.py PMjobs WS nonWS --lang DE                    # German, global")
    print("  python job_scraper.py PMjobs WS nonWS --location Hamburg Bremen    # Specific locations")
    print("  python job_scraper.py PMjobs nonWS --lang IT --location Milano     # Italian, Milano only\n")


def main():
    """Main entry point."""
    
    # Parse arguments
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    job_type = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []
    
    # Validate job type
    try:
        job_class = get_job_class(job_type)
    except ValueError as e:
        print(f"Error: {e}")
        print_usage()
        sys.exit(1)
    
    # Parse WS/nonWS and --lang flags
    include_ws = "WS" in args
    include_nonws = "nonWS" in args
    
    # Extract language code
    language_code = DEFAULT_LANGUAGE
    custom_locations = None
    
    remaining_args = []
    i = 0
    while i < len(args):
        if args[i] == "--lang":
            if i + 1 < len(args):
                language_code = args[i + 1]
                i += 2
            else:
                print("Error: --lang requires a language code")
                print_usage()
                sys.exit(1)
        elif args[i] == "--location":
            # Collect all remaining arguments as locations
            custom_locations = args[i + 1:]
            break
        else:
            remaining_args.append(args[i])
            i += 1
    
    args = remaining_args
    
    # If neither WS nor nonWS specified, default to both
    if not include_ws and not include_nonws:
        include_ws = True
        include_nonws = True
    
    # Validate remaining arguments
    valid_args = {"WS", "nonWS"}
    if args and not all(arg in valid_args for arg in args):
        invalid = [arg for arg in args if arg not in valid_args]
        print(f"Error: Invalid arguments: {', '.join(invalid)}")
        print_usage()
        sys.exit(1)
    
    # Validate language code
    try:
        lang_config = get_language_config(language_code)
    except ValueError as e:
        print(f"Error: {e}")
        print_usage()
        sys.exit(1)
    
    # Run scraper
    try:
        process_and_save_results(job_class, include_ws, include_nonws, language_code, custom_locations=custom_locations)
    except Exception as e:
        log_time(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
