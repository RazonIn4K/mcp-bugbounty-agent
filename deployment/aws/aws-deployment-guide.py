#!/usr/bin/env python3
"""
AWS Bedrock Deployment Guide for MCP Bug Bounty Agent
Student-friendly deployment with cost optimization and step-by-step instructions
"""

import json
import os
from datetime import datetime
from pathlib import Path

def load_bedrock_config():
    """Load and validate bedrock agent configuration"""
    config_path = Path("bedrock-agent-config.json")
    if not config_path.exists():
        return None, "❌ bedrock-agent-config.json not found"
    
    try:
        with open(config_path) as f:
            config = json.load(f)
        
        required_fields = ['agentName', 'description', 'foundationModel', 'instruction']
        missing = [field for field in required_fields if field not in config]
        
        if missing:
            return None, f"❌ Missing required fields: {missing}"
        
        return config, "✅ Configuration loaded successfully"
    
    except json.JSONDecodeError as e:
        return None, f"❌ Invalid JSON: {e}"
    except Exception as e:
        return None, f"❌ Error loading config: {e}"

def validate_policy_files():
    """Check if IAM policy files exist and are valid JSON"""
    files_to_check = {
        "trust-policy.json": "IAM trust policy",
        "permission-policy.json": "IAM permission policy"
    }
    
    results = {}
    for filename, description in files_to_check.items():
        filepath = Path(filename)
        if not filepath.exists():
            results[filename] = f"❌ {description} file missing"
            continue
        
        try:
            with open(filepath) as f:
                json.load(f)
            results[filename] = f"✅ {description} valid"
        except json.JSONDecodeError:
            results[filename] = f"❌ {description} invalid JSON"
        except Exception as e:
            results[filename] = f"❌ {description} error: {e}"
    
    return results

def generate_aws_cli_commands(config):
    """Generate AWS CLI commands for deployment"""
    role_name = "BedrockMCPAgentRole"
    region = "us-east-1"
    
    commands = [
        {
            "step": "1. Create IAM Role",
            "description": "Create IAM role with Bedrock trust relationship",
            "command": f"""aws iam create-role \\
    --role-name {role_name} \\
    --assume-role-policy-document file://trust-policy.json \\
    --description "IAM role for MCP Bug Bounty Agent on Amazon Bedrock" \\
    --region {region}""",
            "validation": f"aws iam get-role --role-name {role_name} --query 'Role.Arn' --output text"
        },
        {
            "step": "2. Attach IAM Policy",
            "description": "Attach permissions policy to the role",
            "command": f"""aws iam put-role-policy \\
    --role-name {role_name} \\
    --policy-name MCPBugBountyAgentPolicy \\
    --policy-document file://permission-policy.json""",
            "validation": f"aws iam list-role-policies --role-name {role_name}"
        },
        {
            "step": "3. Create Bedrock Agent",
            "description": "Create the agent with Claude 3 Sonnet model",
            "command": f"""aws bedrock-agent create-agent \\
    --agent-name "{config['agentName']}" \\
    --description "{config['description']}" \\
    --foundation-model "{config['foundationModel']}" \\
    --instruction '{config['instruction']}' \\
    --agent-role-arn "arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/{role_name}" \\
    --region {region}""",
            "validation": f"aws bedrock-agent list-agents --query 'agentSummaries[?agentName==`{config['agentName']}`]' --output table"
        },
        {
            "step": "4. Prepare Agent",
            "description": "Create working draft for the agent",
            "command": f"""aws bedrock-agent prepare-agent \\
    --agent-id $(aws bedrock-agent list-agents --query 'agentSummaries[?agentName==`{config["agentName"]}`].agentId' --output text) \\
    --region {region}""",
            "validation": "# Check agent status shows PREPARED"
        },
        {
            "step": "5. Create Production Alias",
            "description": "Create alias for production testing",
            "command": f"""aws bedrock-agent create-agent-alias \\
    --agent-id $(aws bedrock-agent list-agents --query 'agentSummaries[?agentName==`{config["agentName"]}`].agentId' --output text) \\
    --agent-alias-name "production" \\
    --description "Production alias for MCP Bug Bounty Agent" \\
    --region {region}""",
            "validation": "# Agent alias created successfully"
        },
        {
            "step": "6. Test Agent",
            "description": "Test with NiceHash IDOR analysis query",
            "command": f"""aws bedrock-agent-runtime invoke-agent \\
    --agent-id $(aws bedrock-agent list-agents --query 'agentSummaries[?agentName==`{config["agentName"]}`].agentId' --output text) \\
    --agent-alias-id $(aws bedrock-agent list-agent-aliases --agent-id $(aws bedrock-agent list-agents --query 'agentSummaries[?agentName==`{config["agentName"]}`].agentId' --output text) --query 'agentAliasSummaries[0].agentAliasId' --output text) \\
    --session-id "test-session-$(date +%s)" \\
    --input-text "Research IDOR vulnerabilities in the NiceHash platform with Burp Suite payload generation" \\
    --region {region}""",
            "validation": "# Should return structured vulnerability analysis with $7K-$16K bounty estimates"
        }
    ]
    
    return commands

