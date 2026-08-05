# -----------------------------------------------------------------------------
# Foundry Models Accelerator — Codebase audit script
#
# Source:  https://github.com/fatimataayeb/azure-openai-migration-guide
#          (originally `scripts/audit_codebase.py`)
# Author:  Fatima Taayeb (@fatimataayeb)
# License: MIT — see THIRD_PARTY_NOTICES.md at the repo root.
#
# This script targets the GPT-4o → GPT-5.1 transition specifically. The
# pattern-matching rules are useful as a first-pass scan for *any* migration
# off GPT-4o (the unsupported sampling parameters and the max_tokens rename
# apply to GPT-5.x and the o-series too). For per-target-model parameter
# differences, see docs/05-api-changes-by-model.md.
# -----------------------------------------------------------------------------

#!/usr/bin/env python3
"""
Azure OpenAI Migration Audit Script

Scans your codebase for GPT-4o parameters that need updating for GPT-5.1.

Usage:
    python audit_codebase.py --path /path/to/your/code
"""

import argparse
import os
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Finding:
    file_path: str
    line_number: int
    line_content: str
    issue_type: str
    severity: str
    recommendation: str

# Patterns to search for
PATTERNS = {
    "temperature": {
        "pattern": r'temperature\s*[=:]\s*[\d.]+',
        "severity": "HIGH",
        "recommendation": "Remove this parameter - not supported in GPT-5.1"
    },
    "top_p": {
        "pattern": r'top_p\s*[=:]\s*[\d.]+',
        "severity": "HIGH",
        "recommendation": "Remove this parameter - not supported in GPT-5.1"
    },
    "frequency_penalty": {
        "pattern": r'frequency_penalty\s*[=:]\s*[\d.]+',
        "severity": "HIGH",
        "recommendation": "Remove this parameter - not supported in GPT-5.1"
    },
    "presence_penalty": {
        "pattern": r'presence_penalty\s*[=:]\s*[\d.]+',
        "severity": "HIGH",
        "recommendation": "Remove this parameter - not supported in GPT-5.1"
    },
    "max_tokens": {
        "pattern": r'max_tokens\s*[=:]\s*\d+',
        "severity": "HIGH",
        "recommendation": "Rename to 'max_completion_tokens'"
    },
    "system_role": {
        "pattern": r'["\']role["\']\s*:\s*["\']system["\']',
        "severity": "MEDIUM",
        "recommendation": "Change to 'developer' role (system still works but deprecated)"
    },
    "gpt-4o_model": {
        "pattern": r'["\']gpt-4o["\']',
        "severity": "INFO",
        "recommendation": "Update to 'gpt-5.1' after code changes are complete"
    },
    "old_api_version": {
        "pattern": r'api_version\s*[=:]\s*["\']2024',
        "severity": "MEDIUM",
        "recommendation": "Update to api_version='2025-06-01'"
    },
    "logprobs": {
        "pattern": r'logprobs\s*[=:]\s*(True|true|\d+)',
        "severity": "HIGH",
        "recommendation": "Remove this parameter - not supported in GPT-5.1"
    }
}

# File extensions to scan
EXTENSIONS = {'.py', '.js', '.ts', '.jsx', '.tsx', '.cs', '.java', '.go', '.rb'}

def scan_file(file_path: Path) -> List[Finding]:
    """Scan a single file for migration issues."""
    findings = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
        return findings
    
    for line_num, line in enumerate(lines, 1):
        for issue_type, config in PATTERNS.items():
            if re.search(config["pattern"], line, re.IGNORECASE):
                findings.append(Finding(
                    file_path=str(file_path),
                    line_number=line_num,
                    line_content=line.strip()[:100],  # Truncate long lines
                    issue_type=issue_type,
                    severity=config["severity"],
                    recommendation=config["recommendation"]
                ))
    
    return findings

def scan_directory(root_path: str, exclude_dirs: List[str] = None) -> List[Finding]:
    """Recursively scan directory for migration issues."""
    if exclude_dirs is None:
        exclude_dirs = ['node_modules', '.git', '__pycache__', 'venv', '.venv', 'dist', 'build']
    
    all_findings = []
    root = Path(root_path)
    
    for file_path in root.rglob('*'):
        # Skip excluded directories
        if any(excluded in file_path.parts for excluded in exclude_dirs):
            continue
        
        # Only scan relevant file types
        if file_path.suffix.lower() in EXTENSIONS:
            findings = scan_file(file_path)
            all_findings.extend(findings)
    
    return all_findings

