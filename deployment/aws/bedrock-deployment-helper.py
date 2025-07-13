#!/usr/bin/env python3
"""
AWS Bedrock Deployment Helper for MCP Bug Bounty Agent
Streamlined deployment with student-friendly guidance and cost optimization
"""

import json
import boto3
import os
from datetime import datetime
from pathlib import Path

class BedrockDeploymentHelper:
    def __init__(self):
        self.region = "us-east-1"  # Recommended for students
        self.agent_name = "MCP-BugBountyAgent"
        self.role_name = "BedrockMCPAgentRole"
        
    def check_aws_credentials(self):
        """Check if AWS credentials are configured"""
        try:
            session = boto3.Session()
            credentials = session.get_credentials()
            if credentials is None:
                return False, "No AWS credentials found"
            
            # Test credentials with a simple call
            sts = boto3.client('sts', region_name=self.region)
            identity = sts.get_caller_identity()
            account_id = identity.get('Account')
            
            return True, f"✅ AWS credentials valid for account: {account_id}"
        except Exception as e:
            return False, f"❌ AWS credential error: {str(e)}"
    
    def check_bedrock_access(self):
        """Check if Bedrock is enabled and model access is available"""
        try:
            bedrock = boto3.client('bedrock', region_name=self.region)
            
            # Check if we can list foundation models
            models = bedrock.list_foundation_models()
            claude_models = [m for m in models['modelSummaries'] 
                           if 'claude' in m['modelId'].lower()]
            
            if claude_models:
                return True, f"✅ Bedrock enabled, {len(claude_models)} Claude models available"
            else:
                return False, "❌ Claude models not available - request model access"
                
        except Exception as e:
            return False, f"❌ Bedrock access error: {str(e)}"
    
    def validate_iam_role(self):
        """Check if IAM role exists and has correct permissions"""
        try:
            iam = boto3.client('iam', region_name=self.region)
            
            # Check if role exists
            role = iam.get_role(RoleName=self.role_name)
            role_arn = role['Role']['Arn']
            
            # Check trust policy
            trust_policy = role['Role']['AssumeRolePolicyDocument']
            bedrock_trusted = any(
                stmt.get('Principal', {}).get('Service') == 'bedrock.amazonaws.com'
                for stmt in trust_policy.get('Statement', [])
            )
            
            if bedrock_trusted:
                return True, f"✅ IAM role exists: {role_arn}"
            else:
                return False, "❌ IAM role missing Bedrock trust relationship"
                
        except iam.exceptions.NoSuchEntityException:
            return False, f"❌ IAM role '{self.role_name}' not found"
        except Exception as e:
            return False, f"❌ IAM role validation error: {str(e)}"
    
    def create_agent_via_cli(self):
        """Generate AWS CLI commands for agent creation"""
        
        # Load bedrock agent config
        config_path = Path("bedrock-agent-config.json")
        if not config_path.exists():
            return False, "❌ bedrock-agent-config.json not found"
        
        with open(config_path) as f:
            config = json.load(f)
        
        # Generate CLI commands
        commands = []
        
        # 1. Create agent
        create_cmd = f"""aws bedrock-agent create-agent \\
    --agent-name "{config['agentName']}" \\
    --description "{config['description']}" \\
    --foundation-model "{config['foundationModel']}" \\
    --instruction '{config['instruction']}' \\
    --agent-role-arn "arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/{self.role_name}" \\
    --region {self.region}"""
        
        commands.append(("Create Agent", create_cmd))
        
        # 2. Prepare agent (creates working draft)
        prepare_cmd = f"""aws bedrock-agent prepare-agent \\
    --agent-id $(aws bedrock-agent list-agents --query 'agentSummaries[?agentName==`{config["agentName"]}`].agentId' --output text) \\
    --region {self.region}"""
        
        commands.append(("Prepare Agent", prepare_cmd))
        
        # 3. Create alias for testing
        alias_cmd = f"""aws bedrock-agent create-agent-alias \\
    --agent-id $(aws bedrock-agent list-agents --query 'agentSummaries[?agentName==`{config["agentName"]}`].agentId' --output text) \\
    --agent-alias-name "production" \\
    --description "Production alias for MCP Bug Bounty Agent" \\
    --region {self.region}"""
        
        commands.append(("Create Production Alias", alias_cmd))
        
        # 4. Test agent
        test_cmd = f"""aws bedrock-agent-runtime invoke-agent \\
    --agent-id $(aws bedrock-agent list-agents --query 'agentSummaries[?agentName==`{config["agentName"]}`].agentId' --output text) \\
    --agent-alias-id $(aws bedrock-agent list-agent-aliases --agent-id $(aws bedrock-agent list-agents --query 'agentSummaries[?agentName==`{config["agentName"]}`].agentId' --output text) --query 'agentAliasSummaries[0].agentAliasId' --output text) \\
    --session-id "test-session-$(date +%s)" \\
    --input-text "Research IDOR vulnerabilities in the NiceHash platform" \\
    --region {self.region}"""
        
        commands.append(("Test Agent", test_cmd))
        
        return True, commands
    
    def estimate_costs(self):
        """Estimate deployment and usage costs for students"""
        costs = {
            "deployment": {
                "iam_role": "$0.00 (free)",
                "bedrock_agent": "$0.00 (free to create)",
                "storage": "$0.00 (minimal S3 usage within free tier)"
            },
            "usage": {
                "claude_3_sonnet": "$0.003 per 1K input tokens, $0.015 per 1K output tokens",
                "typical_query": "~$0.01-0.05 per vulnerability analysis",
                "daily_testing": "~$2-5 (50-100 queries)",
                "aws_educate_credits": "Up to $100 offset"
            },
            "student_tips": [
                "Apply for AWS Educate for free credits",
                "Use AWS Free Tier for S3, CloudWatch",
                "Set up billing alerts at $10, $25, $50",
                "Test with smaller queries first",
                "Clean up test resources after validation"
            ]
        }
        
        return costs
    
    def generate_deployment_report(self):
        """Generate comprehensive deployment status report"""
        print("🚀 AWS Bedrock Deployment Helper - MCP Bug Bounty Agent")
        print("=" * 70)
        print(f"📅 Deployment Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌍 Target Region: {self.region}")
        print(f"🎯 Agent Name: {self.agent_name}")
        print(f"🔑 IAM Role: {self.role_name}")
        
        print("\n🔍 Pre-deployment Validation:")
        print("-" * 30)
        
        # Check AWS credentials
        cred_status, cred_msg = self.check_aws_credentials()
        print(f"   {cred_msg}")
        
        if not cred_status:
            print("\n❌ AWS credentials required. Configure with:")
            print("   aws configure")
            print("   or export AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
            return False
        
        # Check Bedrock access
        bedrock_status, bedrock_msg = self.check_bedrock_access()
        print(f"   {bedrock_msg}")
        
        if not bedrock_status:
            print("\n💡 Enable Bedrock access:")
            print("   1. Go to AWS Console → Amazon Bedrock")
            print("   2. Click 'Model access' → 'Request model access'")
            print("   3. Enable Anthropic Claude models")
        
        # Check IAM role
        iam_status, iam_msg = self.validate_iam_role()
        print(f"   {iam_msg}")
        
        if not iam_status:
            print("\n💡 Create IAM role:")
            print("   1. Go to AWS Console → IAM → Roles")
            print("   2. Create role with trust-policy.json")
            print("   3. Attach permission-policy.json")
        
        # Cost estimation
        print("\n💰 Cost Estimation (Student-Optimized):")
        print("-" * 40)
        costs = self.estimate_costs()
        
        print("   Deployment Costs:")
        for item, cost in costs["deployment"].items():
            print(f"     • {item}: {cost}")
        
        print("\n   Usage Costs:")
        for item, cost in costs["usage"].items():
            if item != "student_tips":
                print(f"     • {item}: {cost}")
        
        print("\n   💡 Student Cost Tips:")
        for tip in costs["usage"]["student_tips"]:
            print(f"     • {tip}")
        
        # Generate CLI commands if ready
        if cred_status and iam_status:
            print("\n🛠️ AWS CLI Deployment Commands:")
            print("-" * 35)
            
            cmd_status, commands = self.create_agent_via_cli()
            if cmd_status:
                for i, (name, cmd) in enumerate(commands, 1):
                    print(f"\n   {i}. {name}:")
                    print(f"   {cmd}")
            else:
                print(f"   ❌ {commands}")
        
        print("\n✅ Next Steps:")
        print("   1. Complete any missing prerequisites above")
        print("   2. Run the CLI commands in sequence")
        print("   3. Test agent with NiceHash vulnerability query")
        print("   4. Validate $7K-$16K bounty estimation outputs")
        print("   5. Set up monitoring and cost alerts")
        
        print(f"\n🎯 Deployment Status: {'Ready for CLI execution' if (cred_status and iam_status) else 'Prerequisites needed'}")
        
        return cred_status and iam_status

def main():
    """Main execution function"""
    helper = BedrockDeploymentHelper()
    ready = helper.generate_deployment_report()
    
    if ready:
        print("\n🎉 All prerequisites met! Ready for agent deployment.")
        print("💡 Tip: Save the CLI commands to a script file for easy execution.")
    else:
        print("\n⚠️  Complete prerequisites before deployment.")
        print("💡 Tip: Use AWS Educate tutorials for step-by-step guidance.")

if __name__ == "__main__":
    main()