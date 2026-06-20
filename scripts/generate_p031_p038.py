import pandas as pd
import os
import jinja2
import re
from datetime import datetime

# Paths
BASE_DIR = "/home/yorch/Documentos/helm-hackathon/synthetic-data"
PROPERTIES_CSV = os.path.join(BASE_DIR, "meridianav1/datasets/raw/properties.csv")
FEATURES_CSV = os.path.join(BASE_DIR, "meridianav1/datasets/raw/property_features.csv")
AGENTS_CSV = os.path.join(BASE_DIR, "meridianav1/datasets/raw/agents.csv")
TEMPLATE_PATH = os.path.join(BASE_DIR, "meridianav1/templates/public/property-brochure.html")
PROPERTIES_DIR = os.path.join(BASE_DIR, "meridianav1/properties")

def format_currency(value):
    try:
        return "{:,.0f}".format(float(value))
    except:
        return value

def mustache_to_jinja(template_content):
    # Handle the features loop specifically
    template_content = re.sub(r'\{\{#features\}\}(.*?)\{\{/features\}\}', 
                              r'{% for feature in features %}\1{% endfor %}', 
                              template_content, flags=re.DOTALL)
    
    template_content = template_content.replace('{{feature_name}}', '{{feature.feature_name}}')
    
    # Handle boolean sections
    template_content = re.sub(r'\{\{#([\w_]+)\}\}', r'{% if \1 %}', template_content)
    template_content = re.sub(r'\{\{\^([\w_]+)\}\}', r'{% if not \1 %}', template_content)
    template_content = re.sub(r'\{\{/([\w_]+)\}\}', r'{% endif %}', template_content)
    
    # Fix the hardcoded avatar initial
    template_content = template_content.replace('<div class="agent-avatar"><span>M</span></div>', 
                                              '<div class="agent-avatar"><span>{{agent_initial}}</span></div>')
    
    return template_content

def generate_brochures():
    # Load data
    df_prop = pd.read_csv(PROPERTIES_CSV)
    df_feat = pd.read_csv(FEATURES_CSV)
    df_agents = pd.read_csv(AGENTS_CSV)
    
    # Load template
    with open(TEMPLATE_PATH, 'r') as f:
        template_raw = f.read()
    
    jinja_template_content = mustache_to_jinja(template_raw)
    env = jinja2.Environment()
    template = env.from_string(jinja_template_content)
    
    # Filter for P031-P038
    target_ids = [f'P{str(i).zfill(3)}' for i in range(31, 39)]
    df_prop_subset = df_prop[df_prop['property_id'].isin(target_ids)]
    
    for _, prop in df_prop_subset.iterrows():
        prop_id = prop['property_id']
        print(f"Generating brochure for {prop_id}...")
        
        # Logic for special status
        is_renta = (prop['listing_type'] == 'renta')
        is_sold = (prop['status'] in ['vendida', 'rentada'])
        
        # Get Agent
        agent_matches = df_agents[df_agents['agent_id'] == prop['agent_id']]
        if not agent_matches.empty:
            agent = agent_matches.iloc[0]
        else:
            # Fallback or error
            print(f"Warning: Agent {prop['agent_id']} not found for {prop_id}")
            agent = {'full_name': 'Meridiana Agent', 'phone': 'N/A', 'email': 'contact@meridiana.mx'}
        
        # Get Features (Public only)
        features = df_feat[(df_feat['property_id'] == prop_id) & (df_feat['is_public'] == 'sí')]
        features_list = features.to_dict('records')
        
        # Context for rendering
        context = {
            'brand_name': 'Meridiana',
            'property_title': prop['title'],
            'listing_code': prop['listing_code'],
            'commercial_name': prop['commercial_name'],
            'property_type': prop['property_type'],
            'listing_type': prop['listing_type'],
            'neighborhood': prop['neighborhood'],
            'municipality': prop['municipality'],
            'state': prop['state'],
            'price_mxn': format_currency(prop['price_mxn']),
            'is_renta': is_renta,
            'is_sold': is_sold,
            'title': prop['title'],
            'bedrooms': prop['bedrooms'],
            'bathrooms': prop['bathrooms'],
            'construction_m2': prop['construction_m2'],
            'lot_m2': prop['lot_m2'],
            'parking_spaces': prop['parking_spaces'],
            'public_description': prop['public_description'],
            'features': features_list,
            'address_line': prop['address_line'],
            'agent_name': agent['full_name'],
            'agent_phone': agent['phone'],
            'agent_email': agent['email'],
            'agent_initial': agent['full_name'][0] if agent['full_name'] else 'M'
        }
        
        # Render HTML
        output_html = template.render(context)
        
        # Write HTML
        dest_dir = os.path.join(PROPERTIES_DIR, prop_id)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
            
        dest_path = os.path.join(dest_dir, "property-brochure.html")
        with open(dest_path, 'w') as f:
            f.write(output_html)
            
        # Generate MD documentation
        md_content = f"""# Data Mapping - {prop_id} ({prop['commercial_name']})

## General Information
- **Brand Name:** Meridiana (Hardcoded)
- **Listing Code:** {prop['listing_code']}
- **Commercial Name:** {prop['commercial_name']}
- **Title:** {prop['title']}
- **Property Type:** {prop['property_type']}
- **Listing Type:** {prop['listing_type']}
- **Price:** {"Vendido" if is_sold else f"${context['price_mxn']} MXN" + (" (Renta)" if is_renta else "")}

## Stats
- **Bedrooms:** {prop['bedrooms']}
- **Bathrooms:** {prop['bathrooms']}
- **Construction:** {prop['construction_m2']} m²
- **Lot:** {prop['lot_m2']} m²
- **Parking:** {prop['parking_spaces']}

## Location
- **Address:** {prop['address_line']}
- **Neighborhood:** {prop['neighborhood']}
- **Municipality:** {prop['municipality']}
- **State:** {prop['state']}

## Agent Details
- **Name:** {agent['full_name']}
- **Email:** {agent['email']}
- **Phone:** {agent['phone']}

## Description Mapping
- **Main Title:** {prop['commercial_name']} (from `commercial_name`)
- **Cover Tagline:** {prop['title']} (from `title`)
- **Detailed Description:** `title` + `public_description`

## Features
"""
        for feat in features_list:
            md_content += f"- {feat['feature_name']}\n"
        
        md_content += f"\n*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
        
        md_path = os.path.join(dest_dir, f"{prop_id}.md")
        with open(md_path, 'w') as f:
            f.write(md_content)
            
        print(f"Done: {dest_path} and {md_path}")

if __name__ == "__main__":
    generate_brochures()
