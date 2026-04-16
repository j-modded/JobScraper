#!/usr/bin/env python3
"""
Cleanup script for JobScraper results.

Deletes CSV files in results/ subdirectories that are older than 30 days.
Useful for managing storage and keeping only recent job listings.
"""

import os
import time
from datetime import datetime, timedelta
import glob

# Configuration
RESULTS_DIR = "results"
MAX_AGE_DAYS = 30


def get_file_age_days(file_path):
    """Get age of file in days.
    
    Args:
        file_path: Path to file
        
    Returns:
        Age in days
    """
    file_mtime = os.path.getmtime(file_path)
    file_age_seconds = time.time() - file_mtime
    file_age_days = file_age_seconds / (24 * 3600)
    return file_age_days


def cleanup_old_results(max_age_days=MAX_AGE_DAYS, dry_run=False):
    """Delete CSV files older than specified days in results/ subdirectories.
    
    Args:
        max_age_days: Maximum age in days (default: 30)
        dry_run: If True, only show what would be deleted without actually deleting
        
    Returns:
        Dictionary with cleanup statistics
    """
    
    stats = {
        'total_files_checked': 0,
        'files_deleted': 0,
        'total_size_freed': 0,
        'deleted_files': [],
        'errors': []
    }
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Starting cleanup of old CSV files (max age: {max_age_days} days)")
    print(f"[{timestamp}] Results directory: {RESULTS_DIR}")
    
    if not os.path.exists(RESULTS_DIR):
        print(f"[{timestamp}] ERROR: Results directory not found: {RESULTS_DIR}")
        return stats
    
    # Iterate through all subdirectories in results/
    for job_type_dir in glob.glob(os.path.join(RESULTS_DIR, "*")):
        if not os.path.isdir(job_type_dir):
            continue
        
        job_type = os.path.basename(job_type_dir)
        print(f"\n[{timestamp}] Processing directory: {job_type}")
        
        # Find all CSV files in this subdirectory
        csv_files = glob.glob(os.path.join(job_type_dir, "*.csv"))
        
        if not csv_files:
            print(f"[{timestamp}]   No CSV files found")
            continue
        
        print(f"[{timestamp}]   Found {len(csv_files)} CSV files")
        
        for csv_file in csv_files:
            stats['total_files_checked'] += 1
            
            try:
                file_age_days = get_file_age_days(csv_file)
                file_size = os.path.getsize(csv_file)
                file_name = os.path.basename(csv_file)
                
                if file_age_days > max_age_days:
                    if dry_run:
                        print(
                            f"[{timestamp}]   [DRY RUN] Would delete: {file_name} "
                            f"(age: {file_age_days:.1f} days, size: {file_size / 1024:.1f} KB)"
                        )
                    else:
                        os.remove(csv_file)
                        print(
                            f"[{timestamp}]   [DELETED] {file_name} "
                            f"(age: {file_age_days:.1f} days, size: {file_size / 1024:.1f} KB)"
                        )
                        stats['files_deleted'] += 1
                        stats['total_size_freed'] += file_size
                        stats['deleted_files'].append({
                            'file': file_name,
                            'age_days': file_age_days,
                            'size_bytes': file_size
                        })
                else:
                    print(
                        f"[{timestamp}]   [KEPT] {file_name} "
                        f"(age: {file_age_days:.1f} days)"
                    )
            
            except Exception as e:
                error_msg = f"Error processing {csv_file}: {str(e)}"
                print(f"[{timestamp}]   [ERROR] {error_msg}")
                stats['errors'].append(error_msg)
    
    # Print summary
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{timestamp}] ========== CLEANUP SUMMARY ==========")
    print(f"[{timestamp}] Total files checked: {stats['total_files_checked']}")
    print(f"[{timestamp}] Files deleted: {stats['files_deleted']}")
    print(f"[{timestamp}] Space freed: {stats['total_size_freed'] / 1024 / 1024:.2f} MB")
    
    if stats['errors']:
        print(f"[{timestamp}] Errors encountered: {len(stats['errors'])}")
        for error in stats['errors']:
            print(f"[{timestamp}]   - {error}")
    
    print(f"[{timestamp}] ====================================")
    
    return stats


if __name__ == "__main__":
    import sys
    
    # Check for dry-run flag
    dry_run = "--dry-run" in sys.argv
    
    if dry_run:
        print("Running in DRY-RUN mode (no files will be deleted)\n")
    
    cleanup_old_results(max_age_days=MAX_AGE_DAYS, dry_run=dry_run)