def generate_console_instructions():
    """Generate AWS Console step-by-step instructions"""
    instructions = [
        {
            "section": "🌐 AWS Console Access",
            "steps": [
                "1. Navigate to https://console.aws.amazon.com",
                "2. Sign in with your AWS account (use AWS Educate if available)",
                "3. Select region: us-east-1 (N. Virginia) - best for students",
                "4. Verify you have appropriate permissions for IAM and Bedrock"
            ]
        },
        {
            "section": "👤 IAM Role Setup",
            "steps": [
                "1. Go to IAM Console → Roles → Create role",
                "2. Select 'AWS service' → 'Bedrock' (if available)",
                "3. Or select 'Custom trust policy' and paste trust-policy.json content",
                "4. Role name: BedrockMCPAgentRole",
                "5. Click 'Create role'",
                "6. Click the created role → Add permissions → Create inline policy",
                "7. JSON tab → paste permission-policy.json content",
                "8. Policy name: MCPBugBountyAgentPolicy",
                "9. Save the Role ARN for later use"
            ]
        },
        {
            "section": "🤖 Bedrock Agent Creation",
            "steps": [
                "1. Go to Amazon Bedrock Console",
                "2. Check 'Model access' → Request access to Anthropic Claude models",
                "3. Wait for approval (usually instant)",
                "4. Go to 'Agents' → Create agent",
                "5. Agent name: MCP-BugBountyAgent",
                "6. Description: AI-powered vulnerability research agent...",
                "7. Foundation model: Anthropic Claude 3 Sonnet",
                "8. IAM role: BedrockMCPAgentRole",
                "9. Paste agent instructions from bedrock-agent-config.json",
                "10. Add tags: Environment=Production, Application=BugBountyResearch",
                "11. Create agent"
            ]
        },
        {
            "section": "🧪 Testing & Validation",
            "steps": [
                "1. Create working draft in agent console",
                "2. Create alias 'production' for testing",
                "3. Test with query: 'Research IDOR vulnerabilities in NiceHash platform'",
                "4. Verify output includes PoC templates and bounty estimates",
                "5. Check CloudWatch logs for any errors",
                "6. Monitor costs in billing dashboard"
            ]
        }
    ]
    
    return instructions

def estimate_student_costs():
    """Provide student-friendly cost estimates"""
    return {
        "deployment_costs": {
            "IAM roles": "$0.00 (free)",
            "Bedrock agent creation": "$0.00 (free)",
            "S3 storage": "$0.00 (within free tier)"
        },
        "usage_costs": {
            "Claude 3 Sonnet input": "$0.003 per 1K tokens",
            "Claude 3 Sonnet output": "$0.015 per 1K tokens",
            "Typical vulnerability analysis": "$0.01 - $0.05 per query",
            "Daily testing (50 queries)": "$0.50 - $2.50",
            "Monthly development": "$15 - $75"
        },
        "student_savings": {
            "AWS Educate credits": "Up to $100 free credits",
            "Free tier benefits": "12 months free S3, CloudWatch",
            "Cost optimization tips": [
                "Use shorter test queries during development",
                "Clean up test resources regularly",
                "Set billing alerts at $10, $25, $50",
                "Monitor usage with AWS Cost Explorer"
            ]
        }
    }

