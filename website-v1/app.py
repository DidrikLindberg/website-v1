from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# Company Configuration
SITE_CONFIG = {
    'company_name': 'A-frame Solutions',
    'tagline': 'Salesforce Development & Strategic Consulting',
    'email': 'contact@aframesolutions.com',
    'phone': '+1 (555) 123-4567',
    'linkedin': 'https://linkedin.com/company/aframe-solutions',
    
    # Salesforce-specific credentials
    'certifications': [
        'Salesforce Certified Platform Developer II',
        'Salesforce Certified Application Architect',
        'Salesforce Certified System Architect',
        'Salesforce Certified Technical Architect (CTA) Candidate'
    ],
    'partner_status': 'Salesforce Consulting Partner',
    'years_experience': '12+',
    'projects_completed': '200+',
    'industries_served': ['Healthcare', 'Financial Services', 'Manufacturing', 'Technology', 'Nonprofit']
}

# Salesforce Services
SERVICES = [
    {
        'id': 'apex-development',
        'title': 'Custom Apex Development',
        'icon': '⚡',
        'short_description': 'Enterprise-grade Apex code that scales with your business.',
        'full_description': '''We build robust, scalable Apex solutions following Salesforce best practices and design patterns. 
        Our code is always bulkified, properly tested (90%+ coverage), and optimized for performance. We specialize in complex 
        business logic, integrations, and custom platform extensions.''',
        'deliverables': [
            'Custom Apex classes, triggers, and batch jobs',
            'Comprehensive test coverage (90%+ code coverage)',
            'Governor limit optimization and performance tuning',
            'Integration with external systems via REST/SOAP',
            'Detailed technical documentation',
            'Post-deployment support and monitoring'
        ],
        'ideal_for': 'Organizations needing complex automation, custom business logic, or Salesforce platform extensions',
        'outcomes': [
            'Automated workflows that save 20+ hours per week',
            'Scalable code that handles high data volumes',
            'Maintainable solutions with clear documentation',
            'Faster time-to-market for new features'
        ],
        'tech_highlights': ['Apex', 'SOQL/SOSL', 'Queueable', 'Batch Apex', 'Platform Events']
    },
    {
        'id': 'lightning-web-components',
        'title': 'Lightning Web Components (LWC)',
        'icon': '🎨',
        'short_description': 'Modern, responsive interfaces that delight users.',
        'full_description': '''We create beautiful, performant Lightning Web Components using modern JavaScript (ES6+) 
        and Salesforce Lightning Design System. Our components are reusable, accessible (WCAG 2.1 AA), and optimized for 
        both desktop and mobile experiences.''',
        'deliverables': [
            'Custom Lightning Web Components',
            'Lightning App Builder compatible components',
            'Mobile-responsive designs',
            'SLDS-compliant styling',
            'Cross-browser testing',
            'Component documentation and usage guides'
        ],
        'ideal_for': 'Companies wanting to modernize their Salesforce UI and improve user adoption',
        'outcomes': [
            ' 40% increase in user adoption',
            'Faster page load times',
            'Consistent, branded user experience',
            'Reduced support tickets due to intuitive design'
        ],
        'tech_highlights': ['LWC', 'JavaScript', 'HTML/CSS', 'SLDS', 'Lightning Data Service']
    },
    {
        'id': 'salesforce-consulting',
        'title': 'Strategic Salesforce Consulting',
        'icon': '🎯',
        'short_description': 'Expert guidance to maximize your Salesforce investment.',
        'full_description': '''We provide strategic consulting to help you get the most from Salesforce. From platform 
        strategy and architecture reviews to implementation roadmaps and change management, we ensure your Salesforce 
        org supports your business goals.''',
        'deliverables': [
            'Salesforce health check and org assessment',
            'Technical architecture review',
            'Implementation roadmap with priorities',
            'Best practices documentation',
            'Change management strategies',
            'Executive-level reporting and recommendations'
        ],
        'ideal_for': 'Organizations planning major Salesforce initiatives or experiencing platform challenges',
        'outcomes': [
            'Clear roadmap for Salesforce growth',
            'Reduced technical debt',
            'Better alignment with business goals',
            'Higher ROI from Salesforce investment'
        ],
        'tech_highlights': ['Platform Strategy', 'Solution Architecture', 'Best Practices', 'Governance']
    },
    {
        'id': 'integration-services',
        'title': 'Integration & Data Migration',
        'icon': '🔗',
        'short_description': 'Seamlessly connect Salesforce with your entire tech stack.',
        'full_description': '''We design and implement robust integrations between Salesforce and your external systems. 
        Whether it's ERP, marketing automation, or custom applications, we ensure data flows securely and reliably. 
        We also handle complex data migrations with zero data loss.''',
        'deliverables': [
            'Integration architecture and design',
            'Custom REST/SOAP API development',
            'Middleware configuration (MuleSoft, Boomi, etc.)',
            'Real-time and batch data sync solutions',
            'Data migration with validation',
            'Error handling and monitoring'
        ],
        'ideal_for': 'Companies with complex tech stacks needing Salesforce integration',
        'outcomes': [
            'Single source of truth across systems',
            '99.9% data sync reliability',
            'Real-time visibility into business operations',
            'Eliminated manual data entry'
        ],
        'tech_highlights': ['REST API', 'SOAP', 'Platform Events', 'Change Data Capture', 'Data Loader']
    },
    {
        'id': 'healthcare-solutions',
        'title': 'Healthcare-Specific Solutions',
        'icon': '🏥',
        'short_description': 'HIPAA-compliant Salesforce solutions for healthcare organizations.',
        'full_description': '''We specialize in building secure, HIPAA-compliant Salesforce solutions for healthcare 
        providers, payers, and life sciences companies. We understand healthcare workflows, compliance requirements, 
        and the unique challenges of the industry.''',
        'deliverables': [
            'Health Cloud implementation and customization',
            'HIPAA compliance and security reviews',
            'Patient engagement portals',
            'Provider relationship management',
            'Claims processing automation',
            'Healthcare analytics and reporting'
        ],
        'ideal_for': 'Healthcare providers, insurance companies, and medical device manufacturers',
        'outcomes': [
            'HIPAA-compliant patient data management',
            'Improved care coordination',
            'Faster claims processing',
            'Enhanced patient satisfaction scores'
        ],
        'tech_highlights': ['Health Cloud', 'Shield Platform Encryption', 'Audit Trail', 'Person Accounts']
    },
    {
        'id': 'financial-services',
        'title': 'Financial Services Solutions',
        'icon': '💰',
        'short_description': 'Secure Salesforce implementations for financial institutions.',
        'full_description': '''We build secure, compliant Salesforce solutions for banks, wealth management firms, 
        insurance companies, and fintech startups. We understand regulatory requirements, security best practices, 
        and the complex needs of financial services organizations.''',
        'deliverables': [
            'Financial Services Cloud implementation',
            'Wealth management solutions',
            'Loan origination systems',
            'Compliance and audit trail setup',
            'Client onboarding automation',
            'Financial analytics dashboards'
        ],
        'ideal_for': 'Banks, wealth advisors, insurance companies, and fintech companies',
        'outcomes': [
            'Regulatory compliance (SOX, FINRA, etc.)',
            'Faster client onboarding (50% reduction)',
            '360-degree client view',
            'Improved advisor productivity'
        ],
        'tech_highlights': ['Financial Services Cloud', 'Shield', 'Einstein Analytics', 'Actionable Relationships']
    }
]

