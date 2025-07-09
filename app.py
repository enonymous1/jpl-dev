from flask import Flask, render_template, url_for
from flask_frozen import Freezer
import json
import re

app = Flask(__name__)
app.config['FREEZER_DESTINATION'] = 'docs'
app.config['FREEZER_RELATIVE_URLS'] = True
freezer = Freezer(app)

# Custom filter to convert newlines to HTML breaks
@app.template_filter('nl2br')
def nl2br_filter(text):
    if text is None:
        return ''
    return text.replace('\n', '<br>\n')

# Provision text map with exact content from SCP-FSS-001
PROVISION_TEXT_MAP = {
    "(c)": """(c) Offers must be current, accurate, and complete, and demonstrate a thorough understanding of solicitation requirements. By submission of an offer:
(1) The offeror has not taken exceptions to the terms and conditions of this solicitation unless explicitly identified in eOffer (see "Exceptions to Terms and Conditions" under the Standard Response module).
(2) The offeror understands and agrees to comply with the requirements of all clauses and provisions. Failure to comply with applicable clauses and provisions will result in rejection of the offer. Offerors are responsible for ensuring that their offers meet ALL solicitation requirements and should not assume that deficient items will be clarified prior to the offer being rejected.
(3) The offeror understands and agrees to comply with the requirements of GSAR clause, 552.238-80 Industrial Funding Fee and Sales Reporting OR GSAR clause 552.238-80, Industrial Funding Fee and Sales Reporting (Alternate I) if participating in Transactional Data Reporting (TDR) (see paragraph (f) below for more information on TDR).""",
    
    "(d) (1-4)": """(d) Existing Federal Supply Schedule (FSS) Program contractors and any small business who does not have its own FSS program contract but is performing under an active FSS program joint venture contract as a joint venture partner may submit a streamlined offer if the following criteria are met:
(1) The offeror is requesting award of Special Item Number(s) (SIN(s)) under the same subcategory as its current FSS program contract(s);
(2) The offeror is not requesting award of any new labor categories under a services SIN;
(3) The offeror is not requesting award of any new SINs that would change the predominant contract type of the FSS program contract (i.e., supply to service or service to supply); and
(4) The offeror held an FSS program contract that was not canceled for cause, non-compliance, or convenience of the Government due to the contractor's non-performance.""",
    
    "(e)": """(e) A current FSS contractor can submit an offer for a continuous contract beginning on the first day of the month following the month in which the FSS contractor's current contract expires. However, the offeror must satisfy the eligibility criteria in paragraph (d) above. Additionally, the offeror must be in good standing (i.e., current on reporting requirements and Industrial Funding Fee (IFF) payments) on its current FSS program contract. Continuous contracts will be awarded for the full ordering period.""",
    
    "(i)": """(i) Rejection of Offer. If GSA previously rejected an offeror's offer, GSA will not consider a new offer from the same offeror for award of the same SIN(s) unless the offeror submits a point-by-point response to GSA's rejection letter with its new offer. The new offer must also address all deficiencies noted in the previous rejection letter. The point-by-point response must be submitted as a separate document and uploaded to eOffer. See "Rejection of Offer" under the Standard Response module for more information.""",
    
    "(j) (1) (i.)": """(j) (1) (i.) Pathway to Success. The offeror must acknowledge that it has downloaded and completed the Pathway to Success training within the past 12 months. The Pathway to Success training is available at GSA.gov/PathwaytoSuccess. This training covers the fundamental concepts of the FSS program and the GSA Advantage!® online catalog. Completion of this training is required for all new FSS contractors and is strongly recommended for existing FSS contractors submitting offers for additional SINs.""",
    
    "(j) (1) (ii.)": """(j) (1) (ii.) Readiness Assessment. The offeror must acknowledge that it has downloaded and completed the Readiness Assessment within the past 12 months. The Readiness Assessment is available at GSA.gov/ReadinessAssessment. This assessment helps offerors determine their readiness to compete for and manage an FSS contract.""",
    
    "(j) (1) (iii.)": """(j) (1) (iii.) System for Award Management (SAM) Registration. The offeror must have a current, accurate, and complete SAM registration that reflects the North American Industrial Classification System (NAICS) code(s) for this solicitation and the products/services proposed. The offeror must maintain an active SAM registration throughout the life of any contract awarded as a result of this solicitation.""",
    
    "(j) (1) (iv.)": """(j) (1) (iv.) Previous Contract Performance. If an offeror was previously awarded a Schedule contract, and it was subsequently cancelled or allowed to expire due to low sales or non-compliance with other contract terms and conditions, the offeror must provide a detailed description of the steps the offeror plans to take to generate sales and/or ensure compliance through a new contract.""",
    
    "(j) (1) (v.)": """(j) (1) (v.) Financial Responsibility. The offeror must provide annual financial statements for the previous 2 years (balance sheet and income statement), unless submitting under Startup Springboard. The firm must provide an explanation for any negative financial information disclosed.""",
    
    "(j) (1) (vi.)": """(j) (1) (vi.) Subcontracting Plan. If applicable, the offeror must submit a subcontracting plan in accordance with FAR 19.7 and the clause at 52.219-9, Small Business Subcontracting Plan.""",
    
    "(j) (1) (viii.)": """(j) (1) (viii.) Agent Authorization Letter. If applicable, an Agent Authorization Letter must be completed and submitted as part of the offer if a consultant or third-party agent assisted in the preparation of the offer, will be involved in any part of the negotiation of the offer, or will be involved in any post-award actions.""",
    
    "(j) (1) (ix.)": """(j) (1) (ix.) Section 508 Compliance. Section 508 of the Rehabilitation Act, as amended by the Workforce Investment Act of 1998 (P.L. 105-220) requires that when Federal agencies develop, procure, maintain, or use information and communication technology (ICT), it must be accessible to people with disabilities.""",
    
    "(j) (1) (x.)": """(j) (1) (x.) Trade Agreements Act (TAA) Compliance. The offeror must identify the country of origin for all products offered. All products must comply with the Trade Agreements Act.""",
    
    "(j) (1) (xi.)": """(j) (1) (xi.) Letter of Commitment/Supply. If applicable, the offeror must provide a Letter of Commitment/Supply from the manufacturer or authorized distributor for all products offered.""",
    
    "(j) (1) (xii.)": """(j) (1) (xii.) Product Obsolescence. If an item appears to be obsolete, GSA may request additional information, such as confirmation of sufficient availability of supply and may decide the item should not be offered under the MAS program.""",
    
    "(j) (1) (xiii.)": """(j) (1) (xiii.) Prohibited Products. Products that are solely compatible with products that are prohibited for national security reasons (e.g., FAR clauses 52.204-23; 52.204-25; and 52.204-30) may not be offered under MAS contracts.""",
    
    "(j) (1) (xiv)": """(j) (1) (xiv.) Dealer/Reseller Functions. If applicable, the offeror must describe dealer/reseller functions for products offered.""",
    
    "(j) (1) (xv.)": """(j) (1) (xv.) AbilityOne Program. If applicable, the offeror must be an authorized AbilityOne Program distributor for products on the AbilityOne Procurement List.""",
    
    "(j) (1) (xvi.)": """(j) (1) (xvi.) Manufacturer Part Number (MPN) and Universal Product Code (UPC-A). For products only, accurate MPN and/or UPC-A data must be submitted.""",
    
    "(j) (1) (xvii.)": """(j) (1) (xvii.) Electronic Contract Data. Following contract award, Schedule contractors offering products under designated Special Item Numbers (SINs) must submit detailed electronic contract data, such as, but not limited to, Universal Product Codes (UPC) and product photos for each item offered on GSA Advantage!®.""",
    
    "(j) (1) (xviii.)": """(j) (1) (xviii.) GSA Advantage Purchase Order (PO) Portal. The offeror must use EDI, cXML or the GSA Advantage Purchase Order (PO) Portal to provide order acknowledgment information that enables ordering agencies to track the location of an order at any time.""",
    
    "(j) (1) (xix.)": """(j) (1) (xix.) Frustrated Freight. For products only, GSAR Clause 552.211-73, Marking, establishes marking and labeling requirements for shipping Federal Government orders. The Government reserves the right to require sample electronic versions of all required documents.""",
    
    "(j) (1) (xx.)": """(j) (1) (xx.) Joint Ventures. All joint venture offerors, regardless of size status, must complete the All Joint Ventures section of the Joint Venture Solicitation Attachment and Appendix A.""",
    
    "(j) (2) (i.)": """(j) (2) (i.) Corporate Experience Narrative. The offeror must provide a minimum of 2 years of corporate experience, unless submitting under Startup Springboard. This narrative should demonstrate the offeror's ability to successfully perform under this solicitation.""",
    
    "(j) (2) (ii.)": """(j) (2) (ii.) Past Performance. The offeror must provide past performance information, including contractor performance assessment reports (CPARS) or customer references and past performance questionnaires.""",
    
    "(j) (2) (iii.)": """(j) (2) (iii.) Quality Control Narrative. The offeror must provide a quality control narrative describing the offeror's quality control procedures and processes.""",
    
    "(j) (2) (iv.)": """(j) (2) (iv.) Relative Project Experience Narrative. For offers including services, the offeror must provide a narrative describing relevant project experience for the services being offered.""",
    
    "(j) (3) (ii.)": """(j) (3) (ii.) Completed Price Proposal Template. The offeror must submit a completed Price Proposal Template in Excel format with all proposed prices and supporting documentation.""",
    
    "(j) (3) (iii.)": """(j) (3) (iii.) Supporting Documentation. The offeror must provide supporting documentation for EACH proposed product/service price. Supporting pricing documentation may consist of published and publicly-available commercial catalogs/price lists, copies of invoices, contracts, or quote sheets.""",
    
    "(j) (3) (iv.)": """(j) (3) (iv.) Most Favored Customer Justification. If the pricing offered is not equal to or better than the pricing extended to the Most Favored Customer, the offeror must provide justification.""",
    
    "(j) (3) (v.)": """(j) (3) (v.) Proposed Escalation Method. The offeror must propose an escalation method: 552.216-70 (EPA) for Commercial Price List or I-FSS-969 (Escalation Rate) for Market Pricing.""",
    
    "(j) (3) (vi.)": """(j) (3) (vi.) Commercial Sales Practices Document (CSP-1). The offeror must complete the CSP-1 with rationale to support projected MAS sales. This document is applicable to Non-TDR offers only.""",
    
    "(j) (3) (vii.)": """(j) (3) (vii.) Full and Broad Offering. The offeror must present a total solution with a full and broad offering of services and/or products.""",
    
    "(j) (3) (viii.)": """(j) (3) (viii.) Remanufactured Items. Remanufactured items are only allowable under specific MAS SINs and must be identified per clause 552.238-78 and meet the prescribed definition of "factory rebuilt to original specifications.".""",
    
    "(j) (3) (ix.)": """(j) (3) (ix.) Fair and Reasonable Pricing. All offers must demonstrate fair and reasonable pricing. This requirement is applicable to ALL offers.""",
    
    "(j) (3) (x.) (A)": """(j) (3) (x.) (A) Position Descriptions. For services offers, the offeror must provide detailed position descriptions for each labor category proposed, including minimum years of relevant experience and educational requirements.""",
    
    "(j) (3) (x.) (B)": """(j) (3) (x.) (B) Training Course Descriptions. For offers containing training SINs, the offeror must provide detailed training course descriptions.""",
    
    "(j) (3) (x.) (C)": """(j) (3) (x.) (C) Fixed Price Services Descriptions. For offers containing fixed price solutions, the offeror must provide descriptions that clearly demonstrate how each service is within scope of the applicable SIN(s).""",
    
    "(j) (3) (x.) (D)": """(j) (3) (x.) (D) Ancillary Supplies and Services/ODCs Descriptions. If applicable, the offeror must provide descriptions of ancillary supplies and services or Other Direct Costs (ODCs).""",
    
    "(j) (3) (x.) (E)": """(j) (3) (x.) (E) Fully Burdened Rates. All proposed prices must be inclusive of all cost factors and represent fully burdened rates.""",
    
    "(j) (3) (xi.)": """(j) (3) (xi.) Professional Compensation Plan. For professional services offers, the offeror must provide a Professional Compensation Plan in accordance with provision 52.222-46 Evaluation of Compensation for Professional Employees.""",
    
    "(j) (3) (xii.)": """(j) (3) (xii.) Policy on Uncompensated Overtime. For services offers, the offeror must provide a policy on uncompensated overtime that clearly shows how the company addresses uncompensated overtime without resulting in unreasonably low hourly rates.""",
    
    "(j) (3) (xiii.) (B)": """(j) (3) (xiii.) (B) Service Contract Labor Standards (SCLS) Wage Determination. For applicable services offers, the offeror must comply with Service Contract Labor Standards wage determination requirements.""",
    
    "(j) (3) (xiii.) (C)": """(j) (3) (xiii.) (C) Service Contract Labor Standards (SCLS)/SCA Matrix. For all offers that include services, the offeror must submit a matrix that lists all employees that will work on the contract and identifies which employees are considered "Service Employees" as defined by clause 52.222-41.""",
}

