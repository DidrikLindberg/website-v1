"""
Flask application for web development consulting firm website.
Simple, clean architecture with Jinja2 templates and minimal dependencies.
"""

from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuration - EDIT THESE VALUES
SITE_CONFIG = {
    'company_name': 'A-frame Solutions',
    'tagline': 'Salesforce Development & Strategic Consulting',
    'email': 'contact@yourcompany.com',
    'linkedin': 'https://www.linkedin.com/in/didrik-lindberg-3b2955148/',
    'phone': '+1 (555) 123-4567',
}

# Services data - EDIT THIS
SERVICES = [
    {
        'id': 'salesforce-custom-development',
        'title': 'Salesforce Custom Development',
        'icon': '⚡',
        'short_description': 'Tailored Salesforce solutions built with Apex, LWC, and platform best practices.',
        'full_description': 'We architect and develop custom Salesforce applications that extend platform capabilities to match your unique business processes. From complex automation to custom UI components, we build scalable solutions that leverage the full power of the Salesforce ecosystem.',
        'deliverables': [
            'Custom Apex triggers, classes, and batch jobs',
            'Lightning Web Components (LWC) development',
            'Visualforce pages and custom controllers',
            'Custom objects, fields, and data model design',
            'Platform Events and integration patterns',
            'Comprehensive unit testing and code coverage',
        ],
        'ideal_for': 'Organizations with complex Salesforce requirements, healthcare and financial services needing compliance features, enterprises scaling their Salesforce instance',
        'outcomes': [
            'Automated workflows that eliminate manual processes',
            'Custom features tailored to your business logic',
            'Scalable architecture following platform best practices',
            'Improved user adoption through intuitive interfaces',
        ]
    },
    {
        'id': 'salesforce-consulting',
        'title': 'Salesforce Strategic Consulting',
        'icon': '🎯',
        'short_description': 'Expert guidance on Salesforce architecture, optimization, and strategic roadmap planning.',
        'full_description': 'We provide strategic consulting services to help you maximize your Salesforce investment. Whether you need architecture review, performance optimization, or roadmap planning, we bring deep platform expertise to guide your Salesforce journey.',
        'deliverables': [
            'Architecture assessment and recommendations',
            'Technical debt analysis and remediation strategy',
            'Performance optimization and governor limit management',
            'Security and compliance audits',
            'Release management and deployment strategy',
            'Team training and knowledge transfer',
        ],
        'ideal_for': 'Companies inheriting complex Salesforce orgs, organizations planning major platform initiatives, teams facing technical challenges or governor limits',
        'outcomes': [
            'Optimized platform performance and scalability',
            'Clear technical roadmap aligned with business goals',
            'Reduced technical debt and maintenance costs',
            'Enhanced security posture and compliance readiness',
        ]
    },
    {
        'id': 'salesforce-integrations',
        'title': 'Salesforce Integration & Automation',
        'icon': '🔗',
        'short_description': 'Connect Salesforce with external systems through robust, real-time integrations.',
        'full_description': 'We design and implement secure, scalable integrations that connect Salesforce with your enterprise systems, third-party applications, and external data sources. Our integration patterns ensure data consistency and real-time synchronization.',
        'deliverables': [
            'REST/SOAP API integrations',
            'MuleSoft and middleware implementations',
            'Platform Events and Change Data Capture',
            'ETL processes and data migration',
            'Heroku and external system connectivity',
            'Error handling and monitoring dashboards',
        ],
        'ideal_for': 'Organizations with complex system landscapes, companies migrating to Salesforce, businesses requiring real-time data synchronization',
        'outcomes': [
            'Seamless data flow between systems',
            'Real-time synchronization and reduced latency',
            'Automated data validation and error handling',
            'Single source of truth across platforms',
        ]
    },
    {
        'id': 'salesforce-optimization',
        'title': 'Salesforce Platform Optimization',
        'icon': '🚀',
        'short_description': 'Performance tuning, code refactoring, and optimization to scale your Salesforce org.',
        'full_description': 'We analyze and optimize your Salesforce implementation to improve performance, reduce governor limit issues, and ensure your org scales efficiently. From query optimization to architectural refactoring, we make your Salesforce faster and more reliable.',
        'deliverables': [
            'Performance profiling and bottleneck identification',
            'SOQL query optimization and indexing strategy',
            'Code refactoring and design pattern implementation',
            'Asynchronous processing architecture',
            'Data archiving and storage optimization',
            'Custom metadata and configuration optimization',
        ],
        'ideal_for': 'Organizations hitting governor limits, slow-performing Salesforce orgs, companies preparing for high-growth scaling',
        'outcomes': [
            'Faster page loads and improved user experience',
            'Elimination of governor limit errors',
            'Reduced API consumption and costs',
            'Scalable architecture ready for growth',
        ]
    },
]
# Projects/Case Studies - EDIT THIS
PROJECTS = [
    {
        'id': 'ephi-audit-system',
        'title': 'ePHI Audit & Compliance Platform',
        'client': 'National Behavioral Health Network',
        'tagline': 'Metadata-driven Salesforce audit layer covering every PHI touchpoint across five critical objects.',
        'image_placeholder': '🩺',
        'problem': 'Compliance and security teams lacked field-level visibility into how clinicians and coordinators were touching protected health information. Manual audits across Account, Contact, Assessment, Order, and Program Engagement objects took days and still left blind spots around record views.',
        'solution': 'Architected a modular audit platform with Apex triggers, Lightning Web Components, and metadata-driven configuration. Triggers capture create/update/delete events per field, while an invisible LWC logs view/close activity in real time. Custom metadata toggles tracked objects and fields without deployments, and BaseDML services guarantee partial-success inserts.',
        'tech_stack': ['Salesforce Platform', 'Apex', 'Lightning Web Components', 'Custom Metadata Types', 'Field Sets', 'Platform Events'],
        'results': [
            '100% Create/View/Edit/Delete coverage across Account, Contact, Assessment, Order, and Program Engagement',
            'Per-field audit records generated automatically for every change, ready for HIPAA reporting in minutes',
            'View/close tracking closes blind spots and proves who accessed sensitive records',
            'Admins adjust tracked fields through metadata with no additional code releases',
        ],
        'featured': True,
    },
    {
        'id': 'hipaa-suspicious-login',
        'title': 'HIPAA Suspicious Login Detection',
        'client': 'Regional Healthcare System',
        'tagline': 'Proactive Salesforce security pipeline that flags risky logins within 15 minutes and routes investigators.',
        'image_placeholder': '🔐',
        'problem': 'Security leadership needed continuous insight into suspicious login behavior but was stuck exporting LoginHistory weekly and triaging alerts manually. Investigations were slow, inconsistent, and difficult to audit.',
        'solution': 'Delivered a schedulable + queueable orchestration that sweeps LoginHistory every 15 minutes, evaluates risk via configurable metadata, and writes prioritized alerts to Suspicious_Login__c. Lightning dashboards and reviewer utilities give investigators one queue for triage, while platform events and permission sets enforce least privilege.',
        'tech_stack': ['Salesforce', 'Apex', 'Platform Events', 'Queueables', 'Lightning Web Components', 'Custom Metadata Types'],
        'results': [
            'Continuous monitoring with a 15-minute rolling detection window covering 100% of logins',
            'Automated investigator queue with deduplicated alerts and merged violation reasons',
            'Configurable thresholds, whitelists, and schedules managed entirely by admins',
            'Investigation time reduced by 60% thanks to richer context and prioritized routing',
        ],
        'featured': True,
    },
    {
        'id': 'financial-services-portal',
        'title': 'Financial Services Client Portal',
        'client': 'Investment Advisory Firm',
        'tagline': 'Custom Salesforce Experience Cloud portal delivering real-time portfolio insights to 2,500+ high-net-worth clients.',
        'image_placeholder': '💼',
        'problem': 'Wealth management firm needed to provide clients with secure, real-time access to portfolio performance, documents, and advisor communications. Their legacy portal was outdated, slow, and required manual data updates from multiple systems.',
        'solution': 'Built a modern Experience Cloud portal with Lightning Web Components for interactive dashboards, integrated with external portfolio management systems via REST APIs. Implemented Einstein Analytics for portfolio visualization and automated document generation using Apex batch processes. Single Sign-On (SSO) with MFA ensures security compliance.',
        'tech_stack': ['Salesforce Experience Cloud', 'Lightning Web Components', 'Apex', 'Einstein Analytics', 'REST APIs', 'Single Sign-On'],
        'results': [
            'Real-time portfolio data synchronized hourly from external systems',
            '2,500+ clients onboarded with 87% monthly active usage',
            'Client support inquiries reduced by 45% through self-service access',
            'Automated quarterly report generation saving 200+ advisor hours per quarter',
        ],
        'featured': True,
    },
    {
        'id': 'manufacturing-cpq',
        'title': 'Manufacturing CPQ & Quote Automation',
        'client': 'Industrial Equipment Manufacturer',
        'tagline': 'Salesforce CPQ implementation with custom pricing logic reducing quote generation time by 75%.',
        'image_placeholder': '⚙️',
        'problem': 'Sales team spent 4-6 hours per complex equipment quote, manually calculating configurations, discounts, and delivery timelines across 10,000+ SKUs. Pricing errors occurred in 15% of quotes, causing margin erosion and contract disputes.',
        'solution': 'Implemented Salesforce CPQ with custom Apex pricing calculators for volume discounts, product bundling rules, and delivery lead-time calculations. Built guided selling flows in Lightning for configuration validation. Integrated with ERP system for real-time inventory checks and automated proposal document generation.',
        'tech_stack': ['Salesforce CPQ', 'Apex', 'Lightning Flow', 'Product Rules', 'Price Rules', 'Document Generation', 'ERP Integration'],
        'results': [
            'Quote generation time reduced from 4-6 hours to under 1 hour',
            'Pricing error rate decreased from 15% to under 2%',
            'Sales cycle shortened by 18 days on average',
            'Automated approval workflows handling 85% of quotes without manual intervention',
        ],
        'featured': True,
    },
    {
        'id': 'nonprofit-donor-management',
        'title': 'Nonprofit Donor Management System',
        'client': 'National Healthcare Foundation',
        'tagline': 'Salesforce Nonprofit Cloud customization managing $50M+ in annual donations across 15,000+ donors.',
        'image_placeholder': '❤️',
        'problem': 'Foundation tracked donor relationships, grants, and program outcomes across multiple disconnected databases. Fundraising staff lacked visibility into donor history, engagement scores, and campaign effectiveness, limiting personalized outreach.',
        'solution': 'Customized Nonprofit Cloud with Apex automation for donor scoring, Einstein recommendations for optimal engagement timing, and custom Lightning components for campaign tracking. Integrated with marketing automation platform and payment processors. Built executive dashboards showing real-time fundraising metrics.',
        'tech_stack': ['Salesforce Nonprofit Cloud', 'Apex', 'Einstein Analytics', 'Lightning Web Components', 'Marketing Cloud Integration', 'Payment Gateway APIs'],
        'results': [
            'Unified view of 15,000+ donors with complete engagement history',
            'Donor retention increased by 23% through personalized engagement',
            '$50M+ in annual donations tracked with full attribution reporting',
            'Campaign ROI visibility improved with automated performance dashboards',
        ],
        'featured': False,
    },
    {
        'id': 'retail-inventory-sync',
        'title': 'Retail Multi-Channel Inventory Sync',
        'client': 'Specialty Retail Chain',
        'tagline': 'Real-time Salesforce-to-ERP inventory synchronization across 80+ retail locations and e-commerce.',
        'image_placeholder': '🏪',
        'problem': 'Retail chain struggled with inventory discrepancies between Salesforce, their e-commerce platform, and warehouse management system. Out-of-stock situations and overselling caused customer dissatisfaction and lost revenue.',
        'solution': 'Architected bi-directional integration using Platform Events and MuleSoft for real-time inventory updates. Implemented Change Data Capture to push Salesforce order updates to ERP, with webhook receivers for external inventory changes. Built custom Lightning dashboards for inventory visibility and automated reorder triggers.',
        'tech_stack': ['Salesforce', 'MuleSoft', 'Platform Events', 'Change Data Capture', 'Apex', 'REST APIs', 'Heroku'],
        'results': [
            'Real-time inventory sync across 80+ locations with sub-minute latency',
            'Overselling incidents reduced by 92%',
            'Customer satisfaction scores improved by 28%',
            'Inventory carrying costs reduced by 15% through optimized reordering',
        ],
        'featured': False,
    },
]