# Case Studies / Projects
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
        'id': 'healthcare-patient-portal',
        'title': 'Patient Engagement Portal',
        'client': 'Regional Healthcare System',
        'industry': 'Healthcare',
        'tagline': 'Increased patient satisfaction by 45% with HIPAA-compliant self-service portal',
        'image_placeholder': '🏥',
        'problem': '''A 12-hospital healthcare system struggled with patient engagement and faced high call 
        center volumes for appointment scheduling and medical records requests. Patients had no self-service 
        options, leading to frustration and decreased satisfaction scores.''',
        'solution': '''We built a custom Lightning Experience portal on Salesforce Experience Cloud with 
        Health Cloud integration. Patients can schedule appointments, view lab results, message providers, 
        and access medical records securely. All data is encrypted and HIPAA-compliant with full audit trails.''',
        'tech_stack': ['Health Cloud', 'Experience Cloud', 'LWC', 'Shield Platform Encryption', 'DocuSign Integration'],
        'results': [
            '45% increase in patient satisfaction scores',
            '60% reduction in call center volume for routine requests',
            '10,000+ patients registered in first 3 months',
            'HIPAA audit passed with zero findings'
        ],
        'featured': True,
        'duration': '4 months',
        'team_size': '3 developers + 1 architect'
    },
    {
        'id': 'wealth-management-crm',
        'title': 'Wealth Management CRM',
        'client': 'Private Wealth Advisors',
        'industry': 'Financial Services',
        'tagline': 'Transformed client management for $5B AUM firm with 360° advisor view',
        'image_placeholder': '💼',
        'problem': '''A wealth management firm managing $5B in assets operated with disparate systems for 
        client data, portfolio management, and communications. Advisors wasted hours switching between systems, 
        and compliance tracking was manual and error-prone.''',
        'solution': '''We implemented Financial Services Cloud with custom Apex integrations to portfolio 
        management systems. Built custom LWC components for household relationship management, automated 
        compliance workflows, and Einstein Analytics dashboards for advisor productivity tracking.''',
        'tech_stack': ['Financial Services Cloud', 'Apex', 'LWC', 'Einstein Analytics', 'Heroku Connect'],
        'results': [
            '360° view of client households and relationships',
            '3 hours saved per advisor per day',
            '100% compliance tracking automation',
            '25% increase in assets under management'
        ],
        'featured': True,
        'duration': '6 months',
        'team_size': '4 developers + 1 architect + 1 business analyst'
    },
    {
        'id': 'manufacturing-cpq',
        'title': 'Custom CPQ Solution',
        'client': 'Industrial Equipment Manufacturer',
        'industry': 'Manufacturing',
        'tagline': 'Reduced quote generation time from 5 days to 30 minutes',
        'image_placeholder': '⚙️',
        'problem': '''A complex industrial equipment manufacturer with highly configurable products took 
        5+ days to generate quotes. Their sales team struggled with pricing rules, and errors in quotes 
        led to margin erosion and delayed deals.''',
        'solution': '''Built a custom CPQ solution using Apex and LWC with advanced pricing rules, 
        configuration logic, and integration with their ERP system. Implemented guided selling to help 
        reps configure products correctly, and automated approval workflows.''',
        'tech_stack': ['Apex', 'LWC', 'Flows', 'SAP Integration', 'DocuSign CLM'],
        'results': [
            'Quote generation reduced from 5 days to 30 minutes',
            '95% reduction in pricing errors',
            '40% increase in quote-to-close rate',
            '$2M recovered margin in first year'
        ],
        'featured': True,
        'duration': '5 months',
        'team_size': '5 developers + 1 architect'
    },
    {
        'id': 'nonprofit-fundraising',
        'title': 'Donor Management System',
        'client': 'National Education Nonprofit',
        'industry': 'Nonprofit',
        'tagline': 'Increased fundraising efficiency by 60% with Nonprofit Cloud',
        'image_placeholder': '🎓',
        'problem': '''A national education nonprofit tracked donations in spreadsheets and couldn't segment 
        donors effectively. They missed fundraising opportunities and struggled to show impact to major donors.''',
        'solution': '''Implemented Nonprofit Success Pack (NPSP) with custom campaign management, automated 
        thank-you workflows, and Einstein Analytics for donor insights. Built donor portal for donation history 
        and impact tracking.''',
        'tech_stack': ['Nonprofit Cloud (NPSP)', 'Marketing Cloud', 'Experience Cloud', 'Einstein Analytics'],
        'results': [
            '60% increase in fundraising team efficiency',
            '35% growth in recurring donations',
            'Major donor retention improved from 70% to 92%',
            'Automated thank-you process saved 200+ hours/year'
        ],
        'featured': False,
        'duration': '3 months',
        'team_size': '2 developers + 1 consultant'
    },
    {
        'id': 'saas-integration-platform',
        'title': 'Multi-SaaS Integration Hub',
        'client': 'Enterprise SaaS Company',
        'industry': 'Technology',
        'tagline': 'Connected 15 SaaS tools to Salesforce with zero downtime',
        'image_placeholder': '🔗',
        'problem': '''A fast-growing SaaS company used 15+ different tools (Zendesk, Stripe, HubSpot, etc.) 
        with no integration. Sales and support teams operated blind without customer data visibility across tools.''',
        'solution': '''Architected an integration hub using Platform Events, Change Data Capture, and custom 
        REST APIs. Built middleware on Heroku for complex transformations. Implemented real-time sync for 
        critical data and batch processing for historical data.''',
        'tech_stack': ['Platform Events', 'Change Data Capture', 'REST APIs', 'Heroku', 'Redis'],
        'results': [
            'Real-time sync of customer data across 15 tools',
            '99.9% sync reliability (measured over 6 months)',
            'Support team resolution time reduced 40%',
            'Sales team visibility into customer health scores'
        ],
        'featured': False,
        'duration': '4 months',
        'team_size': '3 developers + 1 integration architect'
    }
]

