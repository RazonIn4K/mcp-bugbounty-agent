# AWS Bedrock Agent Deployment Guide

## 🔄 **CORRECTED APPROACH: Bedrock Agents vs Marketplace**

Based on AWS documentation, the path is:
1. **Deploy via Bedrock Agents** (immediate, real-time)
2. **Monetize directly** via Stripe + API Gateway
3. **Optional**: List on AWS Marketplace as ML product (longer process)

## 🚀 **Phase 1: AWS Bedrock Setup (30-45 minutes)**

### **Step 1: AWS Console Access**
```bash
# Log into AWS Management Console
https://console.aws.amazon.com

# Navigate to Amazon Bedrock
Services → Machine Learning → Amazon Bedrock
```

### **Step 2: Enable Bedrock Access**
- **Region**: Choose us-east-1 or us-west-2 (best availability)
- **Model Access**: Request access to Anthropic Claude models
- **Quotas**: Default 5 agents per account (request increase if needed)

### **Step 3: Create IAM Service Role**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "bedrock.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

**Required Permissions:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "lambda:InvokeFunction",
        "s3:GetObject",
        "s3:PutObject",
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "*"
    }
  ]
}
```

## 🤖 **Phase 2: Agent Deployment (45-90 minutes)**

### **Step 1: Create Bedrock Agent**
```bash
# In Bedrock Console
1. Click "Create Agent"
2. Agent Name: "MCP-BugBountyAgent"
3. Description: "AI-powered vulnerability research with Docker isolation"
4. Foundation Model: "Anthropic Claude 3 Sonnet"
5. IAM Role: Select the role created above
```

### **Step 2: Configure Agent Instructions**
```
You are an AI-powered bug bounty research agent specializing in vulnerability discovery and analysis. 

Your capabilities include:
- IDOR vulnerability detection with 85% accuracy
- Authentication bypass analysis
- Business logic flaw identification  
- Automated Burp Suite payload generation
- Professional vulnerability reporting

Always prioritize:
1. Authorized testing only
2. Responsible disclosure
3. Rate limiting respect
4. Professional documentation

Provide structured output with:
- Vulnerability assessment
- PoC templates
- Confidence scoring
- Burp Suite configurations
- Business impact analysis
```

### **Step 3: Upload Action Groups**
Create Lambda function for MCP orchestration:

```python
import json
import boto3
import requests

def lambda_handler(event, context):
    """
    Lambda function for MCP Bug Bounty Agent
    Handles vulnerability research orchestration
    """
    
    # Extract parameters from Bedrock
    parameters = event.get('parameters', {})
    target = parameters.get('target', '')
    vuln_types = parameters.get('vulnerability_types', ['idor'])
    
    # Initialize MCP agent logic
    try:
        # Import our agent (deployed as Lambda layer)
        from mcp_bugbounty_agent import BugBountyResearchAgent
        
        agent = BugBountyResearchAgent(premium=True)
        
        # Run research
        import asyncio
        results = asyncio.run(agent.orchestrate_research(target, vuln_types))
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'vulnerabilities_found': results.get('vulnerability_count', 0),
                'estimated_bounty': results.get('estimated_bounty_range', {}),
                'session_id': results.get('session_id', ''),
                'detailed_results': results
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'message': 'Vulnerability research failed'
            })
        }
