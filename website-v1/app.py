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
    'tagline': 'Custom web apps that actually ship',
    'email': 'contact@yourcompany.com',
    'linkedin': 'https://www.linkedin.com/in/didrik-lindberg-3b2955148/',
    'phone': '+1 (555) 123-4567',
}

# Services data - EDIT THIS
SERVICES = [
    {
        'id': 'web-app-development',
        'title': 'Web App Development',
        'icon': '🚀',
        'short_description': 'Custom web applications built with modern frameworks and best practices.',
        'full_description': 'We build scalable, maintainable web applications tailored to your business needs. From MVPs to enterprise solutions, we handle the entire development lifecycle.',
        'deliverables': [
            'Custom web application development',
            'Database design and optimization',
            'API development and integration',
            'User authentication and authorization',
            'Responsive frontend design',
            'Testing and quality assurance',
        ],
        'ideal_for': 'SaaS startups, businesses needing custom internal tools, companies outgrowing spreadsheets',
        'outcomes': [
            'Faster operations and reduced manual work',
            'Scalable architecture that grows with you',
            'Clean, maintainable codebase',
            'Modern UX that users actually enjoy',
        ]
    },
    {
        'id': 'api-integrations',
        'title': 'API Integration & Automation',
        'icon': '🔗',
        'short_description': 'Connect your tools and automate workflows to save time and reduce errors.',
        'full_description': 'We integrate your existing tools and platforms, building custom middleware and automation that eliminates manual data entry and keeps your systems in sync.',
        'deliverables': [
            'Third-party API integration',
            'Custom middleware development',
            'Workflow automation',
            'Data synchronization',
            'Webhook implementations',
            'Documentation and support',
        ],
        'ideal_for': 'Businesses using multiple SaaS tools, companies with manual data entry, teams seeking efficiency',
        'outcomes': [
            'Eliminate duplicate data entry',
            'Real-time data synchronization',
            'Reduced human error',
            'Better visibility across tooling',
            'Teams focus on higher-value work',
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
        'id': 'saas-dashboard',
        'title': 'SaaS Analytics Dashboard',
        'client': 'TechCorp (SaaS Startup)',
        'tagline': 'Real-time analytics platform that increased customer retention by 40%',
        'image_placeholder': '📊',
        'problem': 'TechCorp needed a way to give their B2B customers visibility into usage metrics and ROI. Their existing reporting was manual and time-consuming.',
        'solution': 'Built a real-time analytics dashboard with interactive charts, custom reporting, and automated email summaries. Integrated with their existing API and data warehouse.',
        'tech_stack': ['Python', 'Flask', 'PostgreSQL', 'React', 'Chart.js', 'Celery'],
        'results': [
            '+40% customer retention',
            '15 hours/week saved on manual reporting',
            'Customers upgrade faster after seeing ROI',
            'Reduced support tickets by 30%',
        ],
        'featured': True,
    },
    {
        'id': 'crm-integration',
        'title': 'Multi-Platform CRM Integration',
        'client': 'GrowthAgency (Marketing Agency)',
        'tagline': 'Automated data sync across 5 platforms, eliminating manual entry',
        'image_placeholder': '🔗',
        'problem': 'Marketing agency was manually copying client data between Salesforce, their project management tool, invoicing system, and email marketing platform. This caused errors and wasted hours every week.',
        'solution': 'Built custom middleware that syncs data in real-time across all platforms using webhooks and scheduled jobs. Created a central dashboard to monitor sync status.',
        'tech_stack': ['Python', 'FastAPI', 'Redis', 'Salesforce API', 'Asana API', 'QuickBooks API'],
        'results': [
            '20+ hours saved per week',
            '95% reduction in data entry errors',
            'Real-time data synchronization',
            'ROI achieved in 6 weeks',
        ],
        'featured': True,
    },
    {
        'id': 'ecommerce-platform',
        'title': 'Custom E-commerce Platform',
        'client': 'ArtisanGoods (Retail)',
        'tagline': 'Built a custom e-commerce solution that doubled online sales',
        'image_placeholder': '🛒',
        'problem': 'Small retail business outgrew their Shopify setup and needed custom features for their unique business model (subscription boxes + one-time purchases).',
        'solution': 'Developed a custom e-commerce platform with subscription management, inventory tracking, and integration with their existing POS system. Mobile-first design with fast checkout.',
        'tech_stack': ['Python', 'Django', 'PostgreSQL', 'Stripe', 'Tailwind CSS'],
        'results': [
            '2x online sales in 6 months',
            'Subscription revenue up 150%',
            'Mobile conversion rate increased 65%',
            'Average order value up 35%',
        ],
        'featured': False,
    },
    {
        'id': 'internal-tool',
        'title': 'Operations Management Tool',
        'client': 'LogisticsPro (Supply Chain)',
        'tagline': 'Internal tool that streamlined operations and improved team efficiency',
        'image_placeholder': '⚙️',
        'problem': 'Operations team was using spreadsheets and email to coordinate shipments, leading to errors, delays, and poor visibility.',
        'solution': 'Built a custom operations management tool with real-time tracking, automated notifications, and reporting dashboard. Integrated with their shipping carriers and warehouse systems.',
        'tech_stack': ['Python', 'Flask', 'MySQL', 'Vue.js', 'Docker'],
        'results': [
            'Operational errors reduced 85%',
            'Average delivery time reduced by 2 days',
            'Team efficiency improved 40%',
            'Real-time visibility across operations',
        ],
        'featured': False,
    },
]

# Testimonials - EDIT THIS
TESTIMONIALS = [
    {
        'quote': 'Working with [Company Name] was a game-changer. They delivered exactly what we needed, on time and on budget. The custom dashboard has become essential to our business.',
        'author': 'Sarah Johnson',
        'title': 'CEO, TechCorp',
        'company': 'TechCorp',
    },
    {
        'quote': 'The integration work saved us 20+ hours every single week. The ROI was immediate and the quality of work was exceptional. Highly recommend!',
        'author': 'Michael Chen',
        'title': 'Operations Director',
        'company': 'GrowthAgency',
    },
    {
        'quote': 'They took the time to understand our unique business needs and built a solution that actually fits how we work. Our online sales have doubled since launch.',
        'author': 'Emily Rodriguez',
        'title': 'Founder',
        'company': 'ArtisanGoods',
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