# Client Testimonials
TESTIMONIALS = [
    {
        'quote': '''A-frame Solutions transformed our patient engagement strategy. Their deep understanding 
        of both Salesforce and healthcare compliance gave us confidence throughout the project. The portal 
        they built has become indispensable to our operations.''',
        'author': 'Dr. Sarah Mitchell',
        'title': 'Chief Medical Information Officer',
        'company': 'Regional Healthcare System',
        'rating': 5
    },
    {
        'quote': '''Working with A-frame was a game-changer for our firm. They didn't just implement 
        Financial Services Cloud—they understood our business model and built a solution that our advisors 
        actually love using. ROI was evident within the first quarter.''',
        'author': 'James Patterson',
        'title': 'Managing Partner',
        'company': 'Private Wealth Advisors',
        'rating': 5
    },
    {
        'quote': '''The CPQ solution A-frame built has fundamentally changed how we sell. What used to take 
        our sales team days now takes minutes, and the accuracy is perfect. The team's Apex development 
        skills are world-class.''',
        'author': 'Michael Chen',
        'title': 'VP of Sales',
        'company': 'Industrial Equipment Manufacturer',
        'rating': 5
    },
    {
        'quote': '''As a technical team, we're very particular about code quality. A-frame's developers 
        exceeded our standards—clean code, excellent documentation, and they taught us best practices 
        along the way. True Salesforce experts.''',
        'author': 'Lisa Rodriguez',
        'title': 'CTO',
        'company': 'Enterprise SaaS Company',
        'rating': 5
    }
]