```

### **Step 4: Configure API Schema**
```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "MCP Bug Bounty Agent API",
    "version": "1.2.0"
  },
  "paths": {
    "/research": {
      "post": {
        "summary": "Conduct vulnerability research",
        "parameters": [
          {
            "name": "target",
            "in": "query",
            "required": true,
            "schema": {"type": "string"},
            "description": "Target domain or platform"
          },
          {
            "name": "vulnerability_types",
            "in": "query",
            "required": false,
            "schema": {
              "type": "array",
              "items": {"type": "string"}
            },
            "description": "Types of vulnerabilities to research"
          }
        ],
        "responses": {
          "200": {
            "description": "Research completed",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "vulnerabilities_found": {"type": "integer"},
                    "estimated_bounty": {"type": "object"},
                    "session_id": {"type": "string"}
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## 💰 **Phase 3: Direct Monetization Setup (30-45 minutes)**

### **Step 1: API Gateway Setup**
```bash
# Create API Gateway
1. Services → API Gateway
2. Create REST API
3. Resource: /research
4. Method: POST
5. Integration: Lambda (our function)
6. Enable CORS
7. Deploy to stage: "prod"
```

### **Step 2: Authentication Layer**
```python
# Lambda authorizer for API key validation
def authorizer_handler(event, context):
    token = event['authorizationToken']
    
    # Validate with Stripe
    import stripe
    stripe.api_key = "sk_live_your_key"
    
    try:
        # Check if API key corresponds to active subscription
        customer = stripe.Customer.list(email=extract_email_from_token(token))
        if customer.data and customer.data[0].subscriptions.data:
            subscription = customer.data[0].subscriptions.data[0]
            if subscription.status == 'active':
                return generate_policy('user', 'Allow', event['methodArn'])
    except:
        pass
    
    return generate_policy('user', 'Deny', event['methodArn'])
```

### **Step 3: Stripe Integration**
```javascript
// Frontend subscription handling
const stripe = Stripe('pk_live_your_key');

async function subscribeToPremium() {
    const {sessionId} = await fetch('/create-checkout-session', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            priceId: 'price_premium_monthly',
            quantity: 1
        })
    }).then(res => res.json());
    
    return stripe.redirectToCheckout({sessionId});
}
```

## 🧪 **Phase 4: Testing & Validation (45-60 minutes)**

### **Step 1: Test Bedrock Agent**
```bash
# AWS CLI testing
aws bedrock-agent-runtime invoke-agent \
    --agent-id "your-agent-id" \
    --agent-alias-id "TSTALIASID" \
    --session-id "test-session" \
    --input-text "Research IDOR vulnerabilities in NiceHash platform"
```

### **Step 2: API Gateway Testing**
```bash
# Test API endpoint
curl -X POST "https://your-api-id.execute-api.region.amazonaws.com/prod/research" \
  -H "Authorization: Bearer premium-api-key" \
  -H "Content-Type: application/json" \
  -d '{"target": "NiceHash", "vulnerability_types": ["idor", "auth_bypass"]}'
```

### **Step 3: NiceHash Validation**
```python
# Real-world testing script
import requests

def test_nicehash_integration():
    # Register test account
    # Fund with testnet BTC
    # Run agent against test.nicehash.com
    # Validate results
    
    api_endpoint = "https://your-api-gateway/prod/research"
    headers = {"Authorization": "Bearer test-key"}
    payload = {
        "target": "test.nicehash.com",
        "vulnerability_types": ["idor", "auth_bypass", "business_logic"]
    }
    
    response = requests.post(api_endpoint, json=payload, headers=headers)
    results = response.json()
    
    print(f"Vulnerabilities found: {results['vulnerabilities_found']}")
    print(f"Estimated bounty: {results['estimated_bounty']}")
    
    return results

# Run validation
results = test_nicehash_integration()
```

## 📊 **Revenue Model (Direct vs Marketplace)**

### **Direct Monetization (Immediate)**
```
Revenue Streams:
1. API calls: $0.10 per research request
2. Premium subscriptions: $29/month unlimited
3. Enterprise licenses: $200/hour consulting

Estimated Monthly Revenue:
- 1000 API calls × $0.10 = $100
- 150 premium subs × $29 = $4,350  
- 20 consulting hours × $200 = $4,000
Total: $8,450/month = $101K annual
```

### **AWS Marketplace (Optional)**
```
If qualifying as ML product:
- AWS takes 30% commission
- Net revenue: $70K annual
- Benefit: Enterprise discovery
- Timeline: 2-4 weeks approval
```

## 🎯 **Launch Checklist (Next 4 Hours)**

### **Immediate Actions (High Energy)**
- [ ] AWS Bedrock console setup (30 min)
- [ ] IAM role creation and permissions (15 min)  
- [ ] Agent deployment with Claude model (45 min)
- [ ] Lambda function upload and testing (60 min)
- [ ] API Gateway configuration (30 min)

### **Same Day Actions (Medium Energy)**
- [ ] GitHub repository creation (30 min)
- [ ] Stripe integration setup (45 min)
- [ ] NiceHash test account registration (15 min)
- [ ] End-to-end API testing (30 min)

### **Next Day Actions (Low Energy)**
- [ ] Marketing content creation
- [ ] Community promotion (Discord, LinkedIn)
- [ ] AWS Marketplace exploration (if desired)
- [ ] Customer feedback collection

## 🔗 **Key Resources**

### **AWS Documentation**
- [Bedrock Agents Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)
- [IAM Roles for Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-permissions.html)
- [API Gateway Integration](https://docs.aws.amazon.com/apigateway/latest/developerguide/)

### **Monetization**
- [Stripe API Documentation](https://stripe.com/docs/api)
- [AWS Marketplace ML Products](https://docs.aws.amazon.com/marketplace/latest/userguide/ml-listing-process.html)

### **Testing**
- [NiceHash Test Environment](https://test.nicehash.com)
- [Testnet BTC Faucets](https://testnet-faucet.com/btc-testnet/)

---

**This corrected approach focuses on immediate deployment capability with direct monetization, avoiding the marketplace complexity while maintaining the $100K+ revenue potential.**