# Testimonials - EDIT THIS
TESTIMONIALS = [
    {
        'quote': 'A-frame Solutions transformed our Salesforce implementation. Their custom compliance platform gave us the HIPAA audit capabilities we desperately needed, and their team understood both the technical and regulatory requirements perfectly.',
        'author': 'Sarah Mitchell',
        'title': 'VP of Compliance',
        'company': 'National Behavioral Health Network',
    },
    {
        'quote': 'The security monitoring system they built has been a game-changer for our organization. We now have real-time visibility into suspicious login activity, and their Salesforce expertise showed in every aspect of the solution.',
        'author': 'Michael Rodriguez',
        'title': 'CISO',
        'company': 'Regional Healthcare System',
    },
    {
        'quote': 'Working with A-frame Solutions on our client portal project exceeded expectations. They delivered a beautiful, functional Experience Cloud solution that our clients love, and they handled the complex integrations flawlessly.',
        'author': 'Jennifer Chang',
        'title': 'Director of Digital Experience',
        'company': 'Investment Advisory Firm',
    },
]


@app.route('/')
def home():
    """Home page with hero, services overview, featured projects, and testimonials."""
    featured_projects = [p for p in PROJECTS if p.get('featured', False)][:2]
    return render_template(
        'home.html',
        config=SITE_CONFIG,
        services=SERVICES[:4],  # Show first 4 services on home
        projects=featured_projects,
        testimonials=TESTIMONIALS,
    )


