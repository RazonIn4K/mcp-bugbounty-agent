#!/bin/bash
# AWS Bedrock Deployment Script for MCP Bug Bounty Agent
# Auto-generated with student cost optimization
# Target: July 15, 2025 Launch Ready

set -e  # Exit on any error

echo "🚀 Starting MCP Bug Bounty Agent deployment..."
echo "📅 $(date)"
echo "🎯 Target: AWS Bedrock with Claude 3 Sonnet"
echo "💰 Student-optimized with AWS Educate integration"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ROLE_NAME="BedrockMCPAgentRole"
REGION="us-east-1"
AGENT_NAME="MCP-BugBountyAgent"

echo -e "\n${BLUE}🔍 Pre-deployment Validation${NC}"
echo "================================"

# Check AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI not found${NC}"
    echo "Install with: pip install awscli"
    echo "Or download from: https://aws.amazon.com/cli/"
    exit 1
fi
echo -e "${GREEN}✅ AWS CLI found${NC}"

# Check AWS credentials
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}❌ AWS credentials not configured${NC}"
    echo "Configure with: aws configure"
    echo "Or set environment variables:"
    echo "  export AWS_ACCESS_KEY_ID=your_key"
    echo "  export AWS_SECRET_ACCESS_KEY=your_secret"
    exit 1
fi

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo -e "${GREEN}✅ AWS credentials validated for account: $ACCOUNT_ID${NC}"

# Check required files
required_files=("trust-policy.json" "permission-policy.json" "bedrock-agent-config.json")
for file in "${required_files[@]}"; do
    if [[ ! -f "$file" ]]; then
        echo -e "${RED}❌ Required file missing: $file${NC}"
        echo "Generate with: python aws-iam-setup.py"
        exit 1
    fi
done
echo -e "${GREEN}✅ All required files present${NC}"

# Check if region supports Bedrock
echo -e "\n${BLUE}🌍 Checking Bedrock availability in $REGION${NC}"
if aws bedrock list-foundation-models --region $REGION &> /dev/null; then
    echo -e "${GREEN}✅ Bedrock available in $REGION${NC}"
else
    echo -e "${YELLOW}⚠️  Bedrock may not be available in $REGION${NC}"
    echo "Consider switching to us-east-1 or us-west-2"
fi

echo -e "\n${BLUE}💰 Cost Estimate${NC}"
echo "=================="
echo "Deployment: FREE"
echo "Usage: ~$0.01-$0.05 per vulnerability analysis"
echo "Daily testing (50 queries): ~$0.50-$2.50"
echo "AWS Educate: Up to $100 free credits available"

read -p "Continue with deployment? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled"
    exit 0
fi

echo -e "\n${BLUE}🔧 Step 1: Creating IAM Role${NC}"
echo "=============================="

# Check if role already exists
if aws iam get-role --role-name $ROLE_NAME &> /dev/null; then
    echo -e "${YELLOW}⚠️  IAM role $ROLE_NAME already exists${NC}"
    ROLE_ARN=$(aws iam get-role --role-name $ROLE_NAME --query 'Role.Arn' --output text)
    echo "Using existing role: $ROLE_ARN"
else
    echo "Creating IAM role: $ROLE_NAME"
    aws iam create-role \
        --role-name $ROLE_NAME \
        --assume-role-policy-document file://trust-policy.json \
        --description "IAM role for MCP Bug Bounty Agent on Amazon Bedrock" \
        --region $REGION
    
    ROLE_ARN=$(aws iam get-role --role-name $ROLE_NAME --query 'Role.Arn' --output text)
    echo -e "${GREEN}✅ IAM role created: $ROLE_ARN${NC}"
fi

echo -e "\n${BLUE}📋 Step 2: Attaching IAM Policy${NC}"
echo "================================="

# Attach permissions policy
echo "Attaching permissions policy..."
aws iam put-role-policy \
    --role-name $ROLE_NAME \
    --policy-name MCPBugBountyAgentPolicy \
    --policy-document file://permission-policy.json

echo -e "${GREEN}✅ IAM policy attached${NC}"

# Verify policy attachment
POLICIES=$(aws iam list-role-policies --role-name $ROLE_NAME --query 'PolicyNames' --output text)
echo "Attached policies: $POLICIES"

echo -e "\n${BLUE}🤖 Step 3: Creating Bedrock Agent${NC}"
echo "=================================="

# Check if agent already exists
EXISTING_AGENT=$(aws bedrock-agent list-agents --query "agentSummaries[?agentName=='$AGENT_NAME'].agentId" --output text --region $REGION 2>/dev/null || echo "")

if [[ -n "$EXISTING_AGENT" ]]; then
    echo -e "${YELLOW}⚠️  Agent $AGENT_NAME already exists with ID: $EXISTING_AGENT${NC}"
    AGENT_ID=$EXISTING_AGENT
else
    echo "Creating Bedrock agent: $AGENT_NAME"
    
    # Load agent configuration
    AGENT_DESC=$(jq -r '.description' bedrock-agent-config.json)
    FOUNDATION_MODEL=$(jq -r '.foundationModel' bedrock-agent-config.json)
    AGENT_INSTRUCTION=$(jq -r '.instruction' bedrock-agent-config.json)
    
    AGENT_ID=$(aws bedrock-agent create-agent \
        --agent-name "$AGENT_NAME" \
        --description "$AGENT_DESC" \
        --foundation-model "$FOUNDATION_MODEL" \
        --instruction "$AGENT_INSTRUCTION" \
        --agent-role-arn "$ROLE_ARN" \
        --region $REGION \
        --query 'agent.agentId' \
        --output text)
    
    echo -e "${GREEN}✅ Bedrock agent created with ID: $AGENT_ID${NC}"
