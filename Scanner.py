import datetime
import os
import re
import time
import subprocess
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import (
    RED, GREEN, YELLOW, BLUE, RESET, 
    SHODAN_API_KEY, VIRUSTOTAL_API_KEY, NUCLEI_TOKEN, GEMINI_API_KEY, GEMINI_MODEL
)
from utils import (
    safe_import, wait_for_input, is_linux
)
from loading import start_loading, stop_loading
from ui import logo, print_menu_header, print_menu_option

# Imports with safe_import fallback
try:
    import requests
except ImportError:
    safe_import("requests")
    import requests

try:
    import shodan
except ImportError:
    safe_import("shodan")
    import shodan

try:
    import vt
except ImportError:
    safe_import("vt-py", "vt-py")
    import vt

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
except ImportError:
    safe_import("reportlab")
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT


def generate_vulnerability_report(scan_results, target, severities):
    """Generate a professional PDF vulnerability report using Gemini 3 Pro."""
    print(f"\n{YELLOW}Generating professional PDF report with Gemini AI analysis...{RESET}")
    
    start_loading("Consulting Gemini AI for security analysis", style="cyber")
    
    # Gemini API Configuration
    GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    
    # Prepare scan data for AI analysis
    scan_data_str = str(scan_results) if not isinstance(scan_results, str) else scan_results
    
    prompt = f"""You are a professional cybersecurity analyst. Analyze the following vulnerability scan results and provide a comprehensive security assessment report.

Target: {target}
Severity Levels Scanned: {severities}
Scan Results:
{scan_data_str[:8000]}

Please provide a detailed analysis in the following format:

1. EXECUTIVE SUMMARY
- Brief overview of the security posture
- Total vulnerabilities found by severity
- Overall risk rating (Critical/High/Medium/Low)

2. KEY FINDINGS
- List each vulnerability found with:
  - Vulnerability name/type
  - Severity level
  - Description of the issue
  - Potential impact

3. DETAILED ANALYSIS
- Technical breakdown of significant vulnerabilities
- Attack vectors and exploitation scenarios

4. RECOMMENDATIONS
- Prioritized remediation steps
- Short-term fixes (immediate actions)
- Long-term security improvements

5. CONCLUSION
- Summary of security state
- Next steps for the organization

Be professional, thorough, and actionable in your analysis.
IMPORTANT: DO NOT USE MARKDOWN FORMATTING. Do not use **bold**, ### headers, or `code` backticks.
- Write in clean, plain text.
- Use UPPERCASE for section headings.
- Use dashes (-) for bullet points.
- Focus on professional presentation."""

    try:
        # Call Gemini API
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 4096
            }
        }
        
        response = requests.post(GEMINI_URL, json=payload, timeout=120)
        
        if response.status_code == 200:
            data = response.json()
            # Extract text from Gemini response
            ai_analysis = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            if not ai_analysis:
                raise Exception("Empty response from Gemini")
            stop_loading("AI analysis complete!")
        else:
            raise Exception(f"Gemini API error: {response.status_code} - {response.text[:200]}")
        
    except Exception as e:
        stop_loading("AI analysis failed (using basic report)", success=False)
        print(f"{YELLOW}AI analysis error: {e}. Using basic report format.{RESET}")
        ai_analysis = f"""EXECUTIVE SUMMARY
==================
Vulnerability scan completed for {target}.
Severities scanned: {severities}

SCAN RESULTS
============
{scan_data_str[:3000]}

RECOMMENDATIONS
===============
- Review all findings and prioritize by severity
- Address critical and high severity issues immediately
- Implement regular security scanning schedule
"""

    # Generate PDF report
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_target = re.sub(r'[^\w\-_]', '_', target.replace('https://', '').replace('http://', ''))
    pdf_filename = f"vulnerability_report_{safe_target}_{timestamp}.pdf"
    
    start_loading("Compiling PDF Report", style="blocks")
    
    try:
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter,
                                rightMargin=60, leftMargin=60,
                                topMargin=50, bottomMargin=50)
        
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#0d1b2a'),
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=14,
            spaceAfter=8,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1b263b'),
            fontName='Helvetica'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceBefore=18,
            spaceAfter=10,
            textColor=colors.HexColor('#1b263b'),
            fontName='Helvetica-Bold',
            borderPadding=5,
            leftIndent=0
        )
        
        subheading_style = ParagraphStyle(
            'SubHeading',
            parent=styles['Heading3'],
            fontSize=12,
            spaceBefore=12,
            spaceAfter=6,
            textColor=colors.HexColor('#415a77'),
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            leading=16,
            fontName='Helvetica'
        )
        
        bullet_style = ParagraphStyle(
            'BulletStyle',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            leftIndent=20,
            leading=13,
            fontName='Helvetica'
        )
        
        # Build PDF content
        story = []
        
        # Title page with professional header
        story.append(Spacer(1, 1.5*inch))
        
        # Main title
        story.append(Paragraph("VULNERABILITY ASSESSMENT", title_style))
        story.append(Paragraph("SECURITY REPORT", title_style))
        story.append(Spacer(1, 0.4*inch))
        
        # Horizontal line
        line_data = [['']]
        line_table = Table(line_data, colWidths=[5.5*inch])
        line_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#778da9')),
        ]))
        story.append(line_table)
        story.append(Spacer(1, 0.4*inch))
        
        # Target info box
        info_data = [
            ['TARGET', target],
            ['DATE', datetime.datetime.now().strftime('%B %d, %Y at %H:%M')],
            ['SEVERITY SCOPE', severities.upper()],
            ['CLASSIFICATION', 'CONFIDENTIAL']
        ]
        info_table = Table(info_data, colWidths=[1.5*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#415a77')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#1b263b')),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (0, -1), 15),
        ]))
        story.append(info_table)
        
        story.append(Spacer(1, 1*inch))
        
        # Classification banner
        classification_style = ParagraphStyle(
            'Classification',
            parent=styles['Normal'],
            fontSize=11,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#c1121f'),
            fontName='Helvetica-Bold',
            spaceBefore=20
        )
        story.append(Paragraph("FOR AUTHORIZED PERSONNEL ONLY", classification_style))
        
        story.append(PageBreak())
        
        # Table of Contents
        story.append(Paragraph("TABLE OF CONTENTS", heading_style))
        story.append(Spacer(1, 0.15*inch))
        
        toc_items = [
            "1. Executive Summary",
            "2. Key Findings",
            "3. Detailed Analysis", 
            "4. Recommendations",
            "5. Conclusion"
        ]
        for item in toc_items:
            story.append(Paragraph(item, body_style))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Horizontal separator
        story.append(Table([['']], colWidths=[5.5*inch], style=[('LINEABOVE', (0, 0), (-1, 0), 1, colors.HexColor('#778da9'))]))
        story.append(Spacer(1, 0.2*inch))
        
        # Process AI Analysis content
        lines = ai_analysis.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Clean special characters and Markdown artifacts
            line = line.replace('**', '').replace('__', '').replace('### ', '').replace('## ', '').replace('`', '')
            line = line.replace('─', '-').replace('═', '=').replace('•', '-')
            line = line.replace('■', '').replace('□', '').replace('▪', '-')
            line = line.replace('★', '*').replace('●', '-').replace('○', '-')
            line = re.sub(r'[^\x00-\x7F]+', '', line)  # Remove non-ASCII
            
            # Escape XML special chars
            line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            # Detect section headers
            if re.match(r'^[1-5]\.\s+[A-Z]', line) or line.isupper():
                # Main section header
                story.append(Spacer(1, 0.15*inch))
                story.append(Paragraph(line, heading_style))
            elif re.match(r'^[-*]\s+', line):
                # Bullet point
                bullet_text = re.sub(r'^[-*]\s+', '- ', line)
                story.append(Paragraph(bullet_text, bullet_style))
            elif re.match(r'^\d+\)', line) or re.match(r'^[a-z]\)', line):
                # Numbered or lettered list
                story.append(Paragraph(line, bullet_style))
            elif line.endswith(':') and len(line) < 60:
                # Sub-heading
                story.append(Paragraph(line, subheading_style))
            else:
                # Regular paragraph
                story.append(Paragraph(line, body_style))
        
        # Footer section
        story.append(Spacer(1, 0.5*inch))
        story.append(Table([['']], colWidths=[5.5*inch], style=[('LINEABOVE', (0, 0), (-1, 0), 1, colors.HexColor('#778da9'))]))
        story.append(Spacer(1, 0.2*inch))
        
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#415a77'),
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique'
        )
        story.append(Paragraph("Report was made by Khalaf & Timaa", footer_style))
        story.append(Paragraph(f"Generated on {datetime.datetime.now().strftime('%B %d, %Y')}", footer_style))
        
        # Build PDF
        doc.build(story)
        
        stop_loading("PDF Generated successfully")
        print(f"\n{GREEN}PDF Report generated successfully!{RESET}")
        print(f"{BLUE}Report saved to: {os.path.abspath(pdf_filename)}{RESET}")
        return pdf_filename
        
    except Exception as e:
        stop_loading("PDF Generation failed", success=False)
        print(f"{RED}Error generating PDF: {e}{RESET}")
        # Fallback: save as text file
        txt_filename = pdf_filename.replace('.pdf', '.txt')
        with open(txt_filename, 'w', encoding='utf-8') as f:
            f.write(f"VULNERABILITY ASSESSMENT REPORT\n")
            f.write(f"{'='*50}\n")
            f.write(f"Target: {target}\n")
            f.write(f"Date: {datetime.datetime.now().strftime('%B %d, %Y')}\n")
            f.write(f"Severities: {severities}\n\n")
            f.write(ai_analysis)
            f.write(f"\n\nReport was made by Khalaf & Timaa")
        print(f"{YELLOW}Saved as text file instead: {txt_filename}{RESET}")
        return txt_filename