def generate_deployment_report():
    """Generate comprehensive deployment guide"""
    print("🚀 AWS Bedrock Deployment Guide - MCP Bug Bounty Agent")
    print("=" * 70)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Target: July 15, 2025 Launch Ready")
    print("💰 Student-Optimized with AWS Educate Integration")
    
    # Load and validate configuration
    print("\n🔍 Pre-deployment Validation:")
    print("-" * 30)
    
    config, config_msg = load_bedrock_config()
    print(f"   {config_msg}")
    
    if not config:
        print("\n💡 Create bedrock-agent-config.json with required fields:")
        print("   agentName, description, foundationModel, instruction")
        return False
    
    # Validate policy files
    policy_results = validate_policy_files()
    for filename, result in policy_results.items():
        print(f"   {result}")
    
    missing_policies = [f for f, r in policy_results.items() if "❌" in r]
    if missing_policies:
        print(f"\n💡 Create missing policy files: {', '.join(missing_policies)}")
        print("   Use aws-iam-setup.py to generate them")
        return False
    
    # Cost estimation
    print("\n💰 Student Cost Estimate:")
    print("-" * 25)
    costs = estimate_student_costs()
    
    print("   Deployment: FREE")
    for item, cost in costs["deployment_costs"].items():
        print(f"     • {item}: {cost}")
    
    print("\n   Usage (Pay-per-query):")
    for item, cost in costs["usage_costs"].items():
        print(f"     • {item}: {cost}")
    
    print("\n   💡 Student Savings:")
    print(f"     • {costs['student_savings']['AWS Educate credits']}")
    print(f"     • {costs['student_savings']['Free tier benefits']}")
    
    # AWS CLI Commands
    print("\n🛠️ AWS CLI Deployment Commands:")
    print("-" * 35)
    
    commands = generate_aws_cli_commands(config)
    for cmd_info in commands:
        print(f"\n{cmd_info['step']}")
        print(f"   {cmd_info['description']}")
        print(f"   Command:")
        for line in cmd_info['command'].split('\n'):
            print(f"     {line}")
        if 'validation' in cmd_info:
            print(f"   Validation: {cmd_info['validation']}")
    
    # Console Instructions
    print("\n🖱️ AWS Console Alternative:")
    print("-" * 30)
    instructions = generate_console_instructions()
    for section in instructions:
        print(f"\n{section['section']}:")
        for step in section['steps']:
            print(f"   {step}")
    
    # Final recommendations
    print("\n✅ Deployment Recommendations:")
    print("   1. 🎓 Use AWS Educate for free credits and tutorials")
    print("   2. ⚠️  Set up billing alerts before starting")
    print("   3. 🧪 Test with small queries first")
    print("   4. 📊 Monitor costs daily during development")
    print("   5. 🗑️  Clean up test resources regularly")
    
    print("\n🎯 Ready for deployment! All files validated.")
    print("💡 Tip: Save CLI commands to deploy.sh for easy execution")
    
    return True

def main():
    """Main execution function"""
    success = generate_deployment_report()
    
    if success:
        print("\n🎉 All prerequisites validated! Ready for AWS deployment.")
        
        # Generate deployment script
        script_content = """#!/bin/bash
# AWS Bedrock Deployment Script for MCP Bug Bounty Agent
# Generated automatically - review before execution

set -e  # Exit on any error

echo "🚀 Starting MCP Bug Bounty Agent deployment..."
echo "📅 $(date)"

# Check AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Install: pip install awscli"
    exit 1
fi

# Check AWS credentials
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Run: aws configure"
    exit 1
fi

echo "✅ AWS CLI and credentials validated"

# Set variables
ROLE_NAME="BedrockMCPAgentRole"
REGION="us-east-1"

echo "🔧 Creating IAM role..."
# Add your deployment commands here

echo "✅ Deployment complete! Test your agent in the AWS Console."
"""
        
        with open("deploy.sh", "w") as f:
            f.write(script_content)
        
        print("📝 Created deploy.sh script template")
        
    else:
        print("\n⚠️  Fix validation issues before deployment")

if __name__ == "__main__":
    main()