#!/usr/bin/env python3
"""
MCP Bug Bounty Research Agent - Setup Configuration
AI-Powered Vulnerability Research with Market-Ready Monetization
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements from requirements.txt
def read_requirements():
    requirements = []
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    requirements.append(line)
    return requirements

setup(
    name="mcp-bugbounty-agent",
    version="1.2.0",
    
    # Package metadata
    description="AI-Powered Bug Bounty Research Agent with MCP Integration and Docker Isolation",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    
    # Author and contact information
    author="Security Research Team",
    author_email="hello@bugbounty-agent.com",
    maintainer="MCP Bug Bounty Agent Team",
    maintainer_email="support@bugbounty-agent.com",
    
    # URLs and links
    url="https://github.com/your-org/mcp-bugbounty-agent",
    download_url="https://github.com/your-org/mcp-bugbounty-agent/releases",
    project_urls={
        "Homepage": "https://bugbounty-agent.com",
        "Documentation": "https://docs.bugbounty-agent.com",
        "Bug Reports": "https://github.com/your-org/mcp-bugbounty-agent/issues",
        "Source": "https://github.com/your-org/mcp-bugbounty-agent",
        "Discord": "https://discord.gg/bugbounty-agent",
        "Premium": "https://bugbounty-agent.com/premium",
        "Enterprise": "https://calendly.com/bugbounty-agent",
    },
    
    # Package discovery
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    
    # Python version requirement
    python_requires=">=3.8",
    
    # Dependencies
    install_requires=[
        "requests>=2.31.0",
        "docker>=6.1.0",
        "colorama>=0.4.6",
        "beautifulsoup4>=4.12.2",
        "urllib3>=2.0.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
    ],
    
    # Optional dependencies for different features
    extras_require={
        "premium": [
            "stripe>=7.0.0",
            "cryptography>=41.0.0",
        ],
        "development": [
            "pytest>=7.4.0",
            "black>=23.12.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
        ],
        "docker": [
            "docker>=6.1.0",
        ],
        "monitoring": [
            "prometheus-client>=0.19.0",
            "structlog>=23.2.0",
        ],
        "docs": [
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.4.0",
        ],
        "ml": [
            "scikit-learn>=1.3.0",
            "numpy>=1.24.0",
        ],
        "cloud": [
            "boto3>=1.34.0",  # AWS
            "azure-identity>=1.15.0",  # Azure
            "google-cloud-storage>=2.10.0",  # GCP
        ],
        "all": [
            "stripe>=7.0.0",
            "cryptography>=41.0.0",
            "docker>=6.1.0",
            "prometheus-client>=0.19.0",
            "structlog>=23.2.0",
            "scikit-learn>=1.3.0",
            "numpy>=1.24.0",
            "boto3>=1.34.0",
        ],
    },
    
    # Console scripts / CLI entry points
    entry_points={
        "console_scripts": [
            "mcp-bugbounty=mcp_bugbounty_agent.cli:main",
            "mcp-agent=mcp_bugbounty_agent.cli:main",
            "bugbounty-agent=mcp_bugbounty_agent.cli:main",
        ],
    },
    
    # Package data and files
    package_data={
        "mcp_bugbounty_agent": [
            "data/*.json",
            "data/*.yml",
            "templates/*.md",
            "templates/*.py",
            "payloads/*.txt",
        ],
    },
    
    # Classification for PyPI
    classifiers=[
        # Development Status
        "Development Status :: 4 - Beta",
        
        # Intended Audience
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        
        # License
        "License :: OSI Approved :: MIT License",
        
        # Operating System
        "Operating System :: OS Independent",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        
        # Programming Language
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        
        # Topic Classification
        "Topic :: Security",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Networking :: Monitoring",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        
        # Natural Language
        "Natural Language :: English",
        
        # Environment
        "Environment :: Console",
        "Environment :: Web Environment",
        
        # Framework
        "Framework :: AsyncIO",
    ],
    
    # Keywords for search
    keywords=[
        "security", "bug-bounty", "vulnerability", "penetration-testing",
        "ai", "automation", "docker", "mcp", "burp-suite", "idor",
        "authentication-bypass", "business-logic", "cryptocurrency",
        "ethical-hacking", "security-research", "vulnerability-assessment",
        "aws", "marketplace", "freemium", "saas"
    ],
    
    # Zip safe
    zip_safe=False,
    
    # Additional metadata
    platforms=["any"],
    license="MIT",
    
    # Test suite
    test_suite="tests",
    tests_require=[
        "pytest>=7.4.0",
        "pytest-asyncio>=0.21.0",
        "pytest-docker>=2.0.0",
        "pytest-mock>=3.12.0",
    ],
    
    # Command line options for development
    options={
        "build_scripts": {
            "executable": "/usr/bin/env python3",
        },
    },
)