# Stats for trust indicators
STATS = [
    {'number': '200+', 'label': 'Projects Delivered'},
    {'number': '98%', 'label': 'Client Satisfaction'},
    {'number': '12+', 'label': 'Years Experience'},
    {'number': '$50M+', 'label': 'ROI Generated for Clients'}
]

# Routes
@app.route('/')
def home():
    featured_projects = [p for p in PROJECTS if p.get('featured', False)]
    return render_template('home.html', 
                         config=SITE_CONFIG, 
                         services=SERVICES[:4],  # Show first 4 services
                         projects=featured_projects,
                         testimonials=TESTIMONIALS[:3],
                         stats=STATS)

@app.route('/services')
def services():
    return render_template('services.html', 
                         config=SITE_CONFIG, 
                         services=SERVICES)

@app.route('/services/<service_id>')
def service_detail(service_id):
    service = next((s for s in SERVICES if s['id'] == service_id), None)
    if not service:
        return redirect(url_for('services'))
    
    # Get related case studies
    related_projects = [p for p in PROJECTS if any(
        tech in service['tech_highlights'] for tech in p.get('tech_stack', [])
    )][:3]
    
    return render_template('service_detail.html', 
                         config=SITE_CONFIG, 
                         service=service,
                         related_projects=related_projects)

@app.route('/projects')
def projects():
    return render_template('projects.html', 
                         config=SITE_CONFIG, 
                         projects=PROJECTS,
                         stats=STATS)

@app.route('/projects/<project_id>')
def project_detail(project_id):
    project = next((p for p in PROJECTS if p['id'] == project_id), None)
    if not project:
        return redirect(url_for('projects'))
    
    # Get related projects (same industry)
    related_projects = [p for p in PROJECTS 
                       if p['id'] != project_id and p.get('industry') == project.get('industry')][:2]
    
    return render_template('project_detail.html', 
                         config=SITE_CONFIG, 
                         project=project,
                         related_projects=related_projects)

@app.route('/about')
def about():
    return render_template('about.html', 
                         config=SITE_CONFIG)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        company = request.form.get('company')
        budget = request.form.get('budget')
        message = request.form.get('message')
        
        # Here you would typically send an email or save to database
        # For now, we'll just print to console and show a success message
        print(f"New Contact Form Submission:")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Company: {company}")
        print(f"Budget: {budget}")
        print(f"Message: {message}")
        
        flash('Thank you for your message! We will respond within 24 hours.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html', 
                         config=SITE_CONFIG)

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)