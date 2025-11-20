#!/bin/bash

# Demo script for mcp-agent - Model Context Protocol agent

set -e

echo "=========================================="
echo "  🤖 MCP Agent - AI Integration Platform"
echo "  Model Context Protocol Implementation"
echo "=========================================="
echo ""

echo "🔍 Architecture:"
if [ -d "mcp-github-server" ] && [ -d "mcp-jira-server" ]; then
    echo "   ✅ Multi-server MCP architecture detected"
    echo "   • GitHub MCP Server"
    echo "   • Jira MCP Server"
    echo "   • Central agent orchestrator"
else
    echo "   ⚠️  MCP servers not found"
fi

echo ""
echo "✨ MCP Agent Capabilities:"
echo ""
echo "   🔗 GitHub Integration"
echo "      • Repository management"
echo "      • Issue/PR automation"
echo "      • Code review workflows"
echo "      • Actions integration"
echo ""
echo "   📋 Jira Integration"
echo "      • Ticket synchronization"
echo "      • Status updates"
echo "      • Sprint management"
echo "      • Workflow automation"
echo ""
echo "   🤖 AI Orchestration"
echo "      • Multi-tool coordination"
echo "      • Context-aware actions"
echo "      • Intelligent routing"
echo "      • Error recovery"
echo ""

echo "🧪 Testing..."
if [ -d "tests" ]; then
    echo "   ✅ Test suite available"
    if command -v pytest &> /dev/null; then
        echo "   Run: pytest tests/"
    else
        echo "   ℹ️  Install pytest: pip install pytest"
    fi
else
    echo "   ℹ️  Tests directory not found"
fi

echo ""
echo "📝 Configuration:"
if [ -f ".env.example" ]; then
    echo "   ✅ Environment template found"
    echo ""
    echo "   Required variables:"
    echo "   • GITHUB_TOKEN - GitHub API access"
    echo "   • JIRA_URL - Jira instance URL"
    echo "   • JIRA_EMAIL - Jira account email"
    echo "   • JIRA_API_TOKEN - Jira API token"
fi

echo ""
echo "🚀 Quick Start:"
echo ""
echo "   1. Configure environment:"
echo "      cp .env.example .env"
echo "      # Edit .env with your credentials"
echo ""
echo "   2. Start MCP servers:"
echo "      docker-compose up -d"
echo ""
echo "   3. Run agent:"
echo "      python agent/main.py"
echo ""

echo "💡 Use Cases:"
echo ""
echo "   📊 Automated Workflows"
echo "      • Sync Jira tickets to GitHub issues"
echo "      • Create PRs from Jira tasks"
echo "      • Update ticket status on PR merge"
echo ""
echo "   🔄 Bidirectional Sync"
echo "      • Comments between platforms"
echo "      • Status propagation"
echo "      • Assignee mapping"
echo ""
echo "   📈 Analytics"
echo "      • Cross-platform metrics"
echo "      • Workflow efficiency tracking"
echo "      • Team productivity insights"
echo ""

echo "=========================================="
echo "  Repository: github.com/wesleyscholl/mcp-agent"
echo "  Type: MCP Implementation | Multi-server"
echo "=========================================="
echo ""