def generate_report(findings: List[Finding]) -> str:
    """Generate a formatted report of findings."""
    if not findings:
        return """
╔══════════════════════════════════════════════════════════════════╗
║  ✅ No migration issues found!                                   ║
║                                                                  ║
║  Your code appears ready for GPT-5.1.                           ║
║  Remember to update the model name when deploying.              ║
╚══════════════════════════════════════════════════════════════════╝
"""
    
    # Count by severity
    high = sum(1 for f in findings if f.severity == "HIGH")
    medium = sum(1 for f in findings if f.severity == "MEDIUM")
    info = sum(1 for f in findings if f.severity == "INFO")
    
    # Group by file
    by_file = {}
    for f in findings:
        by_file.setdefault(f.file_path, []).append(f)
    
    report = []
    report.append("=" * 70)
    report.append("AZURE OPENAI MIGRATION AUDIT REPORT")
    report.append("=" * 70)
    report.append("")
    report.append(f"Total findings: {len(findings)}")
    report.append(f"  🔴 HIGH:   {high} (will cause errors)")
    report.append(f"  🟡 MEDIUM: {medium} (should fix)")
    report.append(f"  🔵 INFO:   {info} (informational)")
    report.append("")
    report.append("-" * 70)
    report.append("FINDINGS BY FILE")
    report.append("-" * 70)
    
    for file_path, file_findings in sorted(by_file.items()):
        report.append("")
        report.append(f"📄 {file_path}")
        for f in sorted(file_findings, key=lambda x: x.line_number):
            severity_icon = {"HIGH": "🔴", "MEDIUM": "🟡", "INFO": "🔵"}[f.severity]
            report.append(f"   Line {f.line_number}: {severity_icon} {f.issue_type}")
            report.append(f"      Code: {f.line_content}")
            report.append(f"      Fix:  {f.recommendation}")
    
    report.append("")
    report.append("-" * 70)
    report.append("RECOMMENDED ACTIONS")
    report.append("-" * 70)
    report.append("")
    
    if high > 0:
        report.append("1. [REQUIRED] Fix all HIGH severity issues")
        report.append("   - Remove unsupported parameters (temperature, top_p, etc.)")
        report.append("   - Rename max_tokens to max_completion_tokens")
        report.append("")
    
    if medium > 0:
        report.append("2. [RECOMMENDED] Fix MEDIUM severity issues")
        report.append("   - Update API version to 2025-06-01")
        report.append("   - Change 'system' role to 'developer'")
        report.append("")
    
    report.append("3. [AFTER FIXES] Update model name from 'gpt-4o' to 'gpt-5.1'")
    report.append("")
    report.append("4. [TESTING] Run evaluation tests before deploying")
    report.append("   - See docs/evaluation-guide.md for setup instructions")
    report.append("")
    report.append("=" * 70)
    
    return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(
        description="Audit codebase for Azure OpenAI GPT-4o to GPT-5.1 migration"
    )
    parser.add_argument(
        "--path", "-p",
        required=True,
        help="Path to codebase to scan"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file for report (default: stdout)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )
    parser.add_argument(
        "--exclude", "-e",
        nargs="+",
        default=[],
        help="Additional directories to exclude"
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"Error: Path '{args.path}' does not exist")
        return 1
    
    print(f"Scanning {args.path}...")
    
    exclude_dirs = ['node_modules', '.git', '__pycache__', 'venv', '.venv', 'dist', 'build']
    exclude_dirs.extend(args.exclude)
    
    findings = scan_directory(args.path, exclude_dirs)
    
    if args.format == "json":
        import json
        output = json.dumps([f.__dict__ for f in findings], indent=2)
    else:
        output = generate_report(findings)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Report saved to {args.output}")
    else:
        print(output)
    
    # Exit with error code if HIGH severity issues found
    high_count = sum(1 for f in findings if f.severity == "HIGH")
    return 1 if high_count > 0 else 0

if __name__ == "__main__":
    exit(main())