fi

echo -e "\n${BLUE}⚙️ Step 4: Preparing Agent${NC}"
echo "=========================="

echo "Creating working draft for agent..."
aws bedrock-agent prepare-agent \
    --agent-id $AGENT_ID \
    --region $REGION

echo -e "${GREEN}✅ Agent prepared (working draft created)${NC}"

echo -e "\n${BLUE}🏷️ Step 5: Creating Production Alias${NC}"
echo "====================================="

# Check if alias already exists
EXISTING_ALIAS=$(aws bedrock-agent list-agent-aliases --agent-id $AGENT_ID --region $REGION --query "agentAliasSummaries[?agentAliasName=='production'].agentAliasId" --output text 2>/dev/null || echo "")

if [[ -n "$EXISTING_ALIAS" ]]; then
    echo -e "${YELLOW}⚠️  Production alias already exists with ID: $EXISTING_ALIAS${NC}"
    ALIAS_ID=$EXISTING_ALIAS
else
    echo "Creating production alias..."
    ALIAS_ID=$(aws bedrock-agent create-agent-alias \
        --agent-id $AGENT_ID \
        --agent-alias-name "production" \
        --description "Production alias for MCP Bug Bounty Agent" \
        --region $REGION \
        --query 'agentAlias.agentAliasId' \
        --output text)
    
    echo -e "${GREEN}✅ Production alias created with ID: $ALIAS_ID${NC}"
fi

echo -e "\n${BLUE}🧪 Step 6: Testing Agent${NC}"
echo "======================="

echo "Testing agent with NiceHash IDOR analysis query..."
echo "Query: 'Research IDOR vulnerabilities in the NiceHash platform with Burp Suite payload generation'"

TEST_SESSION="test-session-$(date +%s)"
TEST_OUTPUT_FILE="agent-test-output-$(date +%Y%m%d-%H%M%S).json"

aws bedrock-agent-runtime invoke-agent \
    --agent-id $AGENT_ID \
    --agent-alias-id $ALIAS_ID \
    --session-id $TEST_SESSION \
    --input-text "Research IDOR vulnerabilities in the NiceHash platform with Burp Suite payload generation. Focus on sequential ID enumeration and provide detailed PoC templates." \
    --region $REGION \
    --output json > $TEST_OUTPUT_FILE

if [[ $? -eq 0 ]]; then
    echo -e "${GREEN}✅ Agent test successful!${NC}"
    echo "Test output saved to: $TEST_OUTPUT_FILE"
    
    # Extract key information from test output
    if command -v jq &> /dev/null; then
        echo -e "\n${BLUE}📊 Test Results Preview:${NC}"
        echo "Response length: $(jq -r '.completion | length' $TEST_OUTPUT_FILE 2>/dev/null || echo "N/A") characters"
        echo "Session ID: $TEST_SESSION"
        echo "Agent ID: $AGENT_ID"
        echo "Alias ID: $ALIAS_ID"
    fi
else
    echo -e "${RED}❌ Agent test failed${NC}"
    echo "Check CloudWatch logs for details"
fi

echo -e "\n${GREEN}🎉 Deployment Complete!${NC}"
echo "========================"
echo "Agent Name: $AGENT_NAME"
echo "Agent ID: $AGENT_ID"
echo "Production Alias ID: $ALIAS_ID"
echo "Region: $REGION"
echo "Role ARN: $ROLE_ARN"

echo -e "\n${BLUE}📝 Next Steps:${NC}"
echo "1. 🧪 Review test output in $TEST_OUTPUT_FILE"
echo "2. 💰 Monitor costs in AWS Billing Dashboard"
echo "3. 📊 Check CloudWatch logs for detailed agent behavior"
echo "4. 🔄 Iterate on agent instructions based on test results"
echo "5. 🎯 Register NiceHash test account for validation"

echo -e "\n${BLUE}💡 Management URLs:${NC}"
echo "Bedrock Console: https://console.aws.amazon.com/bedrock/home?region=$REGION#/agents/$AGENT_ID"
echo "IAM Role: https://console.aws.amazon.com/iam/home#/roles/$ROLE_NAME"
echo "CloudWatch Logs: https://console.aws.amazon.com/cloudwatch/home?region=$REGION#logsV2:log-groups"

echo -e "\n${GREEN}✅ MCP Bug Bounty Agent is now live on AWS Bedrock!${NC}"
echo "🚀 Ready for July 15, 2025 launch!"

# Save deployment information
DEPLOYMENT_INFO="deployment-info-$(date +%Y%m%d-%H%M%S).json"
cat > $DEPLOYMENT_INFO << EOF
{
  "deployment_date": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "agent_name": "$AGENT_NAME",
  "agent_id": "$AGENT_ID",
  "alias_id": "$ALIAS_ID",
  "region": "$REGION",
  "role_arn": "$ROLE_ARN",
  "account_id": "$ACCOUNT_ID",
  "test_session": "$TEST_SESSION",
  "test_output_file": "$TEST_OUTPUT_FILE",
  "status": "deployed",
  "console_url": "https://console.aws.amazon.com/bedrock/home?region=$REGION#/agents/$AGENT_ID"
}
EOF

echo "📄 Deployment info saved to: $DEPLOYMENT_INFO"
echo "🎯 Total deployment time: $(date)"