"""
Job class definitions for different job categories.
Each job class defines search terms and metadata for scraping.
"""

class JobClass:
    """Base class for job categories."""
    
    def __init__(self, name, search_terms):
        self.name = name
        self.search_terms = search_terms
    
    def __repr__(self):
        return f"{self.name}({len(self.search_terms)} search terms)"


class PMjobs(JobClass):
    """Product/Project Management related jobs."""
    
    def __init__(self):
        search_terms = [
            "Project Manager",
            "Project Leader",
            "Project Management",
            "Project Lead",
            "Product Manager"
        ]
        super().__init__("PMjobs", search_terms)



class Autojobs(JobClass):
    """Automotive Engineering related jobs."""
    
    def __init__(self):
        search_terms = [
            "Automotive Design Engineer",
            "Vehicle Dynamics Engineer",
            "Automotive Systems Engineer",
            "CAD Design Engineer (Automotive)",
            "Powertrain Engineer"
        ]
        super().__init__("Autojobs", search_terms)

        

class Datajobs(JobClass):
    """Data Engineering & Analytics related jobs."""
    
    def __init__(self):
        search_terms = [
            "Data Engineering",
            "Data Analytics"
        ]
        super().__init__("Datajobs", search_terms)



class AIjobs(JobClass):
    """AI/ML related jobs."""
    
    def __init__(self):
        search_terms = [
            "machine learning",
            "artificial intelligence",
            "Generative AI",
            "data science",
            "data scientist"
        ]
        super().__init__("AIjobs", search_terms)





class ResAsstjobs(JobClass):
    """Research Assistant & Graduate Research positions."""
    
    def __init__(self):
        search_terms = [
            "Research Assistant",
            "Graduate Research"
        ]
        super().__init__("ResAsstjobs", search_terms)


class VLSIjobs(JobClass):
    """VLSI/Chip Design Engineering related jobs."""
    
    def __init__(self):
        search_terms = [
            "chip design",
            "FPGA Engineer",
            "RTL Design",
            "ASIC Design Engineer",
            "FPGA Developer"
        ]
        super().__init__("VLSIjobs", search_terms)


class ECEjobs(JobClass):
    """Electronics & Communications Engineering related jobs."""
    
    def __init__(self):
        search_terms = [
            "Embedded Systems Engineer",
            "Hardware Design Engineer",
            "Signal Processing Engineer",
            "RF Engineer",
            "PCB Design Engineer"
        ]
        super().__init__("ECEjobs", search_terms)


# Registry of available job classes for easy lookup
JOB_CLASSES = {
    "PMjobs": PMjobs,
    "Datajobs": Datajobs,
    "AIjobs": AIjobs,
    "Autojobs": Autojobs,
    "ResAsstjobs": ResAsstjobs,
    "VLSIjobs": VLSIjobs,
    "ECEjobs": ECEjobs
}


def get_job_class(job_type):
    """Get a job class instance by name.
    
    Args:
        job_type: The name of the job type (e.g., "PMjobs", "Datajobs")
        
    Returns:
        JobClass instance
        
    Raises:
        ValueError: If job type is not found
    """
    if job_type not in JOB_CLASSES:
        available = ", ".join(sorted(JOB_CLASSES.keys()))
        raise ValueError(f"Unknown job type '{job_type}'. Available types: {available}")
    return JOB_CLASSES[job_type]()
