# JobScraper

A modular, multilingual job scraping tool that scrapes job postings for different job categories from multiple sources. 
Supports filtering by job type, employment type (working student vs. full-time), and +*MOST importantly*+ language requirements.

## Key Features

- **Multiple Job Types**: Scrape 7 different categories of jobs with specialized keywords
- **Modular Language Support**: Default German (DE) with framework for additional languages (Italian, etc.)
- **Smart Filtering**: 
  - Language requirement filtering (C1/C2 proficiency markers)
  - Working student vs. full-time job separation
  - Location-based filtering
- **Organized Output**: Results automatically saved to job-type-specific folders with language code indicators
- **Jupyter notebook with and without Google Colab Integration**: Jupyter notebook available for saving results to Google Drive
- **Open to Contributions**: Community contributions welcome for new job types and improvements

## Available Job Types

- **PMjobs** - Product/Project Management positions
- **Datajobs** - Data Engineering & Analytics positions
- **Autojobs** - Automotive Engineering positions
- **AIjobs** - AI/ML/Data Science positions
- **ResAsstjobs** - Research & Graduate Research positions
- **VLSIjobs** - VLSI/Chip Design Engineering positions
- **ECEjobs** - Electronics & Communications Engineering positions



## Quick Start

### 1. Setup

**Clone the repository:**
```powershell
git clone https://github.com/j-modded/JobScraper.git
cd JobScraper
```

**Create and activate virtual environment:**
```powershell
python -m venv .venv
.\venv\Scripts\Activate.ps1
```

**Install dependencies:**
```powershell
pip install -r requirements.txt
```

### 2. Run the Scraper

**Basic usage (German language, both job types):**
```powershell
python job_scraper.py PMjobs WS nonWS
```

**With language specification:**
```powershell
python job_scraper.py Datajobs WS nonWS --lang DE
```

**Working student jobs only:**
```powershell
python job_scraper.py Autojobs WS
```

**Full-time jobs only:**
```powershell
python job_scraper.py PMjobs nonWS
```

## Usage

### Command Format

```powershell
python job_scraper.py <JOB_TYPE> [WS] [nonWS] [--lang LANGUAGE_CODE]
```

### Arguments

- **JOB_TYPE**: Type of jobs to scrape (required)
  - `PMjobs` - Product/Project Management positions
  - `Datajobs` - Data Engineering & Analytics positions
  - `Autojobs` - Automotive Engineering positions
  - `ResAsstjobs` - Research & Graduate Research positions
  - `AIjobs` - AI/ML positions
  - `VLSIjobs` - VLSI/Chip Design Engineering positions
  - `ECEjobs` - Electronics & Communications Engineering positions
  
- **WS** (optional): Include working student positions
- **nonWS** (optional): Include full-time positions
- **--lang CODE** (optional): Language code for filtering (default: DE)
  - `DE` - German (default)
  - `IT` - Italian (framework available)

### Employment Types

If no employment type is specified, both WS and nonWS jobs are included.

### Examples

```powershell


# Data Engineering jobs - full-time only
python job_scraper.py Datajobs nonWS --lang DE

# Product Management jobs - both types, default language
python job_scraper.py PMjobs

# VLSI/Chip Design jobs - working student only
python job_scraper.py VLSIjobs WS

# Automotive jobs - both types
python job_scraper.py Autojobs WS nonWS

# Research Assistant jobs
python job_scraper.py ResAsstjobs WS

# Electronics & Communications jobs
python job_scraper.py ECEjobs nonWS --lang DE
```

## Job Types Overview

### PMjobs (Product/Project Management)
- Search terms (5): Project Manager, Project Leader, Project Management, Project Lead, Product Manager

### Datajobs (Data Engineering & Analytics)
- Search terms (2): Data Engineering, Data Analytics

### Autojobs (Automotive Engineering)
- Search terms (5): Automotive Design Engineer, Vehicle Dynamics Engineer, Automotive Systems Engineer, CAD Design Engineer (Automotive), Powertrain Engineer

### ResAsstjobs (Research & Graduate Research)
- Search terms (2): Research Assistant, Graduate Research

### AIjobs (AI/ML/Data Science)
- Search terms (5): machine learning, artificial intelligence, Generative AI, data science, data scientist

### VLSIjobs (VLSI/Chip Design Engineering)
- Search terms (5): chip design, FPGA Engineer, RTL Design, ASIC Design Engineer, FPGA Developer

### ECEjobs (Electronics & Communications Engineering)
- Search terms (5): Embedded Systems Engineer, Hardware Design Engineer, Signal Processing Engineer, RF Engineer, PCB Design Engineer

## Output Files

Results are organized by job type and language:

