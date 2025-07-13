#!/usr/bin/env python3
"""
MCP Bug Bounty Agent - Demo Script
Live demonstration of AI-powered vulnerability research capabilities

Usage:
    python demo_script.py [--premium] [--docker] [--target TARGET]

Examples:
    python demo_script.py                           # Free tier demo
    python demo_script.py --premium                 # Premium tier demo
    python demo_script.py --premium --docker        # Full Docker isolation demo
    python demo_script.py --target "ExampleCorp"    # Custom target demo
"""

import asyncio
import json
import time
import argparse
from pathlib import Path
import sys

# Add the agent to the path for import
sys.path.append(str(Path(__file__).parent))

# Import the agent classes from the main file
try:
    from MCP_BugBountyAgent import BugBountyResearchAgent
except ImportError:
    # If running from the same directory, import directly
    import importlib.util
    spec = importlib.util.spec_from_file_location("MCP_BugBountyAgent", 
                                                  Path(__file__).parent / "MCP-BugBountyAgent.py")
    mcp_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mcp_module)
    BugBountyResearchAgent = mcp_module.BugBountyResearchAgent

def print_banner():
    """Print demo banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║         🕵️  MCP Bug Bounty Research Agent Demo              ║
    ║                                                              ║
    ║    AI-Powered Vulnerability Research with Docker Isolation   ║
    ║                                                              ║
    ║    💰 Market Opportunity: $86K+ Annual Revenue Potential    ║
    ║    🚀 AWS AI Agent Marketplace Ready (July 15, 2025)       ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)
    print(f"Demo started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

def print_section(title: str, description: str = ""):
    """Print section header"""
    print(f"\n{'='*70}")
    print(f"🎯 {title}")
    if description:
        print(f"   {description}")
    print("=" * 70)

def print_results_summary(results: dict):
    """Print formatted results summary"""
    print(f"\n📊 RESULTS SUMMARY")
    print(f"   Session ID: {results.get('session_id', 'N/A')}")
    print(f"   Target: {results.get('target', 'N/A')}")
    print(f"   Vulnerabilities Found: {results.get('vulnerability_count', 0)}")
    
    bounty_range = results.get('estimated_bounty_range', {})
    print(f"   Estimated Bounty: {bounty_range.get('min', '$0')} - {bounty_range.get('max', '$0')}")
    print(f"   Confidence: {bounty_range.get('confidence', 'unknown')}")
    
    if 'analysis_data' in results:
        analysis = results['analysis_data']
        print(f"   Attack Vectors: {len(analysis.get('attack_vectors', []))}")
        print(f"   Tools Recommended: {len(analysis.get('tools_recommended', []))}")

def demonstrate_free_tier():
    """Demonstrate free tier capabilities"""
    print_section("FREE TIER DEMONSTRATION", "3 searches per session, basic features")
    
    print("🆓 Initializing Free Tier Agent...")
    agent = BugBountyResearchAgent(premium=False, use_docker=False)
    
    print("   ✅ Agent initialized (free tier)")
    print("   📝 Features: Basic IDOR research, community support")
    print("   🚫 Limitations: 3 searches/session, no Docker isolation")
    
    return agent

async def demonstrate_premium_tier():
    """Demonstrate premium tier capabilities"""
    print_section("PREMIUM TIER DEMONSTRATION", "$29/month - Unlimited + Docker isolation")
    
    print("💎 Initializing Premium Tier Agent...")
    agent = BugBountyResearchAgent(
        api_key="demo-premium-key",
        premium=True,
        use_docker=False  # Set to True for actual Docker demo
    )
    
    print("   ✅ Agent initialized (premium tier)")
    print("   📝 Features: Unlimited searches, advanced PoCs, priority support")
    print("   🐳 Docker: Available (disabled for demo speed)")
    
    return agent

async def run_vulnerability_research(agent: BugBountyResearchAgent, target: str, vuln_types: list):
    """Run vulnerability research demonstration"""
    print(f"\n🔍 Starting Research: {target}")
    print(f"   Vulnerability Types: {', '.join(vuln_types)}")
    print(f"   Research Method: Hub & Spoke Architecture (L1→L2→L3)")
    
    start_time = time.time()
    
    try:
        results = await agent.orchestrate_research(target, vuln_types)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n⏱️  Research completed in {duration:.2f} seconds")
        print_results_summary(results)
        
        # Show some vulnerability details
        if 'analysis_data' in results and 'vulnerabilities' in results['analysis_data']:
            vulnerabilities = results['analysis_data']['vulnerabilities']
            if vulnerabilities:
                print(f"\n🔍 VULNERABILITY DETAILS:")
                for i, vuln in enumerate(vulnerabilities[:3], 1):  # Show first 3
                    print(f"   {i}. {vuln.title} ({vuln.severity})")
                    print(f"      Confidence: {vuln.confidence:.0%}")
                    print(f"      Description: {vuln.description[:100]}...")
        
        return results
        
    except Exception as e:
        print(f"❌ Research failed: {e}")
        return None

def demonstrate_burp_integration(results: dict):
    """Demonstrate Burp Suite payload generation"""
    if not results or 'analysis_data' not in results:
        return
    
    print_section("BURP SUITE INTEGRATION", "Automated payload generation")
    
    analysis = results['analysis_data']
    vulnerabilities = analysis.get('vulnerabilities', [])
    
    if vulnerabilities:
        vuln = vulnerabilities[0]  # Use first vulnerability
        print(f"📋 Generated Burp Payloads for: {vuln.title}")
        
        # Extract Burp payload from PoC template if available
        poc = vuln.poc_template
        if "Burp Suite Payload:" in poc:
            payload_section = poc.split("Burp Suite Payload:")[1].strip()
            print(f"\n🎯 Intruder Configuration:")
            print("   " + "\n   ".join(payload_section.split('\n')[:10]))  # First 10 lines
        else:
            print("   📝 Basic Burp configuration available")
            print(f"   🎯 Target endpoint: {vuln.description}")
    else:
        print("   ℹ️  No vulnerabilities found for payload generation")

def demonstrate_docker_features(results: dict):
    """Demonstrate Docker isolation features"""
    print_section("DOCKER ISOLATION FEATURES", "Safe testing in isolated containers")
    
    if 'docker_testing' in results:
        docker_results = results['docker_testing']
        print(f"🐳 Docker Testing Summary:")
        print(f"   Containers Created: {docker_results.get('containers_created', 0)}")
        print(f"   Tests Executed: {docker_results.get('tests_executed', 0)}")
        print(f"   Vulnerabilities Confirmed: {len(docker_results.get('vulnerabilities_confirmed', []))}")
        
        envs = docker_results.get('testing_environments', [])
        if envs:
            env = envs[0]
            print(f"   Environment: {env.get('type', 'Unknown')}")
            print(f"   Tools: {', '.join(env.get('tools', []))}")
            print(f"   Isolation: {env.get('isolation_level', 'Unknown')}")
    else:
        print("🐳 Docker Features (Premium):")
        print("   ✅ Kali Linux containers")
        print("   ✅ Pre-installed security tools (nmap, sqlmap, gobuster)")
        print("   ✅ Complete isolation from host system")
        print("   ✅ Automatic cleanup after testing")
        print("   ⚠️  Docker not enabled in this demo for speed")

def save_demo_results(results: dict, filename: str = None):
    """Save demo results to file"""
    if not filename:
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        filename = f"demo_results_{timestamp}.json"
    
    filepath = Path(filename)
    
    try:
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n💾 Demo results saved to: {filepath}")
        print(f"   File size: {filepath.stat().st_size} bytes")
        print(f"   Integration: Ready for CS-Brain import")
        
    except Exception as e:
        print(f"❌ Failed to save results: {e}")

def print_monetization_summary():
    """Print monetization and business summary"""
    print_section("MONETIZATION & BUSINESS MODEL", "Revenue potential and market opportunity")
    
    print("💰 REVENUE PROJECTIONS:")
    print("   Free Tier: 0 revenue (conversion funnel)")
    print("   Premium Tier: $29/month × 150 subscribers = $52K annual")
    print("   Enterprise Tier: $200/hour × 20 hours/month = $48K annual")
    print("   Total Year 1 Potential: $100K+ annual revenue")
    
    print("\n🎯 MARKET OPPORTUNITY:")
    print("   Global AI funding: $110-131B (2024)")
    print("   GenAI ROI: 3.7x returns per dollar invested")
    print("   Bug bounty market growth: 20-30% annually")
    print("   AWS AI Agent marketplace launch: July 15, 2025")
    
    print("\n🏆 COMPETITIVE ADVANTAGES:")
    print("   ✅ MCP tool integration (no setup complexity)")
    print("   ✅ Docker isolation (safe testing)")
    print("   ✅ AI-powered analysis (pattern recognition)")
    print("   ✅ Freemium model (low barrier to entry)")
    print("   ✅ Marketplace distribution (AWS, GitHub)")

async def main():
    """Main demo function"""
    parser = argparse.ArgumentParser(description="MCP Bug Bounty Agent Demo")
    parser.add_argument("--premium", action="store_true", help="Run premium tier demo")
    parser.add_argument("--docker", action="store_true", help="Enable Docker isolation")
    parser.add_argument("--target", default="NiceHash", help="Target for research")
    parser.add_argument("--save", action="store_true", help="Save results to file")
    args = parser.parse_args()
    
    print_banner()
    
    # Demo configuration
    target = args.target
    vuln_types = ["idor", "auth_bypass", "business_logic"]
    
    try:
        if args.premium:
            # Premium tier demonstration
            agent = await demonstrate_premium_tier()
            
            # Run research with premium features
            with agent:
                results = await run_vulnerability_research(agent, target, vuln_types)
                
                if results:
                    demonstrate_burp_integration(results)
                    demonstrate_docker_features(results)
                    
                    if args.save:
                        save_demo_results(results)
        else:
            # Free tier demonstration
            agent = demonstrate_free_tier()
            
            # Run basic research
            results = await run_vulnerability_research(agent, target, ["idor"])
            
            if results and args.save:
                save_demo_results(results)
            
            # Show upgrade prompt
            print("\n🔒 UPGRADE TO PREMIUM:")
            print("   ✅ Unlimited searches per session")
            print("   ✅ Docker isolation for safe testing")
            print("   ✅ Advanced Burp Suite integration")
            print("   ✅ Priority email support")
            print("   💳 Subscribe: https://bugbounty-agent.com/premium")
        
        # Always show business model
        print_monetization_summary()
        
        print_section("DEMO COMPLETE", "Thank you for trying MCP Bug Bounty Agent!")
        print("🔗 Links:")
        print("   GitHub: https://github.com/your-org/mcp-bugbounty-agent")
        print("   Documentation: https://docs.bugbounty-agent.com")
        print("   Premium: https://bugbounty-agent.com/premium")
        print("   Enterprise: https://calendly.com/bugbounty-agent")
        print("   Discord: https://discord.gg/bugbounty-agent")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("For support, contact: hello@bugbounty-agent.com")

if __name__ == "__main__":
    asyncio.run(main())