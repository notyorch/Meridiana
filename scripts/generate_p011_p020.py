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
LOG_PATH = os.path.join(PROPERTIES_DIR, "GENERATION_LOG.md")

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
    
    # Filter for P011-P020
    target_ids = [f'P{str(i).zfill(3)}' for i in range(11, 21)]
    df_prop_target = df_prop[df_prop['property_id'].isin(target_ids)]
    
    for _, prop in df_prop_target.iterrows():
        prop_id = prop['property_id']
        print(f"Generating brochure for {prop_id}...")
        
        # Logic
        is_renta = (prop['listing_type'] == 'renta')
        is_sold = (prop['status'] in ['vendida', 'rentada'])
        
        # Get Agent
        agent_match = df_agents[df_agents['agent_id'] == prop['agent_id']]
        if agent_match.empty:
            print(f"Warning: Agent {prop['agent_id']} not found for {prop_id}")
            agent_name = "Meridiana Agent"
            agent_phone = "Contact us"
            agent_email = "info@meridiana.mx"
        else:
            agent = agent_match.iloc[0]
            agent_name = agent['full_name']
            agent_phone = agent['phone']
            agent_email = agent['email']
        
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
            'features': [{'feature_name': f['feature_name']} for f in features_list],
            'address_line': prop['address_line'],
            'agent_name': agent_name,
            'agent_phone': agent_phone,
            'agent_email': agent_email
        }
        
        # Render HTML
        output_html = template.render(context)
        
        # Write HTML
        dest_dir = os.path.join(PROPERTIES_DIR, prop_id)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
            
        html_path = os.path.join(dest_dir, "property-brochure.html")
        with open(html_path, 'w') as f:
            f.write(output_html)
            
        # Create Pxxx.md
        md_content = f"""# Documentación de Control - {prop_id}

## 1. Mapeo de Campos
- **Título Principal:** `{prop['commercial_name']}`
- **Subtítulo:** `{prop['title']}`
- **Precio:** `${format_currency(prop['price_mxn'])} MXN` {"(Oculto por estatus)" if is_sold else ""}
- **Estatus Especial:** {"Renta (PRECIO POR MES)" if is_renta else "Venta"}
- **Disponibilidad:** {"Vendido/Rentado" if is_sold else "Disponible"}
- **Agente:** {agent_name}

## 2. Datos Hardcodeados
- Marca: "Meridiana"
- Ubicación de marca: "Mérida · Yucatán"

## 3. Fecha de Generación
- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        md_path = os.path.join(dest_dir, f"{prop_id}.md")
        with open(md_path, 'w') as f:
            f.write(md_content)
            
        print(f"Done: {prop_id}")

if __name__ == "__main__":
    generate_brochures()