### Folder Structure
```
results/
├── PMjobs/
│   ├── 20260314_143022_PMjobs_workingstudent-DE.csv
│   ├── 20260314_143022_PMjobs_fulltime-DE.csv
│   └── ...
├── Datajobs/
├── Autojobs/
├── ResAsstjobs/
├── VLSIjobs/
└── ECEjobs/
```

### Filename Format
```
{timestamp}_{JOB_TYPE}_{employment_type}-{LANGUAGE_CODE}.csv
```

**Example:**
- `20260314_143022_PMjobs_workingstudent-DE.csv` - PM jobs, working student, German
- `20260314_143022_EAjobs_fulltime-DE.csv` - Enterprise Architecture, full-time, German

### CSV Content

**Columns (in order):**
1. site
2. title
3. company
4. location
5. date_posted
6. job_url (clickable link)
7. job_url_direct
8. Additional fields from scraper

**Features:**
- Sorted by date (newest first)
- Duplicates removed (by title, company, location)
- Description and company_logo columns excluded for brevity

## Google Colab Integration

A Jupyter notebook (`JobScraper_Colab.ipynb`) is available for running the scraper in Google Colab and saving results directly to Google Drive.

### Using the Notebook

1. Open [JobScraper_Colab.ipynb](JobScraper_Colab.ipynb) in Google Colab
2. Run cells from top to bottom
3. Authenticate with Google Drive when prompted
4. Results are saved to `/MyDrive/JobScraper_Results/`

**Advantages of notebook version:**
- Results saved to your personal Google Drive
- No local installation needed
- Work with custom job types and filters
- Unlimited keyword expansion for independent runs

**Note:** Notebook approach requires manual authentication; not suitable for unattended CI/CD workflows.

## GitHub Workflows

The repository includes automated GitHub Actions workflows for scraping and maintenance tasks.

### Job Scraper Workflow (job-scraper.yml)

**Purpose:** Automatically scrape jobs across all job types and commit results to the repository.

**Schedule:** Runs on **weekdays at 3:30 PM UTC** (Monday-Friday)

**Features:**
- Scrapes all 7 job types (PMjobs, Datajobs, Autojobs, AIjobs, ResAsstjobs, VLSIjobs, ECEjobs)
- Includes both working student (WS) and full-time (nonWS) positions
- Automatically commits results to repository
- Can be triggered manually from GitHub UI
- Uses Python 3.11 with latest dependencies

**Job Types Scraped:**
1. PMjobs (Product/Project Management)
2. Datajobs (Data Engineering & Analytics)
3. Autojobs (Automotive Engineering)
3. AIjobs (AI/ML jobs)
5. ResAsstjobs (Research & Graduate Research)
6. VLSIjobs (VLSI/Chip Design)
7. ECEjobs (Electronics & Communications Engineering)

**Manual Trigger:**
```
Go to Actions → Job Scraper Auto-Run → Run workflow
```

**Configuration:**
- Edit `job_scraper.yml` to change schedule (cron: `30 15 * * 1-5` for 3:30 PM UTC on weekdays)
- Modify job types list to add or remove job categories
- Results are saved to `results/{JOB_TYPE}/` folders with language-specific filenames

### Cleanup Workflow (cleanup-results.yml)

**Purpose:** Automatically delete CSV files older than 30 days from the `results/` directory to manage disk space.

**Schedule:** Runs daily at **8:30 PM UTC** (20:30 UTC)

**Features:**
- Scans all subdirectories in `results/` folder
- Identifies CSV files older than 30 days (configurable)
- Automatically deletes expired files
- Can be triggered manually from GitHub UI with optional dry-run mode
- Commits cleanup results back to repository

**Manual Trigger:**
```
Go to Actions → Cleanup Old Results → Run workflow
Optional: Enable dry-run mode to preview files without deleting
```

**Configuration:**
- Edit `cleanup_old_results.py` to change retention period (default: 30 days)
- Use `--days` argument to override retention period per run
- Use `--dry-run` flag to preview deletions

**Example commands (local execution):**
```powershell
# Delete files older than 30 days (default)
python cleanup_old_results.py

# Preview files to be deleted without deleting
python cleanup_old_results.py --dry-run

# Delete files older than 14 days
python cleanup_old_results.py --days 14

# Verbose output with detailed file information
python cleanup_old_results.py --verbose
```

## Filtering Logic

#### Language Filtering

Jobs are filtered out if they require:
- C1 or C2 language proficiency
- "Verhandlungssicher" (business fluent) language
- "Fließend" (fluent) language
- Other advanced language requirements

Default language: German (DE) - Supports German, Italian, and can be extended

#### Location Filtering (Optional)

By default, the scraper searches **globally** without location restrictions. You can optionally filter by specific locations:

**Examples with location filter:**
```powershell
# Search for Berlin only (working student positions include remote)
python job_scraper.py PMjobs WS --location  Berlin


**Without location filter (default):**
```powershell
# Global search - no location restrictions
python job_scraper.py PMjobs WS nonWS
python job_scraper.py PMjobs WS --lang DE
```

### Deduplication

Jobs are deduplicated by:
- Title
- Company name
- Location

## Technical Details

### Configuration

- **API**: LinkedIn Jobs via `jobspy` library
- **Results Limit**: 500 per search term
- **Search Time**: Last 7 days (168 hours)
- **Output Format**: CSV with UTF-8 encoding

### Language Support Architecture

The application uses a modular language configuration system:
- Each language has its own filtering keywords
- Easy to add new languages by creating new configurations
- Support for language-specific location restrictions
- Default language: German (DE)

### Adding New Languages

To add support for a new language:
1. Add language configuration to `language_config.py`
2. Define language-specific keywords
3. Register in language registry
4. Users can then use: `python job_scraper.py PMjobs --lang <NEW_CODE>`

### Adding New Job Types

**For Independent Users:**
1. Edit `jobs_config.py` and add a new `JobClass`
2. Run: `python job_scraper.py <NEW_TYPE> WS nonWS`
3. No keyword limits - add as many as needed

**For GitHub Workflow Contributions:**
- Maximum 5 keywords per job type (for predictable execution time)
- Submit pull request with new class in `jobs_config.py`
- Update this README with new job type

## GitHub Workflows

Automated job scraping is configured via GitHub Actions:

- **Location**: `.github/workflows/`
- **Schedule**: Daily at 19:00 UTC (adjustable)
- **Job Types**: All configured job types
- **Language**: German (DE)

### Running Workflows

Workflows automatically:
1. Scrape all job types
2. Apply language and employment filters
3. Save results to results folder by job type
4. Commit results to repository

### Modifying Workflow

To add new job types or change schedules:
1. Edit `.github/workflows/job_scraper.yml`
2. Modify job list or cron schedule
3. Keep keyword count ≤ 5 per job type for stability

## Constraints

### GitHub Workflow Limits
- Maximum 5 keywords per job type
- Reason: Predictable execution time for automated runs

### Independent/Local Runs
- Unlimited keywords per job type
- Full control over filtering logic
- Can modify any configuration

## Troubleshooting

### No jobs found
- Check internet connection
- Verify job type name is correct
- Try different search keywords or broader job category

### Jobs with wrong locations
- Location filtering is based on job posting details
- Some remote jobs may be mislabeled by LinkedIn
- Manual review recommended

### Language filtering too aggressive
- If too many relevant jobs are filtered, review keywords in `language_config.py`
- Language requirements are based on job title keywords

## Repository Information

- **Repository Type**: Public
- **Available Job Types**: PMjobs, AIjobs, Datajobs, Autojobs, ResAsstjobs, VLSIjobs, ECEjobs
- **Supported Languages**: German (DE), Italian (IT - framework)
- **Last Updated**: April 17, 2026

## Contributing to Your Own Repo

If you clone this repository and want to customize it:

1. **Add new job types**: Edit `jobs_config.py` to add your job categories
2. **Modify keywords**: Adjust search terms in job class definitions
3. **Change filters**: Update language configs in `language_config.py`
4. **Run independently**: You have full control over keyword limits

No contribution to main repo needed - this is intended for personal/team use.

## Open to Community

This project is open to:
- New job type suggestions
- Language expansion proposals
- Filter keyword improvements
- New feature ideas and bug reports

Feel free to fork and adapt for your specific needs!

## Technical Documentation

For detailed technical information, architecture decisions, and development guidelines, see [software-definitions.md](software-definitions.md).

## Requirements

- Python 3.11+
- pandas
- python-jobspy
- numpy

## License

See LICENSE file (if applicable)

## Contact & Support

Project maintained by: [Your Name/Organization]
For questions or suggestions: [Contact method]


## File Structure

- `job_scraper.py` - Main scraper script with CLI interface
- `jobs_config.py` - Job category definitions and configurations
- `results/` - Output directory for CSV files
- `requirements.txt` - Python dependencies

## Dependencies

- `python-jobspy` - Job scraping library
- `pandas` - Data manipulation and CSV export

## Adding New Job Categories

To add a new job category:

1. Edit `jobs_config.py`
2. Create a new class inheriting from `JobClass`:
   ```python
   class MyJobType(JobClass):
       def __init__(self):
           search_terms = ["term1", "term2", ...]
           super().__init__("MyJobType", search_terms)
   ```
3. Register in `JOB_CLASSES` dictionary:
   ```python
   JOB_CLASSES = {
       ...existing entries...
       "MyJobType": MyJobType
   }
   ```
4. Use it: `python job_scraper.py MyJobType WS nonWS`