def get_provision_text(reference_text):
    """Get provision text using direct lookup from the provision text map"""
    if not reference_text:
        return "No reference provided."
    
    # Clean the reference to get a key like "(c)" or "(j) (1) (i.)"
    ref_key = reference_text.replace('Provision SCP-FSS-001', '').strip()
    
    # Look up the key in our map and return the full text
    return PROVISION_TEXT_MAP.get(ref_key, f'Could not find provision text for reference: "{ref_key}"')

def create_pdf_link(reference_text, pdf_filename):
    """Create a PDF link and get content using direct lookup"""
    if not reference_text or 'SCP-FSS-001' not in reference_text:
        return {'link': reference_text, 'content': None}
    
    # Create a PDF link using url_for for proper path generation
    pdf_url = url_for('static', filename=f'files/{pdf_filename}')
    pdf_link = reference_text.replace('SCP-FSS-001', f'<a href="{pdf_url}" target="_blank" class="pdf-link">SCP-FSS-001</a>')
    
    # Get content using direct lookup
    pdf_content = get_provision_text(reference_text)
    
    return {'link': pdf_link, 'content': pdf_content}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projects/')
def projects():
    return render_template('projects.html')

@app.route('/projects/gsa-mas-checklist/')
def gsa_mas_checklist():
    with open('checklist_data.json') as f:
        data = json.load(f)

    # Group items by section while preserving order
    ordered_sections = []
    section_map = {}
    for item in data:
        section_name = item['Section']
        if section_name not in section_map:
            section_map[section_name] = []
            ordered_sections.append({'name': section_name, 'item_list': section_map[section_name]})
        section_map[section_name].append(item)

    return render_template('projects/gsa_mas_checklist.html', 
                         sections=ordered_sections, 
                         create_pdf_link=create_pdf_link)

if __name__ == '__main__':
    app.run(debug=True)
