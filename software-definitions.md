# JobScraper Software Definitions

**Last Updated:** April 16, 2026  
**Status:** Active Development  

---

## Changelog

- ✅ Updated language_config.py: German (DE) and Italian (IT) framework
- ✅ Multiple job types implemented: Datajobs, Autojobs, ResAsstjobs, VLSIjobs, ECEjobs
- ✅ File organization: Job-type-specific folders (results/{JOB_TYPE}/)
- ✅ Filename format updated: {timestamp}_{JOB_TYPE}_{employment_type}-{LANGUAGE_CODE}.csv
- ✅ CLI language support: --lang argument with German (DE) default
- ✅ Documentation: Software-definitions.md as single source of truth
- ✅ Initial JobScraper setup 

---

## Project Overview

JobScraper is a modular job scraping tool designed to scrape job postings from multiple sources and filter them by job type, employment type, and language requirements.

---

## Repository Structure

**Available Job Types:**
- PMjobs (Product/Project Management)
- AIjobs (AI/ML/Data Science)
- Datajobs (Data Engineering & Analytics)
- ResAsstjobs (Research & Graduate Research)
- VLSIjobs (VLSI/Chip Design)
- ECEjobs (Electronics & Communications Engineering)
- Autojobs (Automotive Engineering)

---

## Functional Requirements

### 1. Results Organization

**Folder Structure:**
```
results/
├── PMjobs/
├── AIjobs/
├── Datajobs/
├── ResAsstjobs/
├── VLSIjobs/
├── ECEjobs/
└── Autojobs/
```

**File Naming Convention:**
```
{timestamp}_{JOB_TYPE}_{employment_type}-{LANGUAGE_CODE}.csv
```

**Examples:**
- `20260314_143022_EAjobs_fulltime-DE.csv`
- `20260314_143022_Datajobs_workingstudent-IT.csv`

---

### 2. Language Support

**Design Principle:** Modular, expandable language support via CLI

**Currently Supported Languages:**
- German (DE) - Default
- Italian (IT) - Framework in place for future expansion

**CLI Usage:**
```powershell
# Global search (default - no location restrictions)
python job_scraper.py PMjobs WS nonWS

# With language specification
python job_scraper.py PMjobs WS nonWS --lang DE
python job_scraper.py PMjobs WS nonWS --lang IT

# With optional location filter (Hamburg and Berlin)
python job_scraper.py PMjobs WS nonWS --location Hamburg Berlin

# Combined: language + location
python job_scraper.py Datajobs WS --lang DE --location Hamburg
python job_scraper.py PMjobs nonWS --lang IT --location Milano Roma
```

**Language Keywords:**
- Each language has specific filtering keywords for language requirements and employment types
- Language filters are stored in a modular configuration structure
- Easy to add new languages by registering new language configuration

**Current Language Configurations:**

#### German (DE) - Default
- **Advanced German Requirements Keywords:** C1, C2 German proficiency markers (>50 keywords)
- **Working Student Keywords:** werkstudent, intern, thesis, praktikum, hiwi, abschlussarbeit, etc.
- **Country Search Location:** Germany (used for country-wide search before optional location filtering)

#### Italian (IT)
- **Starter Italian Keywords:** Framework ready for expansion
- **Country Search Location:** Italy

**Note:** Location filtering is now completely optional. Default behavior searches globally without location restrictions. Use the `--location` CLI parameter to filter by specific cities/regions if needed.

---

### 3. Job Type Definitions & Keywords

**PMjobs** (Product/Project Management)
- Search Terms: Project Manager, Project Leader, Project Management, Project Lead, Product Manager

**Datajobs** (Data Engineering & Analytics)
- Search Terms: Data Engineering, Data Analytics

**AIjobs** (AI/ML/Data Science)
- Search Terms: machine learning, artificial intelligence, Generative AI, data science, data scientist

**ResAsstjobs** (Research & Graduate Research)
- Search Terms: Research Assistant, Graduate Research

**VLSIjobs** (VLSI/Chip Design Engineering)
- Search Terms: chip design, FPGA Engineer, RTL Design, ASIC Design Engineer, FPGA Developer

**ECEjobs** (Electronics & Communications Engineering)
- Search Terms: Embedded Systems Engineer, Hardware Design Engineer, Signal Processing Engineer, RF Engineer, PCB Design Engineer

**Autojobs** (Automotive Engineering)
- Search Terms: Automotive Design Engineer, Vehicle Dynamics Engineer, Automotive Systems Engineer, CAD Design Engineer (Automotive), Powertrain Engineer

---

## Technical Requirements

### Code Architecture

**Core Components:**
1. `job_scraper.py` - Main scraper with language support
2. `jobs_config.py` - Job type definitions and language configurations
3. `language_config.py` - Language-specific filtering rules (new)

**Key Functions:**
- `get_job_class(job_type)` - Retrieve job type configuration
- `get_language_config(language_code)` - Retrieve language filtering rules
- `ensure_results_folder(job_type)` - Create job-type-specific folders
- `filter_language_requirements(df, language_code)` - Language-specific filtering
- `scrape_jobs_for_terms()` - Core scraping logic
- `process_and_save_results()` - Results processing and saving

**CLI Arguments:**
```
python job_scraper.py <JOB_TYPE> [WS] [nonWS] [--lang LANG_CODE] [--location LOCATION1 LOCATION2 ...]
```

**Default Behavior:**
- Employment Type: Both WS and nonWS (if not specified)
- Language: German (DE) - if not specified
- Location: Global/Unrestricted (if not specified) - optional `--location` parameter for filtering
- Results Location: `results/{JOB_TYPE}/`

### Constraints