def nuclei_scan():
    """Comprehensive vulnerability scan with multiple tools - parallel API calls."""
    # Local import to avoid circular dependency
    from main import main_menu
    
    logo()
    print_menu_header("Comprehensive Security Scan")
    print(f"{GREEN}Multi-tool vulnerability assessment with AI-powered reporting.{RESET}")
    print(f"{YELLOW}Cloud APIs run in PARALLEL for speed!{RESET}\n")
    
    target = input(f"{GREEN}Enter target (URL or IP): {RESET}").strip()
    
    if not target:
        print(f"{RED}No target specified.{RESET}")
        wait_for_input(main_menu)
        return
    
    # Parse target
    original_target = target
    url_target = target if target.startswith(('http://', 'https://')) else 'https://' + target
    ip_target = target.replace('https://', '').replace('http://', '').split('/')[0].split(':')[0]
    
    print(f"\n{BLUE}Available Scan Types:{RESET}")
    print(f"{GREEN}[CLOUD - Run in Parallel]{RESET}")
    print_menu_option("1", "Nuclei Vulnerability Scan (CVEs, misconfigs)")
    print_menu_option("2", "Shodan Deep Scan (Ports, vulns, banners)")
    print_menu_option("8", "VirusTotal Check (Malware detection)")
    print(f"\n{YELLOW}[LOCAL - Run Sequentially]{RESET}")
    print_menu_option("3", "Nmap Port Scan (Active scanning)")
    print_menu_option("4", "Directory Discovery (Hidden paths)")
    print_menu_option("5", "SSL/TLS Analysis (Certificates)")
    print_menu_option("6", "HTTP Headers (Security headers)")
    print_menu_option("7", "DNS Enumeration (DNS records)")
    
    print(f"\n{YELLOW}Example: '1+2+8' runs all cloud APIs in parallel!{RESET}")
    print(f"{YELLOW}Enter 'all' for complete scan{RESET}\n")
    
    selection = input(f"{GREEN}Select scans (e.g., 1+2+8 or 'all'): {RESET}").strip().lower()
    
    if not selection:
        selection = "1+2+8"
    
    if selection == 'all':
        selected_scans = ['1', '2', '3', '4', '5', '6', '7', '8']
    else:
        selected_scans = [s.strip() for s in selection.replace(',', '+').split('+')]
    
    # Severity for Nuclei (Always All)
    severities = "info,low,medium,high,critical"
    
    # Delay for local scans (Always Normal - 15s)
    scan_delay = 15
    
    # Separate cloud and local scans
    cloud_scans = [s for s in selected_scans if s in ['1', '2', '8']]
    local_scans = [s for s in selected_scans if s in ['3', '4', '5', '6', '7']]
    
    print(f"\n{YELLOW}{'='*50}{RESET}")
    print(f"{GREEN}Starting Security Assessment{RESET}")
    print(f"{BLUE}Target: {original_target}{RESET}")
    print(f"{BLUE}Cloud APIs (parallel): {len(cloud_scans)} | Local (sequential): {len(local_scans)}{RESET}")
    print(f"{YELLOW}{'='*50}{RESET}")
    
    all_results = {}
    
    # ==================== CLOUD API SCAN FUNCTIONS ====================
    def scan_nuclei():
        """Nuclei API scan"""
        try:
            params = {"token": NUCLEI_TOKEN, "target": url_target, "sev": severities}
            response = requests.get("https://nucleiapi-production.up.railway.app/scan", params=params, timeout=600)
            if response.status_code == 200:
                try:
                    return ('nuclei', response.json())
                except:
                    return ('nuclei', response.text)
            return ('nuclei', f"Error: {response.status_code}")
        except Exception as e:
            return ('nuclei', f"Error: {str(e)}")
    
    def scan_shodan():
        """Shodan API scan"""
        try:
            import socket
            resolved_ip = socket.gethostbyname(ip_target)
            api = shodan.Shodan(SHODAN_API_KEY)
            host = api.host(resolved_ip)
            
            result = {
                'ip': host.get('ip_str'),
                'organization': host.get('org', 'N/A'),
                'isp': host.get('isp', 'N/A'),
                'country': host.get('country_name', 'N/A'),
                'os': host.get('os', 'N/A'),
                'ports': host.get('ports', []),
                'vulns': host.get('vulns', []),
                'hostnames': host.get('hostnames', []),
            }
            
            services = []
            for item in host.get('data', []):
                svc = {
                    'port': item.get('port'),
                    'service': item.get('product', 'unknown'),
                    'version': item.get('version', 'N/A'),
                    'banner': item.get('data', '')[:150]
                }
                if 'vulns' in item:
                    svc['cves'] = list(item['vulns'].keys())
                services.append(svc)
            result['services'] = services
            
            return ('shodan', result)
        except shodan.APIError as e:
            if 'Access denied' in str(e) or '403' in str(e):
                return ('shodan', "Shodan Skipped (Free Plan Limit)")
            if 'No information' in str(e):
                return ('shodan', f"IP not indexed in Shodan")
            return ('shodan', f"Shodan error: {str(e)}")
        except Exception as e:
            if '403' in str(e):
                return ('shodan', "Shodan Skipped (Free Plan Limit)")
            return ('shodan', f"Error: {str(e)}")
    
    def scan_virustotal():
        """VirusTotal API scan"""
        try:
            with vt.Client(VIRUSTOTAL_API_KEY) as client:
                url_id = vt.url_id(url_target)
                try:
                    url_obj = client.get_object(f"/urls/{url_id}")
                    stats = url_obj.last_analysis_stats
                    return ('virustotal', {
                        'malicious': stats.get('malicious', 0),
                        'suspicious': stats.get('suspicious', 0),
                        'harmless': stats.get('harmless', 0),
                        'undetected': stats.get('undetected', 0),
                        'reputation': url_obj.get('reputation', 'N/A'),
                        'categories': url_obj.get('categories', {}),
                    })
                except:
                    analysis = client.scan_url(url_target, wait_for_completion=False)
                    return ('virustotal', {'status': 'Scan submitted', 'id': analysis.id})
        except Exception as e:
            return ('virustotal', f"Error: {str(e)}")
    
    # ==================== RUN CLOUD SCANS IN PARALLEL ====================
    if cloud_scans:
        print(f"\n{GREEN}[CLOUD] Running {len(cloud_scans)} API scans in parallel...{RESET}")
        
        cloud_functions = {
            '1': ('Nuclei', scan_nuclei),
            '2': ('Shodan', scan_shodan),
            '8': ('VirusTotal', scan_virustotal),
        }
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {}
            for scan_id in cloud_scans:
                if scan_id in cloud_functions:
                    name, func = cloud_functions[scan_id]
                    futures[executor.submit(func)] = name
            
            start_loading(f"Running {len(futures)} cloud scans in parallel...", style="cyber")
            
            remaining = len(futures)
            for future in as_completed(futures):
                name = futures[future]
                stop_loading() # Stop animation to print output safely
                
                try:
                    scan_name, result = future.result()
                    all_results[scan_name] = result
                    if isinstance(result, dict):
                        print(f"  {GREEN}{name} complete!{RESET}")
                    else:
                        print(f"  {YELLOW}{name}: {result[:50]}...{RESET}")
                except Exception as e:
                    print(f"  {RED}{name} failed: {e}{RESET}")
                
                remaining -= 1
                if remaining > 0:
                    start_loading(f"Scanning... ({remaining} left)", style="cyber")
        
        print(f"{GREEN}[CLOUD] All API scans finished!{RESET}")
    
    # ==================== RUN LOCAL SCANS SEQUENTIALLY ====================
    if local_scans:
        print(f"\n{YELLOW}[LOCAL] Running {len(local_scans)} local scans sequentially...{RESET}")
        
        # 3. Nmap
        if '3' in local_scans:
            print(f"\n{YELLOW}Running Nmap Port Scan...{RESET}")
            start_loading("Scanning ports with Nmap", style="hack")
            try:
                result = subprocess.run(
                    ['nmap', '-Pn', '-n', '--top-ports', '100', '-sV', '--version-light', '-T3', ip_target],
                    capture_output=True, text=True, timeout=600
                )
                stop_loading("Nmap complete!")
                all_results['nmap'] = result.stdout if result.stdout else "No results"
            except FileNotFoundError:
                stop_loading("Nmap not installed", success=False)
                all_results['nmap'] = "Nmap not installed"
            except subprocess.TimeoutExpired:
                stop_loading("Nmap timed out", success=False)
                all_results['nmap'] = "Timed out"
            except Exception as e:
                stop_loading("Nmap error", success=False)
                all_results['nmap'] = f"Error: {str(e)}"
            
            if len(local_scans) > 1:
                print(f"{BLUE}Waiting {scan_delay}s...{RESET}")
                time.sleep(scan_delay)
        
        # 4. Directory Discovery
        if '4' in local_scans:
            print(f"\n{YELLOW}Running Directory Discovery...{RESET}")
            start_loading("Bruteforcing directories", style="matrix")
            paths = ['/admin', '/login', '/api', '/backup', '/.git', '/.env', '/robots.txt', 
                    '/config', '/uploads', '/swagger', '/graphql', '/phpmyadmin']
            found = []
            for path in paths:
                try:
                    r = requests.head(url_target.rstrip('/') + path, timeout=5, allow_redirects=False,
                                     headers={'User-Agent': 'Mozilla/5.0'})
                    if r.status_code in [200, 301, 302, 401, 403]:
                        found.append(f"{path} [{r.status_code}]")
                    time.sleep(0.2)
                except Exception as e:
                    pass
            stop_loading(f"Found {len(found)} paths")
            all_results['directories'] = {'found': len(found), 'paths': found} if found else "No paths found"
            
            if len([s for s in local_scans if s in ['5', '6', '7']]) > 0:
                print(f"{BLUE}Waiting {scan_delay}s...{RESET}")
                time.sleep(scan_delay)
        
        # 5. SSL/TLS
        if '5' in local_scans:
            print(f"\n{YELLOW}Running SSL/TLS Analysis...{RESET}")
            start_loading("Analyzing SSL Certificate", style="pulse")
            try:
                import ssl
                import socket
                context = ssl.create_default_context()
                with socket.create_connection((ip_target, 443), timeout=15) as sock:
                    with context.wrap_socket(sock, server_hostname=ip_target) as ssock:
                        cert = ssock.getpeercert()
                        all_results['ssl'] = {
                            'protocol': ssock.version(),
                            'cipher': ssock.cipher()[0],
                            'issuer': dict(x[0] for x in cert.get('issuer', [])),
                            'valid_until': cert.get('notAfter'),
                        }
                stop_loading("SSL analysis complete")
            except Exception as e:
                stop_loading("SSL analysis failed", success=False)
                print(f"{RED}SSL Analysis failed (skipping): {e}{RESET}")
                all_results['ssl'] = f"Error: {str(e)}"
            
            if len([s for s in local_scans if s in ['6', '7']]) > 0:
                print(f"{BLUE}Waiting {scan_delay}s...{RESET}")
                time.sleep(scan_delay)
        
        # 6. HTTP Headers
        if '6' in local_scans:
            print(f"\n{YELLOW}Analyzing HTTP Headers...{RESET}")
            start_loading("Checking security headers", style="dots")
            try:
                r = requests.get(url_target, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
                sec_headers = ['Strict-Transport-Security', 'Content-Security-Policy', 'X-Frame-Options',
                              'X-Content-Type-Options', 'X-XSS-Protection', 'Referrer-Policy']
                analysis = {h: 'PRESENT' if h in r.headers else 'MISSING' for h in sec_headers}
                present = sum(1 for v in analysis.values() if v == 'PRESENT')
                all_results['headers'] = {'score': f"{present}/{len(sec_headers)}", 'analysis': analysis}
                stop_loading(f"Headers: {present}/{len(sec_headers)}")
            except Exception as e:
                stop_loading("Header analysis failed", success=False)
                print(f"{RED}Header Analysis failed (skipping): {e}{RESET}")
                all_results['headers'] = f"Error: {str(e)}"
            
            if '7' in local_scans:
                print(f"{BLUE}Waiting {scan_delay}s...{RESET}")
                time.sleep(scan_delay)
        
        # 7. DNS
        if '7' in local_scans:
            print(f"\n{YELLOW}Running DNS Enumeration...{RESET}")
            start_loading("Querying DNS records", style="wave")
            try:
                import socket
                dns_results = {'ip': socket.gethostbyname(ip_target)}
                result = subprocess.run(['nslookup', ip_target], capture_output=True, text=True, timeout=15)
                if result.stdout:
                    dns_results['nslookup'] = result.stdout[:500]
                all_results['dns'] = dns_results
                stop_loading("DNS complete")
            except Exception as e:
                stop_loading("DNS failed", success=False)
                print(f"{RED}DNS Enumeration failed (skipping): {e}{RESET}")
                all_results['dns'] = f"Error: {str(e)}"
    
    # ==================== GENERATE REPORT ====================
    print(f"\n{GREEN}{'='*50}{RESET}")
    print(f"{GREEN}All scans completed! Generating AI report...{RESET}")
    print(f"{GREEN}{'='*50}{RESET}")
    
    tools_used = []
    for s, name in [('1','Nuclei'),('2','Shodan'),('3','Nmap'),('4','DirScan'),('5','SSL'),('6','Headers'),('7','DNS'),('8','VirusTotal')]:
        if s in selected_scans: tools_used.append(name)
    
    compiled = f"SECURITY ASSESSMENT\nTarget: {original_target}\nDate: {datetime.datetime.now()}\nTools: {', '.join(tools_used)}\n\n"
    for k, v in all_results.items():
        compiled += f"\n{'='*40}\n{k.upper()}:\n{'='*40}\n"
        if isinstance(v, dict):
            try:
                compiled += json.dumps(v, indent=2, default=str)
            except TypeError:
                compiled += str(v)
        else:
            compiled += str(v)
        compiled += "\n"
    
    report_file = generate_vulnerability_report(compiled, original_target, severities)
    
    if report_file:
        print(f"\n{GREEN}{'='*50}{RESET}")
        print(f"{GREEN}  ASSESSMENT COMPLETE{RESET}")
        print(f"{GREEN}{'='*50}{RESET}")
        print(f"\n{BLUE}Report: {os.path.abspath(report_file)}{RESET}\n")
    
    wait_for_input(main_menu)