@app.route('/services')
def services():
    """Services page with detailed service information."""
    return render_template(
        'services.html',
        config=SITE_CONFIG,
        services=SERVICES,
    )


@app.route('/projects')
def projects():
    """Projects overview page."""
    return render_template(
        'projects.html',
        config=SITE_CONFIG,
        projects=PROJECTS,
    )


@app.route('/projects/<project_id>')
def project_detail(project_id):
    """Individual project case study page."""
    project = next((p for p in PROJECTS if p['id'] == project_id), None)
    if not project:
        return redirect(url_for('projects'))
    return render_template(
        'project_detail.html',
        config=SITE_CONFIG,
        project=project,
    )


@app.route('/about')
def about():
    """About page with company/founder story and skills."""
    return render_template(
        'about.html',
        config=SITE_CONFIG,
    )


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form."""
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        company = request.form.get('company', 'Not provided')
        budget = request.form.get('budget', 'Not specified')
        message = request.form.get('message')
        
        # Basic validation
        if not name or not email or not message:
            flash('Please fill out all required fields.', 'error')
            return render_template('contact.html', config=SITE_CONFIG)
        
        # In production, you'd send an email here or save to database
        # For now, we'll just log it and show a success message
        print(f"\n=== NEW CONTACT FORM SUBMISSION ===")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Company: {company}")
        print(f"Budget: {budget}")
        print(f"Message: {message}")
        print(f"Timestamp: {datetime.now()}")
        print(f"===================================\n")
        
        # TODO: Send email using Flask-Mail or similar
        # Example: send_email(to=SITE_CONFIG['email'], subject=f"New inquiry from {name}", body=message)
        
        flash('Thanks for reaching out! We\'ll get back to you within 24 hours.', 'success')
        return redirect(url_for('contact'))
    
    return render_template(
        'contact.html',
        config=SITE_CONFIG,
    )


@app.context_processor
def inject_config():
    """Make config available to all templates."""
    return {
        'config': SITE_CONFIG,
        'current_year': datetime.now().year,
    }


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