**Search Term Limits:**
- GitHub Workflows: Maximum 5 keyword filters per job type
  - Rationale: Predictable execution time for automated runs
- Independent/Local Runs: Unlimited keyword expansion allowed
  - Users can modify `jobs_config.py` to add more keywords

**Location Filtering (Optional):**
- Default: Global search without location restrictions
- Optional: Use `--location` parameter to filter by specific cities/regions
- Working Student with location filter: Includes remote jobs + specified locations
- Full-time with location filter: Filters to specified locations only

**Data Filtering:**
- Advanced German language requirement filtering (C1/C2 German proficiency)
- Duplicate removal (by title, company, location)
- Description and company_logo columns excluded from output

---

## Data Output

### CSV File Format

**Columns (in order):**
1. site
2. title
3. company
4. location
5. date_posted
6. job_url (with trailing space)
7. job_url_direct (with trailing space)
8. (remaining columns from scraper)

**Sorting:**
- By date_posted (newest first)

**Deduplication:**
- By title, company, location

---

## Jupyter Notebook Integration

**Features:**
1. Google Drive integration for saving results to personal Google Drive
2. Same scraping functionality as main script
3. Interactive cells for exploring results
4. Support for language parameter input

**Note:** Requires manual authentication for Google Drive access; not suitable for CI/CD workflows

---

## GitHub Workflows & Automation

### Job Scraper Workflow (job-scraper.yml)

**Purpose:** Automated job scraping across all job types and automatic results archival

**Schedule:** Weekdays at 3:30 PM UTC (cron: `30 15 * * 1-5` = Monday-Friday)

**Job Types Scraped:**
1. PMjobs (Product/Project Management)
2. AIjobs (AI/ML/Data Science)
3. Datajobs (Data Engineering & Analytics)
4. Autojobs (Automotive Engineering)
5. ResAsstjobs (Research & Graduate Research)
6. VLSIjobs (VLSI/Chip Design)
7. ECEjobs (Electronics & Communications Engineering)

**Workflow Steps:**
1. Checkout repository
2. Set up Python 3.11 runtime
3. Install dependencies (python-jobspy, pandas)
4. Execute `job_scraper.py` for each job type with WS and nonWS flags
5. Commit and push results to repository

**Configuration:**
- Default Language: German (DE)
- Employment Types: Both working student and full-time
- Results Location: `results/{JOB_TYPE}/` with timestamps

**Key Differences from Manual Runs:**
- Automated scheduling reduces manual intervention
- Results automatically committed to repository history
- Consistent 5-keyword limit per job type for predictable execution time
- Suitable for long-running CI/CD environments

**Manual Trigger:**
- Available in GitHub Actions tab
- Useful for testing or immediate scraping needs

---

### Cleanup Workflow (cleanup-results.yml)

**Purpose:** Automated maintenance to delete old CSV files and manage disk space

**Schedule:** Daily at 8:30 PM UTC (20:30 UTC cron: `30 20 * * *`)

**Steps:**
1. Checkout repository
2. Set up Python 3.11 runtime
3. Execute cleanup script: `python cleanup_old_results.py`
4. Commit and push changes if files were deleted

**Configurable Parameters:**
- `DAYS_TO_KEEP`: Retention period in days (default: 30)
- `RESULTS_FOLDER`: Target folder for cleanup (default: "results")

**Options:**
- `--dry-run`: Preview files to be deleted without deletion
- `--days N`: Override retention period (e.g., `--days 14`)
- `--verbose`: Print detailed logs of all operations

**Manual Trigger:**
- Available in GitHub Actions tab
- Optional input to enable dry-run mode

---

## Configuration Management

### Default Configuration (German/DE)

```python
SITES = ["linkedin"]
RESULTS_WANTED = 500
HOURS_OLD = 168  # Last 7 days
DEFAULT_LANGUAGE = "DE"
DEFAULT_RESULTS_FOLDER = "results"
CLEANUP_DAYS_TO_KEEP = 30  # Cleanup: Retention period for CSV files
```

### How to Add New Configurations

**Adding a New Language:**
1. Create new language configuration in `language_config.py`
2. Define language-specific keywords (required words, student keywords)
3. Register in language registry
4. Users can now use: `python job_scraper.py AIjobs --lang <NEW_CODE>`

**Adding a New Job Type:**
1. Create new JobClass in `jobs_config.py`
2. Define search terms (limit to 5 for workflows, unlimited for local)
3. Register in JOB_CLASSES registry
4. Users can now use: `python job_scraper.py <NEW_TYPE> [WS] [nonWS]`

---

## Future Enhancements

- [ ] Support for additional languages (Italian, French, Spanish, etc.)
- [ ] Web-based dashboard for job viewing
- [ ] Machine learning-based job relevance scoring
---

## Development Guidelines

### Contribution Requirements

When adding new features or job types:
1. Update this `software-definitions.md` file with new requirements
2. Add corresponding entries to `jobs_config.py`
3. Ensure language-specific filtering is handled
4. Update appropriate README files
5. Test with both WS and nonWS job types
6. Verify folder structure and file naming conventions



## Support & Collaboration

**Open to:**
- New job type suggestions
- Language expansion proposals
- Filter keyword improvements
- New feature ideas

**For Community Contributions:**
- Clone repository
- Add your own job types and filters in your local instance
- Submit pull requests for widely applicable enhancements
---

## Deployment Notes

### GitHub Workflows
- Runs periodically with fixed job types and keyword limits (max 5 per type)
- Results automatically saved to respective job-type folders
- Default language: German (DE)

### Local/Independent Runs
- Users have full flexibility to modify keywords and filters
- Can add unlimited search terms per job type
- Can add new job types as needed
- Google Drive integration available via Jupyter notebook


